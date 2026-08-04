# Next session — connect_my_code

**Resume point:** milestones 1–4 done and verified. Milestone 5 (`tree_sitter`)
is the remaining blocker; nothing can extract until it lands.

---

## How to pick up

```bash
cd connect_my_code
./cmc doctor            # shows real-vs-shim resolution for every dependency
./cmc selftest          # portability test suite (once tests/ is populated)
```

Reference clone of upstream is at `../graphify` (pinned to
`00efd6e7969837ae4a9f11d8d504dcd3b20b09df`, v0.9.32). Consult it for exact node
type names — do not guess them.

---

## Milestone 5 — `tree_sitter` shim + language parsers

### Target API (measured from upstream, not guessed)

Node members actually used, with call counts:

```
type 804 · child_by_field_name 302 · parent 208 · start_point 178 · is_named 79
start_byte 30 · end_byte 25 · text 24 · root_node 24 · walk 11
next_named_sibling 2 · has_error 1 · children_by_field_name 1 · child_count 1
```

Plus `Language`, `Parser`, `parser.parse(bytes) -> Tree`, `tree.root_node`, and
module-level `LANGUAGE_VERSION` (must be `>= 14`, checked by
`extract.py:_check_tree_sitter_version`).

**No `Query` / S-expression API is used anywhere** — this is what makes the shim
feasible. Do not build a query engine.

### Architecture to implement

1. `runtime/shims/tree_sitter/__init__.py` — front-end.
   - `Language(spec)`: if `spec` is a bundled `PureGrammar` marker → pure
     parser; otherwise delegate to the real C extension via
     `bootstrap.real_module("tree_sitter")`.
   - This dual dispatch is what allows real-grammar and shim-grammar languages
     to coexist in a single run.
2. `runtime/shims/tree_sitter/node.py` — `Node` / `Tree` / `TreeCursor` with the
   member list above. `text` is a `bytes` property sliced from the source.
3. `runtime/shims/tree_sitter/parser.py` — generic tokenizer (string/comment/
   nesting aware) + structural parser, parameterised per language.
4. `runtime/shims/tree_sitter_<lang>.py` × 29 — each exports `language()`
   returning its `PureGrammar`.

### Node type names must match the real grammars

`extract.py` compares `node.type` against exact grammar strings. Source of
truth is the `LanguageConfig` blocks in `graphify/extract.py` (~line 690+) and
`graphify/extractors/models.py`. Example — Python:

```python
class_types    = {"class_definition"}
function_types = {"function_definition"}
import_types   = {"import_statement", "import_from_statement"}
call_types     = {"call"}
call_function_field = "function"
call_accessor_node_types = {"attribute"}
```

Field names (`name`, `body`, `function`, `attribute`, `object`, `declarator`)
must resolve through `child_by_field_name` with the same semantics.

### Suggested order

1. Python (indentation-based, and the most-tested language upstream).
2. Brace family — JS/TS, Java, Go, Rust, C, C++, C#, Kotlin, Scala, Swift, PHP.
3. Remainder — Ruby, Lua, Bash, JSON, Elixir, Julia, Zig, Verilog, Fortran,
   PowerShell, Objective-C, Pascal, SQL, HCL, Groovy, DM.

Grammars that upstream already treats as optional (`elixir`, `hcl`, `dm`,
`pascal`, `sql`) return a structured `{"nodes": [], "edges": [], "error": ...}`
when missing, so they are the safest to land last.

---

## Milestone 6 — verification plan

- Run the pipeline over a fixture tree and over `graphify/` itself:
  `./cmc extract . --no-cluster` then `build`, `cluster`, `analyze`, `report`,
  `export`, `query`.
- Port upstream `tests/` that do not require the real C parser; wire into
  `./cmc selftest`.
- Diff `graph.json` against upstream where a real-wheel environment is
  available, to quantify extraction parity per language.
- Record per-language fidelity honestly in `progress.md` — a pure-Python parser
  will not match a full GLR grammar on every construct, and the README must say
  so rather than implying byte-identical ASTs.

---

## Standing constraints

- **Never edit anything under `graphify/`.** All portability logic lives in
  `runtime/`. Re-syncing upstream must stay a directory copy.
- Shims defer to real wheels; `tree_sitter` is the sole always-front-ended
  module, and only because it delegates per language.
- Unsupported operations raise a clear error naming the shim — never silently
  approximate.
- Update `progress.md`, `learnings.md` and this file at each milestone.
