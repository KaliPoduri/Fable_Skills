"""Python parser producing a tree-sitter-python-shaped tree.

Rather than reimplementing a Python grammar, this adapts CPython's own
:mod:`ast` -- so the *parse* is exact by construction, and the only work is
translating node names and positions into what tree-sitter-python would have
produced.

Position translation is exact too. Since Python 3.8, ``ast`` reports
``col_offset`` as a UTF-8 **byte** offset within its line, which is the same
unit tree-sitter uses for ``start_point``'s column and for ``start_byte``. A
table of line-start byte offsets converts between them without any re-encoding.

The vocabulary reproduced here is the one ``graphify/extractors/engine.py``
actually inspects -- ``typed_parameter``, ``list_splat_pattern``, ``generic_type``
vs ``subscript``, the ``type`` annotation wrapper, ``with_clause``/``with_item``,
``named_expression`` and the rest. Fidelity target is the real grammar, not
graphify's current reads: upstream is written against real tree-sitter, so
matching the grammar is what keeps a future upstream sync working.
"""
from __future__ import annotations

import ast

from ._node import Node, Tree, link_tree

# Nodes tree-sitter-python treats as scope boundaries or statements, kept in one
# place so the mapping below stays declarative.
_BOOL_LITERALS = {True: "true", False: "false"}


class _Builder:
    """Translates one CPython AST into tree-sitter-shaped nodes."""

    def __init__(self, source: bytes) -> None:
        self.source = source
        # Byte offset at which each line starts; index is the 0-based line number.
        self.line_starts = [0]
        for index, byte in enumerate(source):
            if byte == 0x0A:
                self.line_starts.append(index + 1)

    # ── position helpers ──────────────────────────────────────────────────
    def _byte(self, lineno: int, col: int) -> int:
        line_index = lineno - 1
        if line_index < 0:
            return 0
        if line_index >= len(self.line_starts):
            return len(self.source)
        return min(self.line_starts[line_index] + col, len(self.source))

    def _span(self, node):
        """(start_byte, end_byte, start_point, end_point) for an AST node."""
        start_line = getattr(node, "lineno", 1)
        start_col = getattr(node, "col_offset", 0)
        end_line = getattr(node, "end_lineno", None) or start_line
        end_col = getattr(node, "end_col_offset", None)
        if end_col is None:
            end_col = start_col
        return (
            self._byte(start_line, start_col),
            self._byte(end_line, end_col),
            (start_line - 1, start_col),
            (end_line - 1, end_col),
        )

    def node(self, type_name: str, ast_node, children=None, fields=None, is_named=True) -> Node:
        start_byte, end_byte, start_point, end_point = self._span(ast_node)
        return Node(
            type_name,
            start_byte=start_byte,
            end_byte=end_byte,
            start_point=start_point,
            end_point=end_point,
            children=children or [],
            fields=fields or {},
            is_named=is_named,
            source=self.source,
        )

    def synthetic(self, type_name: str, start, end, children=None, fields=None) -> Node:
        """A node spanning an explicit byte range -- for constructs ``ast`` has no
        node for, such as the ``block`` wrapping a suite of statements."""
        start_byte, start_point = start
        end_byte, end_point = end
        return Node(
            type_name,
            start_byte=start_byte,
            end_byte=end_byte,
            start_point=start_point,
            end_point=end_point,
            children=children or [],
            fields=fields or {},
            is_named=True,
            source=self.source,
        )

    def identifier(self, name: str, ast_node, *, offset: int = 0) -> Node:
        """An ``identifier`` node.

        ``ast`` does not give positions for bare name strings (a ``ClassDef``'s
        ``name``, an attribute's ``attr``), so the span is reconstructed by
        locating the text within the owning node's source range. Falling back to
        the owner's start keeps offsets monotonic when the search misses.
        """
        start_byte, end_byte, start_point, end_point = self._span(ast_node)
        encoded = name.encode("utf-8")
        found = self.source.find(encoded, start_byte + offset, end_byte)
        if found == -1:
            found = start_byte
        return self._at_byte("identifier", found, len(encoded))

    def _at_byte(self, type_name: str, start_byte: int, length: int) -> Node:
        row, col = self._point_for(start_byte)
        end_byte = start_byte + length
        end_row, end_col = self._point_for(end_byte)
        return Node(
            type_name,
            start_byte=start_byte,
            end_byte=end_byte,
            start_point=(row, col),
            end_point=(end_row, end_col),
            children=[],
            fields={},
            is_named=True,
            source=self.source,
        )

    def _point_for(self, byte_offset: int) -> tuple:
        """Binary-search the line table for the (row, column) of a byte offset."""
        low, high = 0, len(self.line_starts) - 1
        while low < high:
            mid = (low + high + 1) // 2
            if self.line_starts[mid] <= byte_offset:
                low = mid
            else:
                high = mid - 1
        return (low, byte_offset - self.line_starts[low])

    # ── suites ────────────────────────────────────────────────────────────
    def block(self, body: list, owner) -> Node:
        """The ``block`` node tree-sitter puts around an indented suite."""
        children = [self.statement(stmt) for stmt in body]
        children = [c for c in children if c is not None]
        if children:
            start = (children[0].start_byte, children[0].start_point)
            end = (children[-1].end_byte, children[-1].end_point)
        else:
            _s, end_byte, _sp, end_point = self._span(owner)
            start, end = (end_byte, end_point), (end_byte, end_point)
        return self.synthetic("block", start, end, children=children)

    # ── statements ────────────────────────────────────────────────────────
    def statement(self, stmt):
        handler = getattr(self, "_stmt_" + type(stmt).__name__, None)
        if handler is not None:
            return handler(stmt)
        # Unknown statement: still descend so nested calls are discoverable.
        return self.node(_snake(type(stmt).__name__), stmt, children=self._child_exprs(stmt))

    def _decorate(self, definition: Node, stmt):
        """Wrap a decorated definition the way tree-sitter-python does."""
        if not getattr(stmt, "decorator_list", None):
            return definition
        decorators = [
            self.node("decorator", dec, children=[self.expression(dec)])
            for dec in stmt.decorator_list
        ]
        children = decorators + [definition]
        start = (children[0].start_byte, children[0].start_point)
        end = (definition.end_byte, definition.end_point)
        return self.synthetic(
            "decorated_definition", start, end, children=children, fields={"definition": definition}
        )

    def _stmt_FunctionDef(self, stmt):
        name_node = self.identifier(stmt.name, stmt)
        params = self.parameters(stmt.args, stmt)
        body = self.block(stmt.body, stmt)
        fields = {"name": name_node, "parameters": params, "body": body}
        children = [name_node, params]
        if stmt.returns is not None:
            return_type = self.type_node(stmt.returns)
            fields["return_type"] = return_type
            children.append(return_type)
        children.append(body)
        definition = self.node("function_definition", stmt, children=children, fields=fields)
        return self._decorate(definition, stmt)

    _stmt_AsyncFunctionDef = _stmt_FunctionDef

    def _stmt_ClassDef(self, stmt):
        name_node = self.identifier(stmt.name, stmt)
        children = [name_node]
        fields = {"name": name_node}
        if stmt.bases or stmt.keywords:
            base_children = [self.expression(b) for b in stmt.bases]
            base_children += [
                self.node("keyword_argument", kw.value, children=[self.expression(kw.value)])
                for kw in stmt.keywords
            ]
            if base_children:
                start = (base_children[0].start_byte, base_children[0].start_point)
                end = (base_children[-1].end_byte, base_children[-1].end_point)
                superclasses = self.synthetic("argument_list", start, end, children=base_children)
                fields["superclasses"] = superclasses
                children.append(superclasses)
        body = self.block(stmt.body, stmt)
        fields["body"] = body
        children.append(body)
        definition = self.node("class_definition", stmt, children=children, fields=fields)
        return self._decorate(definition, stmt)

    def _stmt_Import(self, stmt):
        children = []
        for alias in stmt.names:
            dotted = self._dotted_name(alias.name, stmt)
            if alias.asname:
                children.append(
                    self.node("aliased_import", stmt, children=[dotted, self.identifier(alias.asname, stmt)])
                )
            else:
                children.append(dotted)
        return self.node("import_statement", stmt, children=children)

    def _stmt_ImportFrom(self, stmt):
        children = []
        fields = {}
        if stmt.level:
            module_text = "." * stmt.level + (stmt.module or "")
            module_node = self.node("relative_import", stmt, children=[])
            module_node.type = "relative_import"
            module_node.end_byte = module_node.start_byte + len(module_text.encode())
        elif stmt.module:
            module_node = self._dotted_name(stmt.module, stmt)
        else:
            module_node = None
        if module_node is not None:
            fields["module_name"] = module_node
            children.append(module_node)

        imported = []
        for alias in stmt.names:
            if alias.name == "*":
                continue
            name_node = self._dotted_name(alias.name, stmt, after=children[-1] if children else None)
            imported.append(name_node)
            if alias.asname:
                children.append(
                    self.node(
                        "aliased_import", stmt, children=[name_node, self.identifier(alias.asname, stmt)]
                    )
                )
            else:
                children.append(name_node)
        if imported:
            fields["name"] = imported[0]
            fields["name*"] = imported
        return self.node("import_from_statement", stmt, children=children, fields=fields)

    def _dotted_name(self, dotted: str, owner, after=None) -> Node:
        start_byte, end_byte, _sp, _ep = self._span(owner)
        search_from = after.end_byte if after is not None else start_byte
        encoded = dotted.encode("utf-8")
        found = self.source.find(encoded, search_from, end_byte)
        if found == -1:
            found = self.source.find(encoded, start_byte, end_byte)
        if found == -1:
            found = start_byte
        node = self._at_byte("dotted_name", found, len(encoded))
        cursor = found
        for part in dotted.split("."):
            node.children.append(self._at_byte("identifier", cursor, len(part.encode())))
            cursor += len(part.encode()) + 1
        return node

    def _stmt_Assign(self, stmt):
        left = self.pattern(stmt.targets[0]) if stmt.targets else None
        right = self.expression(stmt.value)
        children = [c for c in (left, right) if c is not None]
        fields = {}
        if left is not None:
            fields["left"] = left
        fields["right"] = right
        assignment = self.node("assignment", stmt, children=children, fields=fields)
        return self.node("expression_statement", stmt, children=[assignment])

    def _stmt_AnnAssign(self, stmt):
        left = self.pattern(stmt.target)
        annotation = self.type_node(stmt.annotation)
        children = [left, annotation]
        fields = {"left": left, "type": annotation}
        if stmt.value is not None:
            right = self.expression(stmt.value)
            fields["right"] = right
            children.append(right)
        assignment = self.node("assignment", stmt, children=children, fields=fields)
        return self.node("expression_statement", stmt, children=[assignment])

    def _stmt_AugAssign(self, stmt):
        left = self.pattern(stmt.target)
        right = self.expression(stmt.value)
        assignment = self.node(
            "augmented_assignment", stmt, children=[left, right], fields={"left": left, "right": right}
        )
        return self.node("expression_statement", stmt, children=[assignment])

    def _stmt_Expr(self, stmt):
        return self.node("expression_statement", stmt, children=[self.expression(stmt.value)])

    def _stmt_Return(self, stmt):
        children = [self.expression(stmt.value)] if stmt.value is not None else []
        return self.node("return_statement", stmt, children=children)

    def _stmt_For(self, stmt):
        left = self.pattern(stmt.target)
        right = self.expression(stmt.iter)
        body = self.block(stmt.body, stmt)
        children = [left, right, body]
        fields = {"left": left, "right": right, "body": body}
        if stmt.orelse:
            alternative = self.block(stmt.orelse, stmt)
            children.append(alternative)
            fields["alternative"] = alternative
        return self.node("for_statement", stmt, children=children, fields=fields)

    _stmt_AsyncFor = _stmt_For

    def _stmt_While(self, stmt):
        condition = self.expression(stmt.test)
        body = self.block(stmt.body, stmt)
        return self.node(
            "while_statement", stmt, children=[condition, body], fields={"condition": condition, "body": body}
        )

    def _stmt_If(self, stmt):
        condition = self.expression(stmt.test)
        body = self.block(stmt.body, stmt)
        children = [condition, body]
        fields = {"condition": condition, "body": body}
        if stmt.orelse:
            alternative = self.block(stmt.orelse, stmt)
            children.append(alternative)
            fields["alternative"] = alternative
        return self.node("if_statement", stmt, children=children, fields=fields)

    def _stmt_With(self, stmt):
        items = []
        for item in stmt.items:
            value = self.expression(item.context_expr)
            item_children = [value]
            item_fields = {"value": value}
            if item.optional_vars is not None:
                alias = self.pattern(item.optional_vars)
                item_fields["alias"] = alias
                item_children.append(alias)
            items.append(
                self.node("with_item", item.context_expr, children=item_children, fields=item_fields)
            )
        if items:
            start = (items[0].start_byte, items[0].start_point)
            end = (items[-1].end_byte, items[-1].end_point)
            clause = self.synthetic("with_clause", start, end, children=items)
            children = [clause]
        else:
            children = []
        body = self.block(stmt.body, stmt)
        children.append(body)
        return self.node("with_statement", stmt, children=children, fields={"body": body})

    _stmt_AsyncWith = _stmt_With

    def _stmt_Try(self, stmt):
        children = [self.block(stmt.body, stmt)]
        for handler in stmt.handlers:
            handler_children = []
            if handler.type is not None:
                handler_children.append(self.expression(handler.type))
            handler_children.append(self.block(handler.body, handler))
            children.append(self.node("except_clause", handler, children=handler_children))
        if stmt.orelse:
            children.append(self.node("else_clause", stmt, children=[self.block(stmt.orelse, stmt)]))
        if stmt.finalbody:
            children.append(self.node("finally_clause", stmt, children=[self.block(stmt.finalbody, stmt)]))
        return self.node("try_statement", stmt, children=children)

    _stmt_TryStar = _stmt_Try

    def _stmt_Raise(self, stmt):
        children = [self.expression(e) for e in (stmt.exc, stmt.cause) if e is not None]
        return self.node("raise_statement", stmt, children=children)

    def _stmt_Delete(self, stmt):
        return self.node("delete_statement", stmt, children=[self.expression(t) for t in stmt.targets])

    def _stmt_Assert(self, stmt):
        children = [self.expression(e) for e in (stmt.test, stmt.msg) if e is not None]
        return self.node("assert_statement", stmt, children=children)

    def _stmt_Global(self, stmt):
        return self.node("global_statement", stmt, children=[self.identifier(n, stmt) for n in stmt.names])

    def _stmt_Nonlocal(self, stmt):
        return self.node("nonlocal_statement", stmt, children=[self.identifier(n, stmt) for n in stmt.names])

    def _stmt_Pass(self, stmt):
        return self.node("pass_statement", stmt)

    def _stmt_Break(self, stmt):
        return self.node("break_statement", stmt)

    def _stmt_Continue(self, stmt):
        return self.node("continue_statement", stmt)

    def _stmt_Match(self, stmt):
        children = [self.expression(stmt.subject)]
        for case in stmt.cases:
            children.append(self.node("case_clause", case, children=[self.block(case.body, case)]))
        return self.node("match_statement", stmt, children=children)

    # ── parameters ────────────────────────────────────────────────────────
    def parameters(self, args, owner) -> Node:
        children = []

        def widen(node: Node) -> Node:
            """Stretch a parameter node to cover its children.

            ``ast`` spans an ``arg`` over just the name and annotation, so a
            default value sits outside it. tree-sitter's ``default_parameter``
            covers ``name = value``, and code that slices ``node.text`` expects
            that, so the span is widened to the last child.
            """
            if node.children:
                last = node.children[-1]
                if last.end_byte > node.end_byte:
                    node.end_byte = last.end_byte
                    node.end_point = last.end_point
            return node

        def add(arg, default=None, splat=None):
            name_node = self.identifier(arg.arg, arg)
            if splat:
                children.append(widen(self.node(splat, arg, children=[name_node])))
                return
            if arg.annotation is not None and default is not None:
                type_node = self.type_node(arg.annotation)
                value = self.expression(default)
                children.append(
                    widen(self.node(
                        "typed_default_parameter",
                        arg,
                        children=[name_node, type_node, value],
                        fields={"name": name_node, "type": type_node, "value": value},
                    ))
                )
            elif arg.annotation is not None:
                type_node = self.type_node(arg.annotation)
                children.append(
                    widen(self.node(
                        "typed_parameter",
                        arg,
                        children=[name_node, type_node],
                        fields={"type": type_node},
                    ))
                )
            elif default is not None:
                value = self.expression(default)
                children.append(
                    widen(self.node(
                        "default_parameter",
                        arg,
                        children=[name_node, value],
                        fields={"name": name_node, "value": value},
                    ))
                )
            else:
                children.append(name_node)

        positional = list(getattr(args, "posonlyargs", [])) + list(args.args)
        defaults = list(args.defaults)
        # Defaults bind to the tail of the positional list.
        pad = len(positional) - len(defaults)
        for index, arg in enumerate(positional):
            add(arg, defaults[index - pad] if index >= pad else None)
        if args.vararg is not None:
            add(args.vararg, splat="list_splat_pattern")
        for arg, default in zip(args.kwonlyargs, args.kw_defaults):
            add(arg, default)
        if args.kwarg is not None:
            add(args.kwarg, splat="dictionary_splat_pattern")

        if children:
            start = (children[0].start_byte, children[0].start_point)
            end = (children[-1].end_byte, children[-1].end_point)
        else:
            start_byte, _eb, start_point, _ep = self._span(owner)
            start = end = (start_byte, start_point)
        return self.synthetic("parameters", start, end, children=children)

    # ── type annotations ──────────────────────────────────────────────────
    def type_node(self, annotation) -> Node:
        """Wrap an annotation in tree-sitter-python's ``type`` node."""
        inner = self.expression(annotation, in_type=True)
        return self.node("type", annotation, children=[inner])

    # ── patterns (assignment targets) ─────────────────────────────────────
    def pattern(self, target) -> Node:
        kind = type(target).__name__
        if kind == "Name":
            return self.identifier(target.id, target)
        if kind in ("Tuple", "List"):
            children = [self.pattern(e) for e in target.elts]
            node_type = "tuple_pattern" if kind == "Tuple" else "list_pattern"
            return self.node(node_type, target, children=children)
        if kind == "Starred":
            return self.node("list_splat_pattern", target, children=[self.pattern(target.value)])
        return self.expression(target)

    # ── expressions ───────────────────────────────────────────────────────
    def expression(self, expr, in_type: bool = False) -> Node:
        if expr is None:
            return None
        kind = type(expr).__name__

        if kind == "Name":
            return self.identifier(expr.id, expr)

        if kind == "Attribute":
            obj = self.expression(expr.value, in_type)
            attr = self.identifier(expr.attr, expr, offset=max(0, obj.end_byte - self._span(expr)[0]))
            return self.node(
                "attribute", expr, children=[obj, attr], fields={"object": obj, "attribute": attr}
            )

        if kind == "Call":
            function = self.expression(expr.func, in_type)
            arg_children = [self.expression(a) for a in expr.args]
            for keyword in expr.keywords:
                value = self.expression(keyword.value)
                if keyword.arg is None:
                    arg_children.append(
                        self.node("dictionary_splat", keyword.value, children=[value])
                    )
                else:
                    name_node = self.identifier(keyword.arg, keyword.value)
                    arg_children.append(
                        self.node(
                            "keyword_argument",
                            keyword.value,
                            children=[name_node, value],
                            fields={"name": name_node, "value": value},
                        )
                    )
            arg_children = [c for c in arg_children if c is not None]
            if arg_children:
                start = (arg_children[0].start_byte, arg_children[0].start_point)
                end = (arg_children[-1].end_byte, arg_children[-1].end_point)
            else:
                _sb, end_byte, _sp, end_point = self._span(expr)
                start = end = (end_byte, end_point)
            arguments = self.synthetic("argument_list", start, end, children=arg_children)
            return self.node(
                "call",
                expr,
                children=[function, arguments],
                fields={"function": function, "arguments": arguments},
            )

        if kind == "Subscript":
            value = self.expression(expr.value, in_type)
            # In an annotation, tree-sitter-python calls this generic_type with a
            # type_parameter child; in an expression it is a plain subscript.
            if in_type:
                inner = expr.slice
                elements = inner.elts if type(inner).__name__ == "Tuple" else [inner]
                param_children = [self.type_node(e) for e in elements if e is not None]
                if param_children:
                    start = (param_children[0].start_byte, param_children[0].start_point)
                    end = (param_children[-1].end_byte, param_children[-1].end_point)
                else:
                    _sb, end_byte, _sp, end_point = self._span(expr)
                    start = end = (end_byte, end_point)
                type_parameter = self.synthetic("type_parameter", start, end, children=param_children)
                return self.node("generic_type", expr, children=[value, type_parameter])
            index = self.expression(expr.slice)
            children = [c for c in (value, index) if c is not None]
            return self.node("subscript", expr, children=children, fields={"value": value})

        if kind == "Lambda":
            params = self.parameters(expr.args, expr)
            body = self.expression(expr.body)
            children = [c for c in (params, body) if c is not None]
            return self.node("lambda", expr, children=children, fields={"parameters": params, "body": body})

        if kind == "NamedExpr":
            name_node = self.pattern(expr.target)
            value = self.expression(expr.value)
            return self.node(
                "named_expression",
                expr,
                children=[name_node, value],
                fields={"name": name_node, "value": value},
            )

        if kind in ("ListComp", "SetComp", "GeneratorExp", "DictComp"):
            children = []
            if kind == "DictComp":
                children.extend(c for c in (self.expression(expr.key), self.expression(expr.value)) if c)
            else:
                element = self.expression(expr.elt)
                if element is not None:
                    children.append(element)
            for comp in expr.generators:
                left = self.pattern(comp.target)
                right = self.expression(comp.iter)
                clause_children = [left, right] + [self.expression(i) for i in comp.ifs]
                clause_children = [c for c in clause_children if c is not None]
                children.append(
                    self.node(
                        "for_in_clause",
                        comp.iter,
                        children=clause_children,
                        fields={"left": left, "right": right},
                    )
                )
            node_type = {
                "ListComp": "list_comprehension",
                "SetComp": "set_comprehension",
                "GeneratorExp": "generator_expression",
                "DictComp": "dictionary_comprehension",
            }[kind]
            return self.node(node_type, expr, children=children)

        if kind == "Constant":
            return self.node(_constant_type(expr.value), expr)

        if kind == "JoinedStr":
            return self.node("string", expr, children=self._child_exprs(expr))

        if kind == "Starred":
            return self.node("list_splat", expr, children=[self.expression(expr.value, in_type)])

        node_type = _EXPR_TYPES.get(kind, _snake(kind))
        return self.node(node_type, expr, children=self._child_exprs(expr, in_type))

    def _child_exprs(self, node, in_type: bool = False) -> list:
        """Generic descent: keep every child expression so nested calls stay reachable."""
        children = []
        for _field, value in ast.iter_fields(node):
            items = value if isinstance(value, list) else [value]
            for item in items:
                if isinstance(item, ast.expr):
                    built = self.expression(item, in_type)
                    if built is not None:
                        children.append(built)
                elif isinstance(item, ast.stmt):
                    built = self.statement(item)
                    if built is not None:
                        children.append(built)
        children.sort(key=lambda n: n.start_byte)
        return children

    # ── entry point ───────────────────────────────────────────────────────
    def module(self, tree) -> Node:
        children = [self.statement(stmt) for stmt in tree.body]
        children = [c for c in children if c is not None]
        end_point = self._point_for(len(self.source))
        return Node(
            "module",
            start_byte=0,
            end_byte=len(self.source),
            start_point=(0, 0),
            end_point=end_point,
            children=children,
            fields={},
            is_named=True,
            source=self.source,
        )


_EXPR_TYPES = {
    "BinOp": "binary_operator",
    "UnaryOp": "unary_operator",
    "BoolOp": "boolean_operator",
    "Compare": "comparison_operator",
    "IfExp": "conditional_expression",
    "Dict": "dictionary",
    "Set": "set",
    "List": "list",
    "Tuple": "tuple",
    "Slice": "slice",
    "Await": "await",
    "Yield": "yield",
    "YieldFrom": "yield",
    "FormattedValue": "interpolation",
}


def _constant_type(value) -> str:
    if value is None:
        return "none"
    if isinstance(value, bool):
        return _BOOL_LITERALS[value]
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "float"
    if isinstance(value, (str, bytes)):
        return "string"
    if value is Ellipsis:
        return "ellipsis"
    return "constant"


def _snake(name: str) -> str:
    out = []
    for index, char in enumerate(name):
        if char.isupper() and index:
            out.append("_")
        out.append(char.lower())
    return "".join(out)


def parse_python(source: bytes) -> Tree:
    """Parse Python source into a tree-sitter-python-shaped tree.

    A ``SyntaxError`` yields an empty ``module`` flagged as an error rather than
    propagating: tree-sitter is error-tolerant and always returns a tree, and
    ``graphify`` relies on that to keep scanning a repository that contains one
    unparseable file (or Python 2 source).
    """
    try:
        parsed = ast.parse(source)
    except (SyntaxError, ValueError, RecursionError):
        builder = _Builder(source)
        root = builder.module(ast.Module(body=[], type_ignores=[]))
        root.is_error = True
        return Tree(link_tree(root, source), source)
    builder = _Builder(source)
    root = builder.module(parsed)
    return Tree(link_tree(root, source), source)
