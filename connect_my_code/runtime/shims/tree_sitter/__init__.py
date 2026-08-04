"""tree-sitter front-end: real C parser when available, bundled parser otherwise.

Unlike the other shims, this module loads even when a real ``tree_sitter`` is
installed. It is a *delegating* front-end, and that is what makes a mixed
environment work: with real ``tree_sitter`` and real ``tree_sitter_python``
installed but no ``tree_sitter_kotlin``, a single run uses the C parser for
Python and the bundled parser for Kotlin. Gating this module the way the others
are gated would instead hand a bundled grammar marker to a C ``Language()``
constructor and fail.

Dispatch is by grammar object: :class:`Language` recognises a
:class:`PureGrammar` marker produced by a bundled ``tree_sitter_<lang>`` module
and routes to the bundled parser; anything else (a real grammar's PyCapsule) is
forwarded to the genuine extension, which is loaded out of the ambient
environment through ``runtime.bootstrap.real_module``.

``LANGUAGE_VERSION`` is exported because ``graphify/extract.py``'s
``_check_tree_sitter_version()`` reads it and raises unless it is at least 14 --
that check is fatal, which is why the core shim is mandatory while individual
grammar shims are not.
"""
from __future__ import annotations

from ._node import Node, Tree, TreeCursor  # noqa: F401  (part of the public API)

__all__ = [
    "Language",
    "Parser",
    "Node",
    "Tree",
    "TreeCursor",
    "PureGrammar",
    "LANGUAGE_VERSION",
    "MIN_COMPATIBLE_LANGUAGE_VERSION",
]

# Language API v2. graphify requires >= 14; report the version the bundled
# parsers implement against.
LANGUAGE_VERSION = 15
MIN_COMPATIBLE_LANGUAGE_VERSION = 13

__version__ = "0.25.0+connect_my_code-shim"


class PureGrammar:
    """Marker returned by a bundled ``tree_sitter_<lang>.language()``.

    Carries the language's display name and the callable that turns source bytes
    into a :class:`~._node.Tree`. Identity of this type is what
    :class:`Language` dispatches on.
    """

    __slots__ = ("name", "parse")

    def __init__(self, name: str, parse) -> None:
        self.name = name
        self.parse = parse

    def __repr__(self) -> str:
        return f"<PureGrammar {self.name}>"


def _real_tree_sitter():
    """The genuine ``tree_sitter`` extension from the ambient environment, or None."""
    try:
        from runtime import bootstrap
    except ImportError:
        return None
    return bootstrap.real_module("tree_sitter")


class Language:
    """A parser language -- bundled or delegated.

    Accepts what both tree-sitter API generations pass: ``Language(capsule)`` and
    the older ``Language(capsule, name)``.
    """

    def __init__(self, language, name: str | None = None) -> None:
        if isinstance(language, PureGrammar):
            self.grammar: PureGrammar | None = language
            self._delegate = None
            self.name = language.name
            return

        real = _real_tree_sitter()
        if real is None:
            raise TypeError(
                "connect_my_code's bundled tree-sitter front-end received a grammar "
                f"it cannot parse ({type(language).__name__}) and no real tree_sitter "
                "is installed to delegate to."
            )
        self.grammar = None
        try:
            self._delegate = real.Language(language) if name is None else real.Language(language, name)
        except TypeError:
            self._delegate = real.Language(language)
        self.name = name or getattr(self._delegate, "name", "")

    @property
    def version(self) -> int:
        if self._delegate is not None:
            return getattr(self._delegate, "version", LANGUAGE_VERSION)
        return LANGUAGE_VERSION

    def __repr__(self) -> str:
        kind = "bundled" if self.grammar is not None else "native"
        return f"<Language {self.name!r} ({kind})>"


class Parser:
    """Source-to-tree parser, mirroring tree-sitter's constructor generations."""

    def __init__(self, language=None) -> None:
        self._language = None
        self._delegate = None
        if language is not None:
            self.language = language

    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, language) -> None:
        if not isinstance(language, Language):
            # A caller handed us a raw grammar; wrap it so dispatch still works.
            language = Language(language)
        self._language = language
        if language.grammar is None:
            real = _real_tree_sitter()
            if real is None:
                raise TypeError("no native tree_sitter available to delegate to")
            try:
                self._delegate = real.Parser(language._delegate)
            except TypeError:            # pre-0.22 API: set_language() after construction
                self._delegate = real.Parser()
                self._delegate.set_language(language._delegate)
        else:
            self._delegate = None

    def set_language(self, language) -> None:
        """Pre-0.22 spelling of the ``language`` setter."""
        self.language = language

    def parse(self, source, old_tree=None, encoding=None):
        """Parse ``source`` bytes into a tree.

        ``old_tree`` is accepted and ignored: the bundled parsers always reparse
        from scratch, which is semantically valid (incremental parsing is an
        optimisation) and is what graphify's call sites already assume.
        """
        if self._delegate is not None:
            return self._delegate.parse(source, old_tree) if old_tree is not None else self._delegate.parse(source)
        if self._language is None or self._language.grammar is None:
            raise ValueError("Parser does not have a language assigned")
        if isinstance(source, str):
            source = source.encode("utf-8")
        return self._language.grammar.parse(source)
