# Next session — connect_my_code

**Status: all six milestones complete.** The tool runs from a bare clone with no
third-party packages, 34/34 selftests pass, Python plus 14 other languages
extract successfully, and skill installation into AI assistants works.

---

## How to pick up

```bash
cd connect_my_code
./cmc doctor      # real-vs-shim resolution for every dependency
./cmc selftest    # 34 portability tests
./cmc extract /path/to/project --code-only
```

Reference clone of upstream is at `../graphify` (pinned to
`00efd6e7969837ae4a9f11d8d504dcd3b20b09df`, v0.9.32) — consult it for exact node
type names rather than guessing. Recreate with:

```bash
git clone https://github.com/Graphify-Labs/graphify graphify
```

---

## Highest-value next steps

Ordered by value per unit of effort.

### 1. More bundled grammars

Not yet covered, so these files are skipped exactly as with an incomplete `pip`
install: Elixir, Julia, Zig, Verilog, Fortran, PowerShell, Objective-C, Pascal,
SQL, HCL/Terraform, DreamMaker, Dart, Bash, JSON.

Bash and JSON are the cheapest wins — JSON needs a small dedicated parser
(`json_config.py` reads object/pair/string nodes) and Bash has its own extractor
in `extractors/bash.py` with a modest node vocabulary. Objective-C, Dart and Zig
fit the existing brace-family spec in `_langs.py` with little new code.

### 2. Deeper structural recall for covered languages

The structural parser emits declarations, imports, inheritance and calls. It does
*not* emit the finer nodes some inference passes read — `variable_declarator`,
field/property declarations, JS/TS arrow functions bound to consts, C++ local
variable declarations for receiver typing. Adding these raises edge recall
without changing the correctness rule (`_brace.py`'s "fewer edges, never wrong
edges").

Start by reading which node types a language branch in
`graphify/extractors/engine.py` inspects, then emit those.

### 3. An `mcp` shim

Would restore `graphify-mcp` — the MCP stdio server in `graphify/serve.py` — with
no install. The protocol is JSON-RPC over stdio, so a stdlib implementation is
tractable. `serve.py` is dual-compatible with the 1.x decorator API and the 2.x
`on_*` constructor-callback API, and picks at runtime in `_build_server`, so the
shim only needs one of the two.

### 4. Parity diffing against real wheels

In an environment where the real wheels *can* be installed, run both and diff
`graph.json` per language. That converts the README's coverage table from
"relations recovered" into a measured recall percentage against ground truth.

---

## Standing constraints

- **Never edit anything under `graphify/`.** All portability logic lives in
  `runtime/`, so re-syncing upstream stays a directory copy.
- Shims defer to real wheels; `tree_sitter` is the sole always-front-ended
  module, and only because it delegates per language.
- Unsupported operations raise a clear error naming the shim — never silently
  approximate.
- Node type names come from `graphify/extract.py`'s `LanguageConfig` blocks and
  the language branches in `graphify/extractors/engine.py`. Do not guess them.
- New language work is verified by extracting a fixture and reading the graph —
  a wrong parser produces missing output, not an exception.
- Update `progress.md`, `learnings.md` and this file at each milestone.
