"""Bundled ``tree_sitter_python`` grammar.

Backed by CPython's own :mod:`ast`, so the parse itself is exact and only the
node vocabulary is translated -- see ``tree_sitter/_python.py``. Of all the
bundled grammars this is the highest-fidelity one; the others are structural
parsers rather than full grammars.
"""
from __future__ import annotations

from tree_sitter import PureGrammar
from tree_sitter._python import parse_python

__all__ = ["language"]


def language() -> PureGrammar:
    """Grammar handle, as the real ``tree_sitter_python`` exposes it."""
    return PureGrammar("python", parse_python)
