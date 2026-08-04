"""Syntax-tree objects with tree-sitter's node API.

The member set here is not a guess -- it is the surface ``graphify`` actually
touches, measured across the upstream package:

    type 804 · child_by_field_name 302 · parent 208 · start_point 178
    is_named 79 · start_byte 30 · end_byte 25 · text 24 · root_node 24
    walk 11 · next_named_sibling 2 · has_error 1 · children_by_field_name 1
    child_count 1

Notably absent: ``Query`` and the S-expression pattern API. Upstream walks trees
by hand, so nothing here needs a query engine.

Nodes are built once by a parser and then treated as immutable. ``parent`` and
the sibling links are wired up in :func:`link_tree` after construction, which
keeps the parsers free to build children bottom-up without threading a parent
reference through every call.
"""
from __future__ import annotations

__all__ = ["Node", "Tree", "TreeCursor", "link_tree"]


class Node:
    """A single syntax-tree node.

    ``fields`` maps tree-sitter field names (``name``, ``body``, ``function``,
    ``declarator``, ...) to child nodes. Upstream reads these constantly through
    :meth:`child_by_field_name`, and the names must match the real grammars --
    ``graphify/extract.py``'s ``LanguageConfig`` blocks are the reference.
    """

    __slots__ = (
        "type",
        "children",
        "fields",
        "start_byte",
        "end_byte",
        "start_point",
        "end_point",
        "is_named",
        "is_error",
        "parent",
        "_source",
    )

    def __init__(
        self,
        type: str,
        start_byte: int = 0,
        end_byte: int = 0,
        start_point: tuple = (0, 0),
        end_point: tuple = (0, 0),
        children=None,
        fields=None,
        is_named: bool = True,
        source: bytes = b"",
    ) -> None:
        self.type = type
        self.start_byte = start_byte
        self.end_byte = end_byte
        self.start_point = start_point
        self.end_point = end_point
        self.children = children if children is not None else []
        self.fields = fields if fields is not None else {}
        self.is_named = is_named
        self.is_error = False
        self.parent = None
        self._source = source

    # ── text ──────────────────────────────────────────────────────────────
    @property
    def text(self) -> bytes:
        return self._source[self.start_byte:self.end_byte]

    # ── children ──────────────────────────────────────────────────────────
    @property
    def named_children(self) -> list:
        return [c for c in self.children if c.is_named]

    @property
    def child_count(self) -> int:
        return len(self.children)

    @property
    def named_child_count(self) -> int:
        return sum(1 for c in self.children if c.is_named)

    def child(self, index: int):
        try:
            return self.children[index]
        except IndexError:
            return None

    def named_child(self, index: int):
        try:
            return self.named_children[index]
        except IndexError:
            return None

    def child_by_field_name(self, name: str):
        return self.fields.get(name)

    def children_by_field_name(self, name: str) -> list:
        """All children under ``name``.

        tree-sitter allows a field to repeat; :attr:`fields` stores the first
        such child, so repeats are kept in a parallel ``name + "*"`` entry that
        the parsers populate when there is more than one.
        """
        repeated = self.fields.get(name + "*")
        if repeated is not None:
            return list(repeated)
        single = self.fields.get(name)
        return [single] if single is not None else []

    def field_name_for_child(self, index: int):
        target = self.child(index)
        for name, node in self.fields.items():
            if node is target and not name.endswith("*"):
                return name
        return None

    # ── siblings ──────────────────────────────────────────────────────────
    def _sibling(self, offset: int, named_only: bool):
        if self.parent is None:
            return None
        siblings = self.parent.named_children if named_only else self.parent.children
        try:
            position = siblings.index(self)
        except ValueError:
            return None
        target = position + offset
        if 0 <= target < len(siblings):
            return siblings[target]
        return None

    @property
    def next_sibling(self):
        return self._sibling(1, False)

    @property
    def prev_sibling(self):
        return self._sibling(-1, False)

    @property
    def next_named_sibling(self):
        return self._sibling(1, True)

    @property
    def prev_named_sibling(self):
        return self._sibling(-1, True)

    # ── errors ────────────────────────────────────────────────────────────
    @property
    def has_error(self) -> bool:
        """Whether this subtree contains an error node.

        The bundled parsers are tolerant by construction -- they skip what they
        cannot classify rather than emitting error nodes -- so this is normally
        False. It is still computed honestly by walking the subtree so that a
        parser which does mark errors reports them.
        """
        if self.is_error:
            return True
        return any(child.has_error for child in self.children)

    @property
    def is_missing(self) -> bool:
        return False

    @property
    def is_extra(self) -> bool:
        return False

    # ── traversal ─────────────────────────────────────────────────────────
    def walk(self) -> "TreeCursor":
        return TreeCursor(self)

    def descendants(self):
        """Depth-first iteration over this node and everything beneath it."""
        stack = [self]
        while stack:
            node = stack.pop()
            yield node
            stack.extend(reversed(node.children))

    def __repr__(self) -> str:
        return f"<Node type={self.type}, start_point={self.start_point}, end_point={self.end_point}>"

    def __eq__(self, other) -> bool:
        return self is other

    def __hash__(self) -> int:
        return id(self)


class TreeCursor:
    """tree-sitter's stateful cursor over a subtree."""

    __slots__ = ("_node", "_stack")

    def __init__(self, node: Node) -> None:
        self._node = node
        self._stack: list = []

    @property
    def node(self) -> Node:
        return self._node

    @property
    def field_name(self):
        parent = self._node.parent
        if parent is None:
            return None
        for name, child in parent.fields.items():
            if child is self._node and not name.endswith("*"):
                return name
        return None

    def goto_first_child(self) -> bool:
        if not self._node.children:
            return False
        self._stack.append(self._node)
        self._node = self._node.children[0]
        return True

    def goto_next_sibling(self) -> bool:
        sibling = self._node.next_sibling
        if sibling is None:
            return False
        self._node = sibling
        return True

    def goto_parent(self) -> bool:
        if not self._stack:
            return False
        self._node = self._stack.pop()
        return True

    def copy(self) -> "TreeCursor":
        clone = TreeCursor(self._node)
        clone._stack = list(self._stack)
        return clone

    def reset(self, node: Node) -> None:
        self._node = node
        self._stack.clear()


class Tree:
    """Parse result -- a root node plus the source it was parsed from."""

    __slots__ = ("root_node", "text")

    def __init__(self, root_node: Node, source: bytes) -> None:
        self.root_node = root_node
        self.text = source

    def walk(self) -> TreeCursor:
        return self.root_node.walk()

    def edit(self, **_kwargs) -> None:
        """No-op: the bundled parsers always reparse from scratch."""

    def __repr__(self) -> str:
        return f"<Tree root={self.root_node!r}>"


def link_tree(root: Node, source: bytes) -> Node:
    """Attach parents and the shared source buffer across a freshly built tree.

    Done as a post-pass so parsers can build children bottom-up without carrying
    a parent reference around. Iterative rather than recursive: deeply nested
    sources (long chained expressions, deeply indented files) would otherwise be
    able to exhaust the interpreter stack.
    """
    stack = [root]
    while stack:
        node = stack.pop()
        node._source = source
        for child in node.children:
            child.parent = node
            stack.append(child)
    return root
