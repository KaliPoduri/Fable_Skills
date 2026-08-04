"""String metrics matching ``rapidfuzz.distance``, in pure Python.

Only the three metrics ``graphify/dedup.py`` imports are provided. Each is
exposed as a class with static methods, mirroring RapidFuzz's namespace layout
(``Jaro.normalized_similarity``, ``DamerauLevenshtein.distance``, ...) so the
upstream import line works untouched.

These are the textbook algorithms RapidFuzz implements -- RapidFuzz's speed comes
from SIMD and bit-parallel tricks, not from a different definition -- so scores
agree with the C++ implementation. The one documented divergence risk is
JaroWinkler's prefix-bonus threshold, discussed in :func:`_jaro_winkler`.
"""
from __future__ import annotations

__all__ = ["Jaro", "JaroWinkler", "DamerauLevenshtein", "Levenshtein"]


def _jaro(s1: str, s2: str) -> float:
    """Jaro similarity in [0, 1].

    Two characters match when they are equal and no further apart than
    ``max(len)/2 - 1`` positions; transpositions are matched pairs that occur in
    a different relative order in each string.
    """
    len1, len2 = len(s1), len(s2)
    if not len1 and not len2:
        return 1.0
    if not len1 or not len2:
        return 0.0
    if s1 == s2:
        return 1.0

    window = max(len1, len2) // 2 - 1
    if window < 0:
        window = 0

    s1_matched = [False] * len1
    s2_matched = [False] * len2
    matches = 0
    for i, ch in enumerate(s1):
        start = max(0, i - window)
        end = min(i + window + 1, len2)
        for j in range(start, end):
            if s2_matched[j] or s2[j] != ch:
                continue
            s1_matched[i] = True
            s2_matched[j] = True
            matches += 1
            break

    if matches == 0:
        return 0.0

    # Count transpositions by walking both match sequences in parallel.
    transpositions = 0
    k = 0
    for i in range(len1):
        if not s1_matched[i]:
            continue
        while not s2_matched[k]:
            k += 1
        if s1[i] != s2[k]:
            transpositions += 1
        k += 1
    transpositions //= 2

    return (matches / len1 + matches / len2 + (matches - transpositions) / matches) / 3.0


def _jaro_winkler(s1: str, s2: str, prefix_weight: float = 0.1) -> float:
    """Jaro-Winkler similarity in [0, 1].

    Adds ``prefix * prefix_weight * (1 - jaro)`` for up to 4 leading characters
    in common, gated on the classic 0.7 boost threshold as RapidFuzz does.

    The threshold cannot change any decision graphify makes: dedup only ever
    compares against 92.0 and 97.0 (percent), and a Jaro of 0.7 with the largest
    possible bonus still reaches only 0.82. Above 0.7 the gated and ungated
    formulas are identical, so both variants agree everywhere it matters.
    """
    jaro = _jaro(s1, s2)
    prefix = 0
    for a, b in zip(s1[:4], s2[:4]):
        if a != b:
            break
        prefix += 1
    if jaro > 0.7:
        jaro += prefix * prefix_weight * (1.0 - jaro)
    return jaro


def _damerau_levenshtein(s1: str, s2: str) -> int:
    """Unrestricted Damerau-Levenshtein edit distance.

    The full variant with a last-occurrence table, matching RapidFuzz -- not the
    restricted (OSA) variant. The two agree for the equal-length, distance<=1
    comparisons dedup performs, but the unrestricted form is what RapidFuzz
    exposes under this name, so that is what is implemented.
    """
    len1, len2 = len(s1), len(s2)
    if not len1:
        return len2
    if not len2:
        return len1
    if s1 == s2:
        return 0

    max_dist = len1 + len2
    # Row/column 0 hold the sentinel that makes the transposition term valid at
    # the borders; real characters are indexed from 1.
    matrix = [[0] * (len2 + 2) for _ in range(len1 + 2)]
    matrix[0][0] = max_dist
    for i in range(len1 + 1):
        matrix[i + 1][0] = max_dist
        matrix[i + 1][1] = i
    for j in range(len2 + 1):
        matrix[0][j + 1] = max_dist
        matrix[1][j + 1] = j

    last_row: dict[str, int] = {}
    for i in range(1, len1 + 1):
        last_match_col = 0
        for j in range(1, len2 + 1):
            i2 = last_row.get(s2[j - 1], 0)   # last row where s2[j-1] appeared in s1
            j2 = last_match_col               # last column that matched in this row
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            if cost == 0:
                last_match_col = j
            matrix[i + 1][j + 1] = min(
                matrix[i][j] + cost,                                    # substitution
                matrix[i + 1][j] + 1,                                   # insertion
                matrix[i][j + 1] + 1,                                   # deletion
                matrix[i2][j2] + (i - i2 - 1) + 1 + (j - j2 - 1),       # transposition
            )
        last_row[s1[i - 1]] = i

    return matrix[len1 + 1][len2 + 1]


def _levenshtein(s1: str, s2: str) -> int:
    """Plain Levenshtein distance (two-row dynamic programming)."""
    if s1 == s2:
        return 0
    if not s1:
        return len(s2)
    if not s2:
        return len(s1)
    previous = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1, start=1):
        current = [i]
        for j, c2 in enumerate(s2, start=1):
            current.append(min(previous[j] + 1, current[j - 1] + 1, previous[j - 1] + (c1 != c2)))
        previous = current
    return previous[-1]


def _norm_dist_to_sim(distance: int, s1: str, s2: str) -> float:
    longest = max(len(s1), len(s2))
    return 1.0 if longest == 0 else 1.0 - distance / longest


class Jaro:
    """``rapidfuzz.distance.Jaro``."""

    @staticmethod
    def similarity(s1: str, s2: str, **_kwargs) -> float:
        return _jaro(s1, s2)

    @staticmethod
    def normalized_similarity(s1: str, s2: str, **_kwargs) -> float:
        return _jaro(s1, s2)

    @staticmethod
    def distance(s1: str, s2: str, **_kwargs) -> float:
        return 1.0 - _jaro(s1, s2)

    @staticmethod
    def normalized_distance(s1: str, s2: str, **_kwargs) -> float:
        return 1.0 - _jaro(s1, s2)


class JaroWinkler:
    """``rapidfuzz.distance.JaroWinkler``."""

    @staticmethod
    def similarity(s1: str, s2: str, prefix_weight: float = 0.1, **_kwargs) -> float:
        return _jaro_winkler(s1, s2, prefix_weight)

    @staticmethod
    def normalized_similarity(s1: str, s2: str, prefix_weight: float = 0.1, **_kwargs) -> float:
        return _jaro_winkler(s1, s2, prefix_weight)

    @staticmethod
    def distance(s1: str, s2: str, prefix_weight: float = 0.1, **_kwargs) -> float:
        return 1.0 - _jaro_winkler(s1, s2, prefix_weight)

    @staticmethod
    def normalized_distance(s1: str, s2: str, prefix_weight: float = 0.1, **_kwargs) -> float:
        return 1.0 - _jaro_winkler(s1, s2, prefix_weight)


class DamerauLevenshtein:
    """``rapidfuzz.distance.DamerauLevenshtein``."""

    @staticmethod
    def distance(s1: str, s2: str, **_kwargs) -> int:
        return _damerau_levenshtein(s1, s2)

    @staticmethod
    def similarity(s1: str, s2: str, **_kwargs) -> int:
        return max(len(s1), len(s2)) - _damerau_levenshtein(s1, s2)

    @staticmethod
    def normalized_distance(s1: str, s2: str, **_kwargs) -> float:
        return 1.0 - _norm_dist_to_sim(_damerau_levenshtein(s1, s2), s1, s2)

    @staticmethod
    def normalized_similarity(s1: str, s2: str, **_kwargs) -> float:
        return _norm_dist_to_sim(_damerau_levenshtein(s1, s2), s1, s2)


class Levenshtein:
    """``rapidfuzz.distance.Levenshtein`` -- not imported by graphify today, but
    cheap to provide so a future upstream sync does not trip over it."""

    @staticmethod
    def distance(s1: str, s2: str, **_kwargs) -> int:
        return _levenshtein(s1, s2)

    @staticmethod
    def similarity(s1: str, s2: str, **_kwargs) -> int:
        return max(len(s1), len(s2)) - _levenshtein(s1, s2)

    @staticmethod
    def normalized_distance(s1: str, s2: str, **_kwargs) -> float:
        return 1.0 - _norm_dist_to_sim(_levenshtein(s1, s2), s1, s2)

    @staticmethod
    def normalized_similarity(s1: str, s2: str, **_kwargs) -> float:
        return _norm_dist_to_sim(_levenshtein(s1, s2), s1, s2)
