"""Per-language configuration for the bundled structural parsers.

Every node type name here is taken from the ``LanguageConfig`` blocks in
``graphify/extract.py`` and the language-specific branches in
``graphify/extractors/engine.py`` --- not from memory of the grammars. Those
blocks are the contract: upstream compares ``node.type`` against these exact
strings, so a mismatch means silently extracting nothing.

Keeping the specs in one file makes that contract auditable in a single read,
and makes it obvious which languages are covered.
"""
from __future__ import annotations

from ._brace import BraceSpec
from ._lexer import LexSpec

__all__ = ["SPECS"]

_C_LEX = LexSpec(line_comments=("//",), block_comments=(("/*", "*/"),), quotes=('"', "'"))
_JS_LEX = LexSpec(line_comments=("//",), block_comments=(("/*", "*/"),), quotes=('"', "'", "`"), ident_extra="_$")
_HASH_LEX = LexSpec(line_comments=("#",), block_comments=(), quotes=('"', "'"))

# JS and TS share everything but the set of type-declaration keywords.
_JS_COMMON = dict(
    lex=_JS_LEX,
    root_type="program",
    class_body_type="class_body",
    function_keywords={"function": "function_declaration"},
    method_type="method_definition",
    function_body_type="statement_block",
    import_keywords={"import": "import_statement"},
    # `export` prefixes a declaration rather than being one, so it wraps.
    wrapping_keywords={"export": "export_statement"},
    bare_methods=True,
    call_type="call_expression",
    call_function_field="function",
    new_expression_type="new_expression",
    accessor_type="member_expression",
    accessor_field="property",
    accessor_object_field="object",
    argument_list_type="arguments",
    parameters_type="formal_parameters",
    modifiers=("public", "private", "protected", "static", "async", "readonly", "abstract", "export", "default"),
)

SPECS: dict = {}

SPECS["javascript"] = BraceSpec(
    "javascript",
    class_keywords={"class": "class_declaration"},
    **_JS_COMMON,
)

# TypeScript adds interface/enum/type-alias declarations; graphify treats them
# as class-like container nodes (see _TS_CONFIG.class_types).
SPECS["typescript"] = BraceSpec(
    "typescript",
    class_keywords={
        "class": "class_declaration",
        "interface": "interface_declaration",
        "enum": "enum_declaration",
    },
    **_JS_COMMON,
)
SPECS["tsx"] = SPECS["typescript"]

SPECS["java"] = BraceSpec(
    "java",
    lex=_C_LEX,
    root_type="program",
    class_keywords={
        "class": "class_declaration",
        "interface": "interface_declaration",
        "enum": "enum_declaration",
        "record": "record_declaration",
        "@interface": "annotation_type_declaration",
    },
    class_body_type="class_body",
    function_keywords={},
    typed_declarations=True,
    typed_function_type="method_declaration",
    method_type="method_declaration",
    function_body_type="block",
    import_keywords={"import": "import_declaration", "package": "package_declaration"},
    # Java's method_invocation carries `object`/`name` directly, with no accessor
    # node -- hence call_style="flat" and _JAVA_CONFIG's empty accessor set.
    call_type="method_invocation",
    call_function_field="name",
    call_style="flat",
    new_expression_type="object_creation_expression",
    new_type_field="type",
    accessor_type="field_access",
    accessor_field="field",
    accessor_object_field="object",
    argument_list_type="argument_list",
    parameters_type="formal_parameters",
    heritage_style="java",
    modifiers=("public", "private", "protected", "static", "final", "abstract",
               "synchronized", "native", "transient", "volatile", "strictfp", "default"),
)

SPECS["groovy"] = BraceSpec(
    "groovy",
    lex=_C_LEX,
    root_type="program",
    class_keywords={"class": "class_declaration", "interface": "interface_declaration"},
    class_body_type="class_body",
    typed_declarations=True,
    typed_function_type="method_declaration",
    method_type="method_declaration",
    function_keywords={"def": "method_declaration"},
    function_body_type="block",
    import_keywords={"import": "import_declaration", "package": "package_declaration"},
    call_type="method_invocation",
    call_function_field="name",
    call_style="flat",
    accessor_type="field_access",
    accessor_field="field",
    accessor_object_field="object",
    argument_list_type="argument_list",
    heritage_style="java",
    modifiers=("public", "private", "protected", "static", "final", "abstract"),
)

SPECS["c"] = BraceSpec(
    "c",
    lex=_C_LEX,
    root_type="translation_unit",
    class_keywords={},
    typed_declarations=True,
    typed_function_type="function_definition",
    function_body_type="compound_statement",
    import_keywords={},
    call_type="call_expression",
    call_function_field="function",
    accessor_type="field_expression",
    accessor_field="field",
    accessor_object_field="argument",
    argument_list_type="argument_list",
    parameters_type="parameter_list",
    declarator_style=True,
    modifiers=("static", "extern", "inline", "const", "unsigned", "signed", "register", "volatile"),
)

SPECS["cpp"] = BraceSpec(
    "cpp",
    lex=_C_LEX,
    root_type="translation_unit",
    class_keywords={"class": "class_specifier", "struct": "struct_specifier"},
    class_body_type="field_declaration_list",
    typed_declarations=True,
    typed_function_type="function_definition",
    method_type="function_definition",
    function_body_type="compound_statement",
    import_keywords={},
    call_type="call_expression",
    call_function_field="function",
    accessor_type="field_expression",
    accessor_field="field",
    accessor_object_field="argument",
    argument_list_type="argument_list",
    parameters_type="parameter_list",
    declarator_style=True,
    heritage_style="csharp",     # `class D : public B` lists bases after a colon
    modifiers=("public", "private", "protected", "static", "virtual", "inline",
               "explicit", "const", "constexpr", "friend", "template"),
)

SPECS["c_sharp"] = BraceSpec(
    "c_sharp",
    lex=_C_LEX,
    root_type="compilation_unit",
    class_keywords={
        "class": "class_declaration",
        "interface": "interface_declaration",
        "enum": "enum_declaration",
        "struct": "struct_declaration",
        "record": "record_declaration",
        "namespace": "namespace_declaration",
    },
    class_body_type="declaration_list",
    typed_declarations=True,
    typed_function_type="method_declaration",
    method_type="method_declaration",
    function_body_type="block",
    import_keywords={"using": "using_directive"},
    call_type="invocation_expression",
    call_function_field="function",
    accessor_type="member_access_expression",
    accessor_field="name",
    accessor_object_field="expression",
    argument_list_type="argument_list",
    parameters_type="parameter_list",
    new_expression_type="object_creation_expression",
    heritage_style="csharp",
    modifiers=("public", "private", "protected", "internal", "static", "sealed",
               "abstract", "virtual", "override", "async", "partial", "readonly", "const"),
)

SPECS["kotlin"] = BraceSpec(
    "kotlin",
    lex=_C_LEX,
    root_type="source_file",
    class_keywords={"class": "class_declaration", "object": "object_declaration",
                    "interface": "class_declaration"},
    class_body_type="class_body",
    function_keywords={"fun": "function_declaration"},
    function_body_type="function_body",
    import_keywords={"import": "import_header", "package": "package_header"},
    call_type="call_expression",
    call_function_field="function",
    accessor_type="navigation_expression",
    accessor_field="name",
    accessor_object_field="expression",
    argument_list_type="call_suffix",
    parameters_type="function_value_parameters",
    modifiers=("public", "private", "protected", "internal", "open", "abstract",
               "override", "suspend", "data", "sealed", "inline", "companion"),
)

SPECS["scala"] = BraceSpec(
    "scala",
    lex=_C_LEX,
    root_type="compilation_unit",
    class_keywords={"class": "class_definition", "object": "object_definition",
                    "trait": "class_definition"},
    class_body_type="template_body",
    function_keywords={"def": "function_definition"},
    function_body_type="block",
    import_keywords={"import": "import_declaration", "package": "package_clause"},
    call_type="call_expression",
    call_function_field="function",
    accessor_type="field_expression",
    accessor_field="field",
    accessor_object_field="value",
    argument_list_type="arguments",
    parameters_type="parameters",
    heritage_style="scala",
    modifiers=("private", "protected", "final", "sealed", "implicit", "lazy", "override", "case"),
)

SPECS["swift"] = BraceSpec(
    "swift",
    lex=_C_LEX,
    root_type="source_file",
    class_keywords={"class": "class_declaration", "struct": "class_declaration",
                    "protocol": "protocol_declaration", "enum": "class_declaration",
                    "extension": "class_declaration"},
    class_body_type="class_body",
    function_keywords={"func": "function_declaration", "init": "init_declaration",
                       "deinit": "deinit_declaration", "subscript": "subscript_declaration"},
    function_body_type="function_body",
    import_keywords={"import": "import_declaration"},
    call_type="call_expression",
    call_function_field="function",
    accessor_type="navigation_expression",
    accessor_field="name",
    accessor_object_field="target",
    argument_list_type="call_suffix",
    parameters_type="parameter_clause",
    identifier_type="simple_identifier",
    type_identifier_type="type_identifier",
    modifiers=("public", "private", "internal", "fileprivate", "open", "static",
               "final", "override", "mutating", "lazy", "weak", "unowned", "required"),
)

SPECS["php"] = BraceSpec(
    "php",
    lex=LexSpec(line_comments=("//", "#"), block_comments=(("/*", "*/"),), quotes=('"', "'"), ident_extra="_$"),
    root_type="program",
    class_keywords={"class": "class_declaration", "interface": "interface_declaration",
                    "trait": "trait_declaration"},
    class_body_type="declaration_list",
    function_keywords={"function": "function_definition"},
    method_type="method_declaration",
    function_body_type="compound_statement",
    import_keywords={"use": "namespace_use_declaration", "namespace": "namespace_definition",
                     "require": "require_expression", "include": "include_expression"},
    call_type="function_call_expression",
    call_function_field="function",
    accessor_type="member_call_expression",
    accessor_field="name",
    accessor_object_field="object",
    argument_list_type="arguments",
    parameters_type="formal_parameters",
    identifier_type="name",
    type_identifier_type="name",
    new_expression_type="object_creation_expression",
    heritage_style="php",
    modifiers=("public", "private", "protected", "static", "abstract", "final", "readonly"),
)

SPECS["go"] = BraceSpec(
    "go",
    lex=_C_LEX,
    root_type="source_file",
    class_keywords={"type": "type_declaration"},
    class_body_type="field_declaration_list",
    function_keywords={"func": "function_declaration"},
    function_body_type="block",
    import_keywords={"import": "import_declaration", "package": "package_clause"},
    statement_terminator="",             # Go statements end at the newline
    receiver_before_name=True,           # func (s *Store) Add(...)
    call_type="call_expression",
    call_function_field="function",
    accessor_type="selector_expression",
    accessor_field="field",
    accessor_object_field="operand",
    argument_list_type="argument_list",
    parameters_type="parameter_list",
)

SPECS["rust"] = BraceSpec(
    "rust",
    lex=LexSpec(line_comments=("//",), block_comments=(("/*", "*/"),),
                nested_block_comments=True, quotes=('"',)),
    root_type="source_file",
    class_keywords={"struct": "struct_item", "enum": "enum_item", "trait": "trait_item",
                    "impl": "impl_item", "mod": "mod_item"},
    class_body_type="declaration_list",
    function_keywords={"fn": "function_item"},
    function_body_type="block",
    import_keywords={"use": "use_declaration"},
    call_type="call_expression",
    call_function_field="function",
    accessor_type="field_expression",
    accessor_field="field",
    accessor_object_field="value",
    argument_list_type="arguments",
    parameters_type="parameters",
    modifiers=("pub", "async", "unsafe", "extern", "const", "static", "mut", "dyn", "impl"),
)

SPECS["ruby"] = BraceSpec(
    "ruby",
    lex=_HASH_LEX,
    root_type="program",
    class_keywords={"class": "class", "module": "module"},
    class_body_type="body_statement",
    function_keywords={"def": "method"},
    function_body_type="body_statement",
    import_keywords={"require": "call", "require_relative": "call"},
    statement_terminator="",
    call_type="call",
    call_function_field="method",
    accessor_type="call",
    accessor_field="method",
    accessor_object_field="receiver",
    argument_list_type="argument_list",
    parameters_type="method_parameters",
    identifier_type="identifier",
    type_identifier_type="constant",
    heritage_style="ruby",
    # Ruby closes every body with `end`, so bodies are found by counting
    # openers rather than matching brackets.
    block_style="end",
    parenless_calls=True,
    block_openers=("def", "class", "module", "begin", "case", "do"),
    line_only_openers=("if", "unless", "while", "until", "for"),
)

SPECS["lua"] = BraceSpec(
    "lua",
    lex=LexSpec(line_comments=("--",), block_comments=(("--[[", "]]"),), quotes=('"', "'")),
    root_type="chunk",
    class_keywords={},
    function_keywords={"function": "function_declaration"},
    function_body_type="block",
    import_keywords={},
    statement_terminator="",
    call_type="function_call",
    call_function_field="name",
    accessor_type="method_index_expression",
    accessor_field="name",
    accessor_object_field="table",
    argument_list_type="arguments",
    parameters_type="parameters",
    block_style="end",
    block_openers=("function", "do"),
    line_only_openers=("if", "while", "for", "repeat"),
)
