# connect_my_code

A portable, **zero-install** distribution of
[graphify](https://github.com/Graphify-Labs/graphify) — turn any folder of code
into a queryable knowledge graph.

```bash
git clone <this-repo>
cd connect_my_code
./cmc extract /path/to/your/project
./cmc query "how does authentication work"
```

No `uv`. No `pip`. No `npm`. No virtualenv, no build step, no compiler.
The only requirement is **Python 3.10 or newer** — which macOS and every Linux
distribution already ship.

---

## Why this exists

Upstream graphify installs with `uv tool install graphifyy`, which pulls **33
required wheels**: `networkx`, `numpy`, `rapidfuzz`, `tree-sitter`, and 29
compiled tree-sitter grammars. Those grammars are per-platform C extensions, so
"just commit the wheels" cannot be portable across operating systems, CPU
architectures and Python versions.

connect_my_code keeps the upstream package **byte-identical** and supplies its
dependencies from a bundled pure-standard-library shim layer instead.

---

## Usage

`./cmc` takes every graphify command, unchanged:

```bash
./cmc extract .                    # build the graph (add --code-only to skip LLM steps)
./cmc query "how do orders get priced"
./cmc explain OrderService
./cmc path User Invoice            # shortest dependency path between two symbols
./cmc god-nodes                    # most-connected nodes
./cmc affected src/models.py       # blast radius of a change
./cmc tree                         # interactive HTML tree
./cmc export html|obsidian|graphml
./cmc benchmark                    # token savings vs. reading the raw corpus
./cmc cluster-only .               # re-cluster and write GRAPH_REPORT.md
```

Two commands are specific to this port:

```bash
./cmc doctor      # show which dependencies resolved real vs. bundled
./cmc selftest    # run the portability test suite
```

| Platform | Launcher |
|----------|----------|
| macOS / Linux / WSL / Git-Bash | `./cmc …` |
| Windows (cmd / PowerShell) | `cmc …` |
| Any (explicit interpreter) | `python3 cmc.py …` or `CMC_PYTHON=python3.12 ./cmc …` |

---

## How it works

```
cmc / cmc.cmd / cmc.py     launcher — finds an interpreter, installs the shim layer
runtime/bootstrap.py       sys.meta_path finder: real wheels win, shims fill gaps
runtime/shims/             pure-stdlib implementations
runtime/dist/              stub .dist-info so --version reports correctly
graphify/                  UNMODIFIED upstream package (216 files, byte-identical)
tests/                     portability test suite
```

### Real dependencies always win

`runtime/shims/` is deliberately **never** placed on `sys.path`. A finder
appended to `sys.meta_path` claims a module name only after confirming the
ambient environment cannot supply it. So:

- If you already have real `networkx`/`numpy`/`rapidfuzz` installed, you keep
  them — per module, with no configuration.
- **Migration is just `pip install`.** Install any real wheel and it takes over
  on the next run. Nothing to reconfigure, no flag to flip.
- `./cmc doctor` shows exactly what resolved to what.

`tree_sitter` is the one module whose shim always loads, because it is a
*delegating front-end*: it hands off to the real C parser for any language whose
grammar is installed, and uses a bundled parser for the rest. That is what lets a
mixed environment (real `tree-sitter` + real `tree-sitter-python`, but no
`tree-sitter-kotlin`) use the C parser for Python and the bundled parser for
Kotlin **in the same run**.

### Upstream stays byte-identical

Nothing under `graphify/` is edited. All portability logic lives in `runtime/`,
so re-syncing to a newer upstream is a directory copy, not a merge.
`UPSTREAM_COMMIT` pins the revision this tree was taken from.

---

## Fidelity: what matches exactly, and what does not

This section is deliberately specific. Not everything is a byte-for-byte
reproduction, and it matters which parts are.

### Exact

| Shim | Status |
|------|--------|
| `rapidfuzz` | Jaro, Jaro-Winkler and **unrestricted** Damerau-Levenshtein, matching published reference values (`MARTHA`/`MARHTA` → 0.944444 / 0.961111). |
| `numpy` | Bit-exact for `_minhash.py`. Reproduces randomkit's `mt19937_seed`, high-word-first `next_uint64` and masked-rejection `randint`, so MinHash coefficients — and therefore dedup's merge decisions — match real NumPy. Twist/temper validated against the canonical `init_genrand(5489)` vector. |
| `networkx` | Graph containers and views, node-link JSON round-trip, and Louvain — the last implemented step-for-step against NetworkX's own `louvain.py`, including the seeded node shuffle, so community assignments agree. |
| **Python parsing** | Backed by CPython's own `ast`. The parse is exact by construction; only node names and positions are translated into tree-sitter's vocabulary. |

### Structural, not a full grammar

The other 14 bundled languages use a **structural parser**, not a
reimplementation of each tree-sitter grammar. It recognises what graphify builds
its graph from — type declarations, functions and methods, imports, inheritance
clauses, and call expressions with their receiver chains — and emits the node
types the real grammars use for those constructs.

**The design rule is: fewer edges, never wrong edges.** Everything emitted has
actually been matched in the token stream. Constructs the parser does not model
produce no node at all, which costs *recall* in graphify's deeper inference
passes rather than inventing relationships. Install the real grammar for a
language and the front-end delegates to it, recovering full fidelity.

Measured on graphify's own multi-language test fixtures — one file per language,
extracted with no third-party packages installed:

| Language | Nodes | Edges | Relations recovered |
|----------|-------|-------|---------------------|
| Python | exact | exact | full upstream behaviour (CPython `ast`) |
| Java | 12 | 16 | contains, method, calls, inherits, implements, imports |
| PHP | 16 | 19 | contains, method, calls, inherits, implements |
| Swift | 16 | 17 | contains, method, calls |
| C# | 10 | 16 | contains, method, calls, inherits, implements, imports |
| Rust | 13 | 14 | contains, calls |
| Kotlin | 11 | 14 | contains, method, calls, imports |
| C++ | 10 | 12 | contains, method, calls |
| Ruby | 9 | 10 | contains, method, calls |
| Groovy | 7 | 10 | contains, method, calls, inherits, implements, imports |
| Scala | 6 | 8 | contains, method, calls, imports |
| Go | 6 | 7 | contains, calls |
| C | 5 | 6 | contains, calls |
| TypeScript / TSX | 4 | 3–5 | contains, method, calls |

Cross-file resolution works across the port: inherited-method calls
(`Order.total` → `Base.audit` in another file), constructor calls, and
type-annotation references all resolve.

### Not covered by bundled parsers

These languages have no bundled grammar, so their files are skipped exactly as
they would be with an incomplete `pip install` — upstream already returns a
structured `"<module> not installed"` result for a missing grammar and carries
on:

Elixir, Julia, Zig, Verilog, Fortran, PowerShell, Objective-C, Pascal, SQL,
HCL/Terraform, DreamMaker, Dart, Bash, JSON.

Install the corresponding `tree-sitter-*` wheel to enable any of them.

### Optional features

Everything upstream guards behind `try/except ImportError` behaves the same
here: install the extra to enable it.

| Feature | Needs |
|---------|-------|
| MCP server (`graphify-mcp`) | `mcp`, `starlette` |
| Leiden clustering (better than Louvain) | `graspologic` |
| SVG export | `matplotlib` |
| PDF / Office / video ingest | `pypdf`, `python-docx`, `openpyxl`, `faster-whisper` |
| Neo4j / FalkorDB export | `neo4j`, `falkordb` |
| LLM semantic extraction of docs | an API key (`GEMINI_API_KEY`, `ANTHROPIC_API_KEY`, …) |
| File watching | `watchdog` |

Code-only extraction needs **none** of these — use `--code-only`.

---

## Verification

`./cmc selftest` runs 31 tests covering the shim layer: reference values for
every metric, the MT19937 vector, NetworkX view semantics and JSON round-trips,
Louvain's recovery of a planted partition, per-language parse shapes, and a full
end-to-end extraction asserting cross-file inheritance and call resolution.

Beyond the suite, this tree was exercised on graphify's own 80-file, 55k-line
source: **2168 nodes, 4257 edges, 160 communities in ~28s**, with entity dedup
running through the MinHash/rapidfuzz/numpy shims. The top god-node
(`_read_text()`, 85 edges) matches the codebase's real shape.

---

## Development

- **Never edit anything under `graphify/`.** Portability logic belongs in
  `runtime/`.
- Shims defer to real wheels; `tree_sitter` is the sole always-front-ended
  module, and only because it delegates per language.
- Unsupported operations raise a clear error naming the shim — they never
  silently approximate.
- `progress.md`, `learnings.md` and `next_session.md` track state and rationale.

## Licence

Upstream graphify is Apache-2.0; `LICENSE`, `LICENSE-MIT` and `NOTICE` are
carried over unchanged. The `runtime/` portability layer is provided under the
same terms.
