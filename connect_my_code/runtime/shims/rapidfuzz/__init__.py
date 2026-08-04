"""Pure-standard-library stand-in for the slice of RapidFuzz graphify uses.

Upstream imports RapidFuzz in one module, ``graphify/dedup.py``, and only from
``rapidfuzz.distance``: ``Jaro``, ``JaroWinkler`` and ``DamerauLevenshtein``.
Those live in :mod:`rapidfuzz.distance`; this package exists to hold it.
"""
from __future__ import annotations

from . import distance  # noqa: F401  (re-exported for `from rapidfuzz import distance`)

__version__ = "0.0.0+connect_my_code-shim"
__all__ = ["distance"]
