"""Bundled ``tree_sitter_lua`` grammar.

Structural parser, not a full grammar reimplementation: it recognises the type
declarations, functions, imports, inheritance clauses and call expressions
graphify builds its graph from, and emits the node types the real
tree-sitter-lua grammar uses for them. See ``tree_sitter/_brace.py`` for the
recall-versus-correctness trade this makes, and ``tree_sitter/_langs.py`` for
this language's node type names.

If the real ``tree_sitter_lua`` wheel is installed, the front-end delegates to it and none
of this is used.
"""
from __future__ import annotations

from tree_sitter import PureGrammar
from tree_sitter._brace import parse_brace_language
from tree_sitter._langs import SPECS

__all__ = ["language"]


def language() -> PureGrammar:
    """Grammar handle, as the real ``tree_sitter_lua`` exposes it."""
    spec = SPECS["lua"]
    return PureGrammar("lua", lambda source: parse_brace_language(source, spec))
