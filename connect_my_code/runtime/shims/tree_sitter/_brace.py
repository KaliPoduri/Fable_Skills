"""Structural parser for brace-delimited languages.

One token-driven parser, configured per language by :class:`BraceSpec`, covering
the C-like grammars graphify extracts. It recognises the constructs the tool
builds its graph from -- type declarations, functions and methods, imports,
inheritance clauses, and call expressions with their receiver chains -- and
deliberately stops there.

**What this is and is not.** This is not a reimplementation of each tree-sitter
grammar; it is a structural recogniser that emits the node types those grammars
use for the constructs above. Everything it emits is something it has actually
matched in the token stream, so extracted edges are trustworthy. Constructs it
does not model simply produce no node, which costs *recall* in graphify's deeper
inference passes rather than introducing wrong edges. That trade -- fewer edges,
never wrong edges -- is the design rule for this file.

Where a real grammar is installed for a language, the front-end delegates to it
instead and none of this runs.
"""
from __future__ import annotations

from ._lexer import COMMENT, IDENT, NEWLINE, PUNCT, STRING, LexSpec, tokenize
from ._node import Node, Tree, link_tree

__all__ = ["BraceSpec", "parse_brace_language"]

# Keywords that are followed by a parenthesised head and a block, and so would
# otherwise look exactly like a function declaration.
_CONTROL_KEYWORDS = frozenset({
    "if", "else", "for", "while", "switch", "catch", "return", "do", "try",
    "with", "using", "lock", "foreach", "when", "match", "unless", "elif",
    "sizeof", "typeof", "defined", "await", "yield", "throw", "case", "select",
    "go", "defer", "guard", "repeat",
})


class BraceSpec:
    """Per-language configuration for :func:`parse_brace_language`."""

    __slots__ = (
        "name", "lex", "root_type", "identifier_type", "type_identifier_type",
        "class_keywords", "class_body_type", "function_keywords", "function_body_type",
        "method_type", "typed_declarations", "import_keywords", "statement_terminator",
        "call_type", "call_function_field", "new_expression_type", "accessor_type",
        "accessor_field", "accessor_object_field", "argument_list_type",
        "parameters_type", "heritage_style", "modifiers", "field_declaration_type",
        "typed_function_type", "call_style", "new_type_field", "wrapping_keywords",
        "bare_methods", "receiver_before_name", "block_style", "block_openers",
        "line_only_openers", "parenless_calls", "declarator_style",
    )

    def __init__(
        self,
        name,
        lex=None,
        root_type="program",
        identifier_type="identifier",
        type_identifier_type="type_identifier",
        class_keywords=None,
        class_body_type="class_body",
        function_keywords=None,
        function_body_type="statement_block",
        method_type=None,
        typed_declarations=False,
        import_keywords=None,
        statement_terminator=";",
        call_type="call_expression",
        call_function_field="function",
        new_expression_type=None,
        accessor_type="member_expression",
        accessor_field="property",
        accessor_object_field="object",
        argument_list_type="arguments",
        parameters_type="formal_parameters",
        heritage_style=None,
        modifiers=(),
        field_declaration_type=None,
        typed_function_type="function_definition",
        call_style="chain",
        new_type_field="type",
        wrapping_keywords=None,
        bare_methods=False,
        receiver_before_name=False,
        block_style="braces",
        block_openers=(),
        line_only_openers=(),
        parenless_calls=False,
        declarator_style=False,
    ):
        self.name = name
        self.lex = lex or LexSpec()
        self.root_type = root_type
        self.identifier_type = identifier_type
        self.type_identifier_type = type_identifier_type
        self.class_keywords = dict(class_keywords or {})
        self.class_body_type = class_body_type
        self.function_keywords = dict(function_keywords or {})
        self.function_body_type = function_body_type
        self.method_type = method_type
        self.typed_declarations = typed_declarations
        self.import_keywords = dict(import_keywords or {})
        self.statement_terminator = statement_terminator
        self.call_type = call_type
        self.call_function_field = call_function_field
        self.new_expression_type = new_expression_type
        self.accessor_type = accessor_type
        self.accessor_field = accessor_field
        self.accessor_object_field = accessor_object_field
        self.argument_list_type = argument_list_type
        self.parameters_type = parameters_type
        self.heritage_style = heritage_style
        self.modifiers = frozenset(modifiers)
        self.field_declaration_type = field_declaration_type
        self.typed_function_type = typed_function_type
        # "chain": the callee is a receiver chain under one field (JS, C#, PHP).
        # "flat":  the grammar hangs `object` and `name` straight off the call
        #          node with no accessor in between (Java, Groovy).
        self.call_style = call_style
        self.new_type_field = new_type_field
        # Keywords that prefix a declaration rather than forming a statement of
        # their own (`export class Foo {}`). They wrap what follows.
        self.wrapping_keywords = dict(wrapping_keywords or {})
        # Methods declared with no introducing keyword inside a class body
        # (`add(item) { ... }` in JS/TS). Only ever matched inside a class.
        self.bare_methods = bare_methods
        # A parenthesised receiver sits between the keyword and the name
        # (`func (s *Store) Add(...)` in Go).
        self.receiver_before_name = receiver_before_name
        # "braces": bodies are `{ ... }`. "end": bodies run to a matching `end`
        # keyword (Ruby, Lua), which needs keyword counting rather than bracket
        # matching.
        self.block_style = block_style
        self.block_openers = frozenset(block_openers)
        # Openers that only open a block at the start of a line -- Ruby's
        # trailing modifiers (`foo if bar`) must not be counted.
        self.line_only_openers = frozenset(line_only_openers)
        # Accept `recv.method` with no argument list as a call (Ruby).
        self.parenless_calls = parenless_calls
        # C/C++ nest the name and parameters inside a `function_declarator` under
        # the `declarator` field. graphify's _get_c_func_name / _get_cpp_func_name
        # unwrap exactly that chain, so the shape is required, not cosmetic.
        self.declarator_style = declarator_style


class _Parser:
    def __init__(self, source: bytes, spec: BraceSpec) -> None:
        self.source = source
        self.spec = spec
        raw = tokenize(source, spec.lex)
        # Comments and newlines carry no structure in these languages, and
        # dropping them lets the matcher and the declaration patterns below work
        # on a dense stream without repeatedly skipping trivia.
        self.tokens = [t for t in raw if t.kind not in (COMMENT, NEWLINE)]
        self.match = self._match_brackets()

    # ── bracket matching ──────────────────────────────────────────────────
    def _match_brackets(self) -> dict:
        """Index-to-index map between every matched bracket pair.

        Unbalanced brackets are simply left unmatched rather than raising:
        graphify scans whole repositories and must tolerate a truncated or
        syntactically broken file.
        """
        pairs = {"(": ")", "[": "]", "{": "}"}
        stack: list = []
        matched: dict = {}
        for index, token in enumerate(self.tokens):
            if token.kind != PUNCT:
                continue
            if token.text in pairs:
                stack.append((index, pairs[token.text]))
            elif token.text in (")", "]", "}"):
                while stack:
                    open_index, closer = stack.pop()
                    if closer == token.text:
                        matched[open_index] = index
                        matched[index] = open_index
                        break
        return matched

    # ── node helpers ──────────────────────────────────────────────────────
    def _node(self, type_name, first, last, children=None, fields=None) -> Node:
        start = self.tokens[first]
        end = self.tokens[last]
        return Node(
            type_name,
            start_byte=start.start_byte,
            end_byte=end.end_byte,
            start_point=start.start_point,
            end_point=end.end_point,
            children=children or [],
            fields=fields or {},
            is_named=True,
            source=self.source,
        )

    def _leaf(self, type_name, index) -> Node:
        return self._node(type_name, index, index)

    def _anon(self, index) -> Node:
        """An *unnamed* leaf carrying a punctuation token's own text as its type.

        Real tree-sitter puts anonymous tokens in `children` (only
        `named_children` excludes them), and a few graphify passes match on them
        directly -- `_js_export_statement_is_star` looks for a `"*"` child to
        detect `export * from`, and `_kotlin_function_return_type_node` walks for
        the `":"` before a return type. Emitting only named nodes silently
        disabled both, so the tokens those passes need are emitted here.
        """
        token = self.tokens[index]
        node = self._node(token.text, index, index)
        node.is_named = False
        return node

    def _is(self, index, text) -> bool:
        return 0 <= index < len(self.tokens) and self.tokens[index].text == text

    def _ident(self, index) -> bool:
        return 0 <= index < len(self.tokens) and self.tokens[index].kind == IDENT

    # ── entry point ───────────────────────────────────────────────────────
    def parse(self) -> Tree:
        children = self._parse_range(0, len(self.tokens), in_class=False)
        end_row = self.source.count(b"\n")
        last_newline = self.source.rfind(b"\n")
        end_col = len(self.source) - (last_newline + 1)
        root = Node(
            self.spec.root_type,
            start_byte=0,
            end_byte=len(self.source),
            start_point=(0, 0),
            end_point=(end_row, end_col),
            children=children,
            fields={},
            is_named=True,
            source=self.source,
        )
        return Tree(link_tree(root, self.source), self.source)

    # ── statement-range parsing ───────────────────────────────────────────
    def _parse_range(self, lo: int, hi: int, in_class: bool) -> list:
        out: list = []
        index = lo
        while index < hi:
            token = self.tokens[index]

            if token.kind == IDENT:
                handled = self._try_wrapper(index, hi, in_class)
                if handled is None:
                    handled = self._try_import(index, hi)
                if handled is None:
                    handled = self._try_class(index, hi)
                if handled is None:
                    handled = self._try_keyword_function(index, hi, in_class)
                if handled is None and in_class and self.spec.bare_methods:
                    handled = self._try_bare_method(index, hi)
                if handled is not None:
                    node, index = handled
                    if node is not None:
                        out.append(node)
                    continue

            if self.spec.typed_declarations:
                handled = self._try_typed_function(index, hi, in_class)
                if handled is not None:
                    node, index = handled
                    if node is not None:
                        out.append(node)
                    continue

            handled = self._try_expression(index, hi)
            if handled is not None:
                nodes, index = handled
                out.extend(nodes)
                continue

            index += 1
        return out

    # ── wrapping keywords (`export`, `export default`) ────────────────────
    def _try_wrapper(self, index: int, hi: int, in_class: bool):
        """Wrap a declaration introduced by a prefix keyword.

        tree-sitter-javascript nests the declaration inside ``export_statement``
        rather than replacing it, so ``export class Foo {}`` must still yield a
        ``class_declaration``. Consuming the statement instead --- which is what
        treating ``export`` as an import keyword did --- silently dropped every
        exported class and function in a module.
        """
        node_type = self.spec.wrapping_keywords.get(self.tokens[index].text)
        if node_type is None:
            return None
        inner_index = index + 1
        while inner_index < hi and self._ident(inner_index) and self.tokens[inner_index].text == "default":
            inner_index += 1

        inner = None
        next_index = index + 1
        if inner_index < hi:
            result = self._try_class(inner_index, hi)
            if result is None:
                result = self._try_keyword_function(inner_index, hi, in_class)
            if result is None and self.spec.typed_declarations:
                result = self._try_typed_function(inner_index, hi, in_class)
            if result is not None:
                inner, next_index = result

        if inner is None:
            # `export { a, b }` / `export * from './x'` -- no declaration to wrap.
            end = self._statement_end(index, hi)
            children = []
            for p in range(index + 1, end + 1):
                token = self.tokens[p]
                if token.kind == IDENT:
                    children.append(self._leaf(self.spec.identifier_type, p))
                elif token.kind == STRING:
                    children.append(self._leaf("string", p))
                elif token.kind == PUNCT and token.text == "*":
                    children.append(self._anon(p))
            return self._node(node_type, index, end, children=children), end + 1

        wrapper = self._node(
            node_type, index, next_index - 1, children=[inner], fields={"declaration": inner}
        )
        return wrapper, next_index

    # ── bare methods in a class body ──────────────────────────────────────
    def _try_bare_method(self, index: int, hi: int):
        """Match ``name(params) [: Type] { ... }`` inside a class body.

        JS and TS declare methods with no introducing keyword. This is gated on
        being inside a class body so a top-level labelled block cannot be
        mistaken for a declaration.
        """
        token = self.tokens[index]
        if token.text in _CONTROL_KEYWORDS or token.text in self.spec.modifiers:
            return None
        if not self._is(index + 1, "("):
            return None
        close = self.match.get(index + 1)
        if close is None:
            return None
        brace = self._body_brace_after_params(close, hi)
        if brace is None:
            return None
        node_type = self.spec.method_type or "method_definition"
        return self._build_function(node_type, index, index, hi, params_open=index + 1, brace=brace)

    # ── imports ───────────────────────────────────────────────────────────
    def _try_import(self, index: int, hi: int):
        node_type = self.spec.import_keywords.get(self.tokens[index].text)
        if node_type is None:
            return None
        # `import` is only a declaration at the start of a statement; inside an
        # expression (`await import(x)`) it is a call, handled elsewhere.
        if self._is(index + 1, "("):
            return None
        end = self._statement_end(index, hi)
        children = []
        for position in range(index + 1, end + 1):
            token = self.tokens[position]
            if token.kind == IDENT:
                children.append(self._leaf(self.spec.identifier_type, position))
            elif token.kind == STRING:
                children.append(self._leaf("string", position))
        return self._node(node_type, index, end, children=children), end + 1

    def _statement_end(self, index: int, hi: int) -> int:
        """Index of the last token of the statement beginning at ``index``."""
        terminator = self.spec.statement_terminator
        position = index
        start_row = self.tokens[index].row
        while position < hi:
            token = self.tokens[position]
            if terminator and token.kind == PUNCT and token.text == terminator:
                return position
            if token.kind == PUNCT and token.text == "{":
                return max(index, position - 1)
            # Without an explicit terminator, a statement ends at the line end.
            if not terminator and token.row > start_row:
                return max(index, position - 1)
            if terminator and token.row > start_row and self.tokens[position - 1].kind != PUNCT:
                # Defensive: a missing `;` must not swallow the rest of the file.
                if token.kind == IDENT and token.text in self.spec.import_keywords:
                    return position - 1
            position += 1
        return hi - 1

    # ── type declarations ─────────────────────────────────────────────────
    def _try_class(self, index: int, hi: int):
        node_type = self.spec.class_keywords.get(self.tokens[index].text)
        if node_type is None:
            return None
        name_index = index + 1
        while name_index < hi and not self._ident(name_index):
            if self.tokens[name_index].kind == PUNCT and self.tokens[name_index].text in "{;":
                break
            name_index += 1
        if not self._ident(name_index):
            return None

        brace = self._find_body_brace(name_index, hi)
        if brace is None:
            return None
        close = self._body_close(brace, hi)
        if close is None:
            return None

        name_node = self._leaf(self.spec.identifier_type, name_index)
        # For brace languages `brace` is the `{` that follows the bases, so an
        # exclusive end is right. For `end`-delimited languages it is the last
        # header token -- often the base class itself -- which must be included.
        heritage_end = brace + 1 if self.spec.block_style == "end" else brace
        heritage = self._parse_heritage(name_index + 1, heritage_end)
        body_children = self._parse_range(brace + 1, close, in_class=True)
        body = self._node(self.spec.class_body_type, brace, close, children=body_children)

        fields = {"name": name_node, "body": body}
        children = [name_node]
        for field_name, node in heritage:
            if field_name:
                fields.setdefault(field_name, node)
            children.append(node)
        children.append(body)
        return self._node(node_type, index, close, children=children, fields=fields), close + 1

    def _find_body_brace(self, start: int, hi: int):
        """Index opening the declaration body, or None if there is no body.

        For brace languages this is the ``{``. For ``end``-delimited languages
        (Ruby, Lua) there is no opening token, so the header's last index is
        returned and :meth:`_body_close` finds the matching ``end``.
        """
        if self.spec.block_style == "end":
            return self._header_end(start, hi)
        position = start
        while position < hi:
            token = self.tokens[position]
            if token.kind == PUNCT:
                if token.text == "{":
                    return position
                if token.text == ";":
                    return None
                if token.text in "([":
                    close = self.match.get(position)
                    if close is None:
                        return None
                    position = close
            position += 1
        return None

    def _header_end(self, start: int, hi: int):
        """Last index of a declaration header in an ``end``-delimited language.

        ``start`` is the last token consumed from the header so far (the
        declaration's name, or its closing paren). The header runs to the end of
        that token's line, stepping over a parameter list that wraps across
        lines. Anchoring the row to ``start`` rather than to the following token
        is what keeps the body from starting one token late and swallowing the
        first statement.
        """
        if start >= hi:
            return None
        row = self.tokens[start].row
        position = start
        while position + 1 < hi:
            following = self.tokens[position + 1]
            if following.kind == PUNCT and following.text == "(":
                close = self.match.get(position + 1)
                if close is None:
                    break
                position = close
                continue
            if following.row > row:
                break
            position += 1
        return position

    def _body_close(self, open_index: int, hi: int):
        """Index closing the body opened at ``open_index``."""
        if self.spec.block_style != "end":
            return self.match.get(open_index)
        depth = 1
        position = open_index + 1
        while position < hi:
            token = self.tokens[position]
            if token.kind == IDENT:
                if token.text == "end":
                    depth -= 1
                    if depth == 0:
                        return position
                elif token.text in self.spec.block_openers:
                    depth += 1
                elif token.text in self.spec.line_only_openers and self._starts_line(position):
                    # `x = 1 if cond` is a modifier, not a block opener; only a
                    # line-initial `if`/`while`/`unless` opens one.
                    depth += 1
            position += 1
        return None

    def _starts_line(self, index: int) -> bool:
        return index == 0 or self.tokens[index - 1].row < self.tokens[index].row

    def _parse_heritage(self, start: int, end: int) -> list:
        """Inheritance clause nodes, shaped per the language's real grammar.

        graphify reads a different structure for each language --- Java's
        ``superclass``/``interfaces`` fields, C#'s ``base_list`` child, PHP's
        ``base_clause``/``class_interface_clause`` --- so each style is built to
        match rather than normalised into a common shape.
        """
        style = self.spec.heritage_style
        if style is None:
            return []
        names = []
        position = start
        mode = None
        while position < end:
            token = self.tokens[position]
            if token.kind == IDENT and token.text in ("extends", "implements", "with"):
                mode = "implements" if token.text == "implements" else "inherits"
                position += 1
                continue
            if token.kind == PUNCT and token.text in (":", "<"):
                # `:` for C#/C++/Kotlin, `<` for Ruby.
                mode = mode or "inherits"
                position += 1
                continue
            if token.kind == PUNCT and token.text in "([<":
                close = self.match.get(position)
                position = (close + 1) if close is not None else position + 1
                continue
            if token.kind == IDENT and mode is not None and token.text not in self.spec.modifiers:
                names.append((mode, position))
                # A qualified name (`a.b.C`) contributes one entry.
                while self._is(position + 1, ".") and self._ident(position + 2):
                    position += 2
            position += 1

        if not names:
            return []

        if style == "java":
            out = []
            supers = [p for mode, p in names if mode == "inherits"]
            interfaces = [p for mode, p in names if mode == "implements"]
            if supers:
                inner = self._leaf(self.spec.type_identifier_type, supers[0])
                out.append(("superclass", self._node("superclass", supers[0], supers[0], children=[inner])))
            if interfaces:
                type_children = [self._leaf(self.spec.type_identifier_type, p) for p in interfaces]
                type_list = self._node("type_list", interfaces[0], interfaces[-1], children=type_children)
                out.append(("interfaces", self._node("interfaces", interfaces[0], interfaces[-1], children=[type_list])))
            return out

        if style == "csharp":
            positions = [p for _mode, p in names]
            children = [self._leaf(self.spec.identifier_type, p) for p in positions]
            return [(None, self._node("base_list", positions[0], positions[-1], children=children))]

        if style == "php":
            out = []
            supers = [p for mode, p in names if mode == "inherits"]
            interfaces = [p for mode, p in names if mode == "implements"]
            if supers:
                out.append((None, self._node("base_clause", supers[0], supers[-1],
                                             children=[self._leaf("name", p) for p in supers])))
            if interfaces:
                out.append((None, self._node("class_interface_clause", interfaces[0], interfaces[-1],
                                             children=[self._leaf("name", p) for p in interfaces])))
            return out

        if style == "scala":
            positions = [p for _mode, p in names]
            children = [self._leaf(self.spec.type_identifier_type, p) for p in positions]
            return [(None, self._node("extends_clause", positions[0], positions[-1], children=children))]

        if style == "ruby":
            position = names[0][1]
            return [("superclass", self._node("superclass", position, position,
                                              children=[self._leaf("constant", position)]))]

        # Default (JS/TS, Kotlin, Swift, Go): a heritage node listing the bases.
        positions = [p for _mode, p in names]
        children = [self._leaf(self.spec.type_identifier_type, p) for p in positions]
        return [(None, self._node("class_heritage", positions[0], positions[-1], children=children))]

    # ── functions ─────────────────────────────────────────────────────────
    def _try_keyword_function(self, index: int, hi: int, in_class: bool):
        node_type = self.spec.function_keywords.get(self.tokens[index].text)
        if node_type is None:
            return None
        name_index = index + 1
        # Go puts a parenthesised receiver between `func` and the method name;
        # skipping it is what turns `func (s *Store) Add(...)` into a declaration
        # named Add rather than an unparsed statement.
        if self.spec.receiver_before_name and self._is(name_index, "("):
            close = self.match.get(name_index)
            if close is not None:
                name_index = close + 1
        while name_index < hi and not self._ident(name_index):
            token = self.tokens[name_index]
            if token.kind == PUNCT and token.text in "{;=":
                break
            if token.kind == PUNCT and token.text == "(":
                break
            name_index += 1
        if not self._ident(name_index):
            return None
        if in_class and self.spec.method_type:
            node_type = self.spec.method_type
        return self._build_function(node_type, index, name_index, hi)

    def _try_typed_function(self, index: int, hi: int, in_class: bool):
        """Match ``[modifiers] [Type] name(params) {`` -- Java, C, C++, C#.

        These languages declare functions with no introducing keyword, so the
        shape has to be recognised: an identifier, a balanced parameter list, and
        a body brace with only declaration trivia (``const``, ``throws X``,
        ``noexcept``, a C++ initialiser list) in between.
        """
        if not self._ident(index):
            return None
        token = self.tokens[index]
        if token.text in _CONTROL_KEYWORDS or token.text in self.spec.class_keywords:
            return None
        if self._is(index - 1, ".") or self._is(index - 1, "new"):
            return None
        if not self._is(index + 1, "("):
            return None
        close = self.match.get(index + 1)
        if close is None:
            return None
        brace = self._body_brace_after_params(close, hi)
        if brace is None:
            return None
        # A bare `name(...) {` at top level with nothing before it is a call
        # followed by a block, not a declaration -- require a preceding type or
        # modifier token on the same logical statement.
        previous = self.tokens[index - 1] if index > 0 else None
        if previous is None or previous.kind not in (IDENT, PUNCT):
            return None
        if previous.kind == PUNCT and previous.text not in (">", "]", "*", "&", "}", ";", ")"):
            return None
        node_type = (
            self.spec.method_type
            if (in_class and self.spec.method_type)
            else self.spec.typed_function_type
        )
        return self._build_function(node_type, index, index, hi, params_open=index + 1, brace=brace)

    def _body_brace_after_params(self, close: int, hi: int):
        """The ``{`` following a parameter list, or None if this is a prototype."""
        position = close + 1
        while position < hi:
            token = self.tokens[position]
            if token.kind == PUNCT:
                if token.text == "{":
                    return position
                if token.text in ";=":
                    return None
                if token.text in "([<":
                    nested = self.match.get(position)
                    if nested is None:
                        return None
                    position = nested + 1
                    continue
                if token.text in (":", ",", "*", "&", "-", ">"):
                    position += 1
                    continue
                return None
            elif token.kind == IDENT:
                position += 1
                continue
            else:
                return None
        return None

    def _build_function(self, node_type, start, name_index, hi, params_open=None, brace=None):
        if params_open is None:
            params_open = name_index + 1
            while params_open < hi and not self._is(params_open, "("):
                token = self.tokens[params_open]
                if token.kind == PUNCT and token.text in "{;=":
                    break
                params_open += 1
        params_close = self.match.get(params_open) if self._is(params_open, "(") else None

        if brace is None:
            # Pass the last header token itself, not the one after it: for
            # `end`-delimited languages the body's extent is derived from that
            # token's line.
            search_from = params_close if params_close is not None else name_index
            brace = self._find_body_brace(search_from, hi)
        if brace is None:
            # Abstract/interface method: emit the declaration with no body so it
            # still becomes a node, and resume after the statement.
            end = self._statement_end(name_index, hi)
            name_node = self._leaf(self.spec.identifier_type, name_index)
            return self._node(node_type, start, end, children=[name_node],
                              fields={"name": name_node}), end + 1
        close = self._body_close(brace, hi)
        if close is None:
            return None

        name_node = self._leaf(self.spec.identifier_type, name_index)
        children = [name_node]
        fields = {"name": name_node}
        params = None

        if params_close is not None:
            param_children = self._parse_parameters(params_open + 1, params_close)
            params = self._node(self.spec.parameters_type, params_open, params_close,
                                children=param_children)
            fields["parameters"] = params
            children.append(params)

        if self.spec.declarator_style:
            # Wrap name + parameters in the `function_declarator` that C/C++
            # name resolution walks down through.
            declarator_children = [name_node] + ([params] if params is not None else [])
            declarator = self._node(
                "function_declarator", name_index,
                params_close if params_close is not None else name_index,
                children=declarator_children,
                fields={"declarator": name_node,
                        **({"parameters": params} if params is not None else {})},
            )
            fields["declarator"] = declarator
            children = [declarator]

        if params_close is not None:
            # A `:` between the parameter list and the body introduces a return
            # type. Kotlin's return-type resolver scans children for exactly that
            # colon, so it is emitted as an anonymous child followed by the type.
            for position in range(params_close + 1, brace):
                token = self.tokens[position]
                if token.kind == PUNCT and token.text == ":":
                    children.append(self._anon(position))
                    for after in range(position + 1, brace):
                        if self.tokens[after].kind == IDENT:
                            type_node = self._leaf(self.spec.type_identifier_type, after)
                            fields.setdefault("return_type", type_node)
                            children.append(type_node)
                            break
                    break

        body_children = self._parse_range(brace + 1, close, in_class=False)
        body = self._node(self.spec.function_body_type, brace, close, children=body_children)
        fields["body"] = body
        children.append(body)
        return self._node(node_type, start, close, children=children, fields=fields), close + 1

    def _parse_parameters(self, lo: int, hi: int) -> list:
        """Parameter nodes, one per comma-separated group.

        The bound name is the last identifier before the group's ``=``, ``:`` or
        end -- which is where it sits in both ``Type name`` and ``name: Type``
        orderings, so one rule serves every language here.
        """
        out = []
        depth = 0
        group: list = []
        for position in range(lo, hi):
            token = self.tokens[position]
            if token.kind == PUNCT and token.text in "([{<":
                depth += 1
            elif token.kind == PUNCT and token.text in ")]}>":
                depth -= 1
            if depth == 0 and token.kind == PUNCT and token.text == ",":
                if group:
                    out.append(self._parameter_node(group))
                group = []
                continue
            group.append(position)
        if group:
            out.append(self._parameter_node(group))
        return [n for n in out if n is not None]

    def _parameter_node(self, group: list):
        name_index = None
        for position in group:
            token = self.tokens[position]
            if token.kind == IDENT:
                name_index = position
            elif token.kind == PUNCT and token.text in "=:":
                break
        if name_index is None:
            return None
        name_node = self._leaf(self.spec.identifier_type, name_index)
        type_children = [
            self._leaf(self.spec.type_identifier_type, p)
            for p in group
            if p != name_index and self.tokens[p].kind == IDENT
        ]
        children = [name_node] + type_children
        return self._node("parameter", group[0], group[-1], children=children,
                          fields={"name": name_node})

    # ── expressions and calls ─────────────────────────────────────────────
    def _try_expression(self, index: int, hi: int):
        """Parse a receiver chain and any calls hanging off it."""
        token = self.tokens[index]

        if self.spec.new_expression_type and token.kind == IDENT and token.text == "new":
            chain_end, chain = self._parse_chain(index + 1, hi)
            if chain is None:
                return None
            if self._is(chain_end, "("):
                close = self.match.get(chain_end)
                if close is None:
                    return None
                arguments, inner = self._argument_list(chain_end, close)
                # Grammars disagree on the field naming the constructed type:
                # JS `new_expression` uses `constructor`, Java
                # `object_creation_expression` uses `type`. Set both, plus the
                # language's call field, so every reader finds it.
                node = self._node(
                    self.spec.new_expression_type, index, close,
                    children=[chain, arguments] + inner,
                    fields={
                        self.spec.call_function_field: chain,
                        self.spec.new_type_field: chain,
                        "constructor": chain,
                        "arguments": arguments,
                    },
                )
                return [node], close + 1
            return [chain], chain_end

        if token.kind != IDENT:
            return None
        if token.text in _CONTROL_KEYWORDS:
            return None
        if self._is(index - 1, "."):
            return None    # mid-chain; the chain's head already consumed it

        chain_end, chain = self._parse_chain(index, hi)
        if chain is None:
            return None

        nodes: list = []
        current = chain
        position = chain_end
        produced_call = False
        while self._is(position, "("):
            close = self.match.get(position)
            if close is None:
                break
            arguments, inner = self._argument_list(position, close)
            call = self._node(
                self.spec.call_type, index, close,
                children=[current, arguments] + inner,
                fields=self._call_fields(current, arguments),
            )
            produced_call = True
            current = call
            position = close + 1
            # A chained continuation: `.then(...)`, `.map(...)`.
            if self._is(position, ".") and self._ident(position + 1):
                property_node = self._leaf(self.spec.identifier_type, position + 1)
                current = self._node(
                    self.spec.accessor_type, index, position + 1,
                    children=[current, property_node],
                    fields={
                        self.spec.accessor_field: property_node,
                        self.spec.accessor_object_field: current,
                    },
                )
                position += 2

        if not produced_call:
            if not (self.spec.parenless_calls and current.type == self.spec.accessor_type):
                return None
            # Ruby routinely calls without parentheses (`prepare`, `obj.run`).
            # Only receiver-qualified chains are accepted here -- a bare
            # identifier is far more often a variable read. graphify resolves
            # the callee name against declared labels anyway, so an unmatched
            # name produces no edge.
            empty = self._node(self.spec.argument_list_type, position - 1, position - 1)
            current = self._node(
                self.spec.call_type, index, position - 1,
                children=[current, empty],
                fields=self._call_fields(current, empty),
            )
        nodes.append(current)
        return nodes, position

    def _call_fields(self, callee: Node, arguments: Node) -> dict:
        """Fields for a call node, in the shape this language's grammar uses.

        Java and Groovy hang ``object`` and ``name`` straight off
        ``method_invocation`` with no accessor node in between --- which is why
        their ``LanguageConfig`` sets ``call_function_field="name"`` and leaves
        ``call_accessor_node_types`` empty. Everything else nests a receiver
        chain under a single field.
        """
        fields = {"arguments": arguments}
        if self.spec.call_style == "flat" and callee.type == self.spec.accessor_type:
            fields["name"] = callee.fields[self.spec.accessor_field]
            fields["object"] = callee.fields[self.spec.accessor_object_field]
        else:
            fields[self.spec.call_function_field] = callee
        return fields

    def _parse_chain(self, index: int, hi: int):
        """Parse ``a``, ``a.b``, ``a.b.c`` into identifier/accessor nodes."""
        if not self._ident(index) or index >= hi:
            return index, None
        node = self._leaf(self.spec.identifier_type, index)
        position = index + 1
        start = index
        while (self._is(position, ".") or self._is(position, "::")) and self._ident(position + 1):
            property_node = self._leaf(self.spec.identifier_type, position + 1)
            node = self._node(
                self.spec.accessor_type, start, position + 1,
                children=[node, property_node],
                fields={
                    self.spec.accessor_field: property_node,
                    self.spec.accessor_object_field: node,
                },
            )
            position += 2
        return position, node

    def _argument_list(self, open_index: int, close_index: int):
        """The ``arguments`` node plus any calls nested inside it."""
        inner = self._parse_range(open_index + 1, close_index, in_class=False)
        arguments = self._node(self.spec.argument_list_type, open_index, close_index,
                               children=list(inner))
        # The nested nodes live under `arguments`; returning an empty extra list
        # keeps them from being attached to the call twice.
        return arguments, []


def parse_brace_language(source: bytes, spec: BraceSpec) -> Tree:
    """Parse ``source`` with ``spec`` into a tree-sitter-shaped tree."""
    return _Parser(source, spec).parse()
