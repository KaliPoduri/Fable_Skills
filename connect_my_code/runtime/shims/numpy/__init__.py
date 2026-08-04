"""Pure-standard-library stand-in for the slice of NumPy graphify actually uses.

Upstream imports NumPy in exactly one module, ``graphify/_minhash.py``, for a
MinHash sketch over ``uint64`` arrays. This shim reproduces that slice --
fixed-width unsigned integer arrays, three ufuncs, and the legacy
``RandomState`` generator -- so ``_minhash.py`` runs byte-identical to upstream.

Bit-exactness is the point, not just API compatibility. ``_minhash`` seeds
``RandomState(1)`` to build its hash-family coefficients, and those coefficients
decide which label pairs LSH puts in the same band, which decides which entities
dedup merges. A "close enough" PRNG would silently produce a different graph, so
:class:`RandomState` reimplements the exact legacy NumPy pipeline: randomkit
``mt19937_seed`` seeding, the standard MT19937 twist/temper, ``mt19937_next64``
(high word first), and the masked-rejection bounded fill from
``random_bounded_uint64_fill``.

Deliberately *not* a general NumPy: unsupported dtypes and operations raise
rather than silently approximating. If a future upstream module imports NumPy
for something else, it fails loudly here instead of returning wrong numbers.
"""
from __future__ import annotations

import struct
from typing import Iterable

__version__ = "0.0.0+connect_my_code-shim"

_UINT64_MASK = (1 << 64) - 1


class _UInt64:
    """Scalar ``uint64`` with wraparound arithmetic.

    NumPy's fixed-width integers wrap on overflow where Python's ``int`` grows
    without bound. ``_minhash`` relies on that wraparound in
    ``(a * hv + b) % _MP``, so every operation here re-masks to 64 bits.
    """

    __slots__ = ("value",)
    dtype_name = "uint64"

    def __init__(self, value: "int | _UInt64" = 0) -> None:
        self.value = int(value) & _UINT64_MASK

    def __int__(self) -> int:
        return self.value

    def __index__(self) -> int:
        return self.value

    def __repr__(self) -> str:
        return f"{self.value}"

    def __eq__(self, other) -> bool:
        return self.value == int(other)

    def __hash__(self) -> int:
        return hash(self.value)

    # Arithmetic against scalars and arrays alike. Array operands delegate to
    # ndarray's reflected handlers so `scalar * array` stays elementwise.
    def _binary(self, other, op):
        if isinstance(other, ndarray):
            return NotImplemented
        return _UInt64(op(self.value, int(other)))

    def __mul__(self, other):
        return self._binary(other, lambda a, b: a * b)

    __rmul__ = __mul__

    def __add__(self, other):
        return self._binary(other, lambda a, b: a + b)

    __radd__ = __add__

    def __sub__(self, other):
        return self._binary(other, lambda a, b: a - b)

    def __mod__(self, other):
        return self._binary(other, lambda a, b: a % b)

    def __and__(self, other):
        return self._binary(other, lambda a, b: a & b)

    __rand__ = __and__

    def __lshift__(self, other):
        return self._binary(other, lambda a, b: a << b)

    def __rshift__(self, other):
        return self._binary(other, lambda a, b: a >> b)


uint64 = _UInt64


class ndarray:
    """One-dimensional ``uint64`` array.

    Only the operations ``_minhash`` performs are implemented: elementwise
    arithmetic against a scalar, slicing, iteration, ``len``, and ``tobytes``.
    Storage is a plain list of Python ints already reduced mod 2**64.
    """

    __slots__ = ("_data",)

    def __init__(self, data: Iterable[int]) -> None:
        self._data = [int(v) & _UINT64_MASK for v in data]

    # ── container protocol ────────────────────────────────────────────────
    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

    def __getitem__(self, item):
        if isinstance(item, slice):
            return ndarray(self._data[item])
        return _UInt64(self._data[item])

    def __setitem__(self, item, value) -> None:
        if isinstance(item, slice):
            self._data[item] = [int(v) & _UINT64_MASK for v in value]
        else:
            self._data[item] = int(value) & _UINT64_MASK

    def __repr__(self) -> str:
        return f"array({self._data}, dtype=uint64)"

    def __eq__(self, other) -> bool:
        if isinstance(other, ndarray):
            return self._data == other._data
        return NotImplemented

    __hash__ = None  # arrays are mutable, mirroring NumPy

    # ── elementwise arithmetic ────────────────────────────────────────────
    def _elementwise(self, other, op) -> "ndarray":
        if isinstance(other, ndarray):
            if len(other) != len(self._data):
                raise ValueError(
                    f"operands could not be broadcast together with shapes "
                    f"({len(self._data)},) ({len(other)},)"
                )
            return ndarray(op(a, b) & _UINT64_MASK for a, b in zip(self._data, other._data))
        scalar = int(other)
        return ndarray(op(a, scalar) & _UINT64_MASK for a in self._data)

    def __mul__(self, other):
        return self._elementwise(other, lambda a, b: a * b)

    __rmul__ = __mul__

    def __add__(self, other):
        return self._elementwise(other, lambda a, b: a + b)

    __radd__ = __add__

    def __sub__(self, other):
        return self._elementwise(other, lambda a, b: a - b)

    def __mod__(self, other):
        return self._elementwise(other, lambda a, b: a % b)

    def __and__(self, other):
        return self._elementwise(other, lambda a, b: a & b)

    __rand__ = __and__

    # ── serialization ─────────────────────────────────────────────────────
    def tobytes(self) -> bytes:
        """Raw little-endian ``uint64`` bytes.

        Used only as an LSH band key, so the choice of byte order just has to be
        stable within a run. Pinning little-endian keeps band keys reproducible
        across machines, which native-order NumPy would not guarantee.
        """
        return struct.pack(f"<{len(self._data)}Q", *self._data)

    def copy(self) -> "ndarray":
        return ndarray(self._data)

    @property
    def size(self) -> int:
        return len(self._data)

    @property
    def shape(self) -> tuple:
        return (len(self._data),)


# ── array constructors and ufuncs ─────────────────────────────────────────────


def _check_uint64(dtype) -> None:
    if dtype not in (None, uint64):
        raise TypeError(
            "connect_my_code's bundled NumPy shim supports dtype=uint64 only "
            f"(got {dtype!r}). Install real NumPy to use other dtypes."
        )


def array(values: Iterable[int], dtype=None) -> ndarray:
    _check_uint64(dtype)
    return ndarray(values)


def full(size: int, fill_value, dtype=None) -> ndarray:
    _check_uint64(dtype)
    return ndarray([int(fill_value)] * int(size))


def zeros(size: int, dtype=None) -> ndarray:
    _check_uint64(dtype)
    return ndarray([0] * int(size))


def minimum(a: ndarray, b: ndarray) -> ndarray:
    """Elementwise minimum, matching ``np.minimum``."""
    if isinstance(a, ndarray) and isinstance(b, ndarray):
        if len(a) != len(b):
            raise ValueError("operands could not be broadcast together")
        return ndarray(min(x, y) for x, y in zip(a, b))
    if isinstance(a, ndarray):
        scalar = int(b)
        return ndarray(min(x, scalar) for x in a)
    if isinstance(b, ndarray):
        scalar = int(a)
        return ndarray(min(scalar, y) for y in b)
    return _UInt64(min(int(a), int(b)))


def bitwise_and(a, b):
    """Elementwise bitwise AND, matching ``np.bitwise_and``."""
    if isinstance(a, ndarray):
        return a & b
    if isinstance(b, ndarray):
        return b & a
    return _UInt64(int(a) & int(b))


# ── legacy MT19937 RandomState ────────────────────────────────────────────────


class _MT19937:
    """Reference MT19937, seeded the way legacy NumPy seeds it.

    ``_seed`` is randomkit's ``mt19937_seed``, which differs from the reference
    ``init_genrand``: it stores the running seed *before* advancing it and adds
    ``pos + 1`` to each step. Matching that exactly is what makes the generated
    coefficients agree with real NumPy.
    """

    N = 624
    M = 397
    MATRIX_A = 0x9908B0DF
    UPPER_MASK = 0x80000000
    LOWER_MASK = 0x7FFFFFFF

    def __init__(self, seed: int) -> None:
        self.key = [0] * self.N
        self.pos = self.N
        self._seed(seed)

    def _seed(self, seed: int) -> None:
        seed &= 0xFFFFFFFF
        for pos in range(self.N):
            self.key[pos] = seed
            seed = (1812433253 * (seed ^ (seed >> 30)) + pos + 1) & 0xFFFFFFFF
        self.pos = self.N

    def _generate(self) -> None:
        key, N, M = self.key, self.N, self.M
        for i in range(N - M):
            y = (key[i] & self.UPPER_MASK) | (key[i + 1] & self.LOWER_MASK)
            key[i] = key[i + M] ^ (y >> 1) ^ (-(y & 1) & self.MATRIX_A)
        for i in range(N - M, N - 1):
            y = (key[i] & self.UPPER_MASK) | (key[i + 1] & self.LOWER_MASK)
            key[i] = key[i + (M - N)] ^ (y >> 1) ^ (-(y & 1) & self.MATRIX_A)
        y = (key[N - 1] & self.UPPER_MASK) | (key[0] & self.LOWER_MASK)
        key[N - 1] = key[M - 1] ^ (y >> 1) ^ (-(y & 1) & self.MATRIX_A)
        self.pos = 0

    def next_uint32(self) -> int:
        if self.pos >= self.N:
            self._generate()
        y = self.key[self.pos]
        self.pos += 1
        y ^= y >> 11
        y ^= (y << 7) & 0x9D2C5680
        y ^= (y << 15) & 0xEFC60000
        y ^= y >> 18
        return y & 0xFFFFFFFF

    def next_uint64(self) -> int:
        """``mt19937_next64``: high word drawn first, then the low word."""
        return ((self.next_uint32() << 32) | self.next_uint32()) & _UINT64_MASK


def _bounded_mask(rng: int) -> int:
    """Smallest ``2**k - 1`` that covers ``rng`` (randomkit's mask loop)."""
    mask = rng
    mask |= mask >> 1
    mask |= mask >> 2
    mask |= mask >> 4
    mask |= mask >> 8
    mask |= mask >> 16
    mask |= mask >> 32
    return mask


class RandomState:
    """Legacy ``numpy.random.RandomState``, ``randint`` with ``dtype=uint64``."""

    def __init__(self, seed: int = 0) -> None:
        self._mt = _MT19937(int(seed))

    def randint(self, low: int, high: "int | None" = None, size: "int | None" = None, dtype=uint64):
        _check_uint64(dtype)
        if high is None:
            low, high = 0, low
        low, high = int(low), int(high)
        if high <= low:
            raise ValueError("low >= high")
        # NumPy's half-open [low, high) maps to an inclusive range of width rng.
        rng = high - low - 1
        if size is None:
            return _UInt64(low + self._bounded(rng))
        return ndarray(low + self._bounded(rng) for _ in range(int(size)))

    def _bounded(self, rng: int) -> int:
        """Masked rejection sampling -- ``random_bounded_uint64_fill``."""
        if rng == 0:
            return 0
        mask = _bounded_mask(rng)
        while True:
            value = self._mt.next_uint64() & mask
            if value <= rng:
                return value


class _RandomModule:
    """Namespace backing ``numpy.random`` for attribute-style access."""

    RandomState = RandomState


random = _RandomModule()

__all__ = [
    "ndarray",
    "uint64",
    "array",
    "full",
    "zeros",
    "minimum",
    "bitwise_and",
    "random",
    "RandomState",
]
