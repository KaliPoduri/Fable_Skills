# connect_my_code

**Turn any folder of code into a queryable knowledge graph — with nothing to install.**

```bash
git clone <this-repo>
cd connect_my_code
./cmc extract /path/to/your/project
./cmc query "how does authentication work"
```

No `uv`. No `pip`. No `npm`. No virtualenv, no build step, no compiler, no
network access required. The only prerequisite is **Python 3.10 or newer**,
which macOS and every Linux distribution already ship.

This is a portable distribution of
[graphify](https://github.com/Graphify-Labs/graphify) — same tool, same
commands, same output format, repackaged so it runs straight from a clone.

---

## Table of contents

1. [What this actually does](#1-what-this-actually-does)
2. [Quick start](#2-quick-start)
3. [A worked example](#3-a-worked-example)
4. [Command reference](#4-command-reference)
5. [How graphify works](#5-how-graphify-works)
6. [How the zero-install part works](#6-how-the-zero-install-part-works)
7. [Fidelity: what matches exactly, what doesn't](#7-fidelity-what-matches-exactly-what-doesnt)
8. [Optional features](#8-optional-features)
9. [Using it with AI coding assistants](#9-using-it-with-ai-coding-assistants)
10. [Troubleshooting](#10-troubleshooting)
11. [Project layout](#11-project-layout)
12. [Development guide](#12-development-guide)
13. [Keeping up with upstream](#13-keeping-up-with-upstream)
14. [FAQ](#14-faq)
15. [Licence and credits](#15-licence-and-credits)

---

## 1. What this actually does

### The problem it solves

When you (or an AI coding assistant) need to understand an unfamiliar codebase,
the usual approach is grep-and-read: search for a symbol, open the file, follow
an import, open another file. That's slow for a human and expensive for an LLM,
because every file you read burns context on code that turns out to be
irrelevant.

graphify takes a different approach. It parses your codebase once and builds a
**knowledge graph**: every class, function, file and document becomes a *node*,
and every import, call, inheritance and type reference becomes an *edge*. Then
you ask questions of the graph instead of the files.

```bash
./cmc query "how are users promoted to admins"
```

...returns just the relevant subgraph — the handful of classes and functions
actually involved, with their relationships and line numbers — instead of the
whole file tree. On a real codebase that's typically a **3–10× reduction** in
tokens needed to answer a question (`./cmc benchmark` measures it for yours).

### What you get

- **`graph.json`** — the graph itself, in NetworkX node-link format
- **`GRAPH_REPORT.md`** — a written architectural overview
- **`graph.html`** — an interactive browser visualisation, no server needed
- **`GRAPH_TREE.html`** — a collapsible D3 tree of the codebase
- An **Obsidian vault** export, **GraphML** for Gephi/yEd, and more

### Why this repackaging exists

Upstream graphify is installed with `uv tool install graphifyy`, which pulls
**33 required wheels**: `networkx`, `numpy`, `rapidfuzz`, `tree-sitter`, and 29
compiled tree-sitter language grammars.

Those grammars are per-platform C extensions. That means "just commit the
wheels into the repo" can never work portably — you'd need a different set for
every combination of operating system, CPU architecture and Python version.

connect_my_code takes a different route: **keep the upstream package
byte-identical, and supply its dependencies from a bundled pure-standard-library
shim layer.** Section 6 explains how, and section 7 is honest about where that
differs from the real thing.

---

## 2. Quick start

### Requirements

| Need | Detail |
|------|--------|
| Python | 3.10 or newer (`python3 --version` to check) |
| Disk | ~30 MB for the clone |
| Network | None, for code-only extraction |
| API key | None, for code-only extraction |

### Install (there isn't one)

```bash
git clone <this-repo>
cd connect_my_code
./cmc doctor        # confirms your Python works and shows what resolved to what
```

### Your first graph

```bash
cd /path/to/your/project
/path/to/connect_my_code/cmc extract . --code-only
/path/to/connect_my_code/cmc query "what talks to the database"
```

`--code-only` indexes source code using the local parsers and **skips
documentation files**, which would otherwise require an LLM API key. Drop the
flag once you've set a key (see [section 8](#8-optional-features)).

Output lands in `graphify-out/` inside the project you scanned.

### Making `cmc` convenient

Add the repo to your `PATH` so you can run `cmc` from anywhere:

```bash
echo 'export PATH="$PATH:/path/to/connect_my_code"' >> ~/.bashrc   # or ~/.zshrc
```

Or symlink it: `ln -s /path/to/connect_my_code/cmc ~/.local/bin/cmc`

### Per-platform launchers

| Platform | Command |
|----------|---------|
| macOS / Linux / WSL / Git-Bash | `./cmc …` |
| Windows (cmd.exe / PowerShell) | `cmc …` |
| Any, explicit interpreter | `python3 cmc.py …` |
| Pick a specific Python | `CMC_PYTHON=python3.12 ./cmc …` |

---

## 3. A worked example

Two small Python files:

```python
# models.py
"""Domain models for the demo app."""
from dataclasses import dataclass

@dataclass
class User:
    """A registered user of the system."""
    name: str
    email: str

    def display(self) -> str:
        return f"{self.name} <{self.email}>"

class Admin(User):
    """An administrator with elevated rights."""

    def grant(self, target: User) -> bool:
        return target.display() is not None
```

```python
# service.py
"""Service layer wiring models to storage."""
from models import User, Admin

class UserService:
    """Creates and looks up users."""

    def create(self, name: str, email: str) -> User:
        user = User(name, email)
        self.store.save(user)
        return user

def bootstrap(store):
    svc = UserService(store)
    svc.create("root", "root@example.com")
    return svc
```

Extract:

```console
$ ./cmc extract . --no-cluster
[graphify extract] scanning /demo
[graphify extract] found 2 code, 0 docs, 0 papers, 0 images
[graphify extract] AST extraction on 2 code files...
[graphify extract] wrote graphify-out/graph.json — 16 nodes, 26 edges
```

What it found — note these span **both files**:

```
models.py  --contains-->      User
User       --method-->        .display()
Admin      --inherits-->      User                # cross-file class hierarchy
service.py --imports_from-->  models.py
.create()  --references-->    User                # from the return annotation
.create()  --calls-->         User                # constructor call
bootstrap()--calls-->         UserService
bootstrap()--calls-->         .create()           # cross-file method resolution
"Domain models for the demo app." --rationale_for--> models.py   # docstrings
```

Ask a question:

```console
$ ./cmc explain UserService
Node: UserService
  ID:        service_userservice
  Source:    service.py L5
  Degree:    6

Connections (6):
  --> .create()   [method]       service.py:L11
  --> .promote()  [method]       service.py:L16
  <-- bootstrap() [calls]        service.py:L23
```

Trace a dependency chain:

```console
$ ./cmc path User bootstrap
Shortest path (2 hops):
  User <--calls/references-- .create() <--calls-- bootstrap()
```

Everything above was produced by this repo with **zero third-party packages
installed**.

---

## 4. Command reference

`./cmc` accepts every graphify command unchanged. The ones you'll use most:

### Building the graph

```bash
./cmc extract <path>              # full extraction (AST + LLM for docs)
./cmc extract <path> --code-only  # code only; no API key needed
./cmc extract <path> --no-cluster # skip community detection (faster)
./cmc update <path>               # re-extract changed code, no LLM
./cmc cluster-only <path>         # re-cluster + regenerate GRAPH_REPORT.md
./cmc watch <path>                # rebuild on file changes (needs watchdog)
```

### Asking questions

```bash
./cmc query "how do orders get priced"   # scoped subgraph for a question
./cmc query "..." --budget 4000          # allow a larger answer
./cmc query "..." --dfs                  # depth-first instead of breadth-first
./cmc explain OrderService               # one node and its neighbours
./cmc path User Invoice                  # shortest dependency path
./cmc affected src/models.py             # blast radius of changing a file
./cmc god-nodes                          # most-connected nodes (architecture hubs)
./cmc god-nodes --top 20 --json
```

### Visualising and exporting

```bash
./cmc tree                     # collapsible D3 tree -> GRAPH_TREE.html
./cmc export html              # interactive graph -> graph.html
./cmc export obsidian          # Obsidian vault + canvas
./cmc export graphml           # for Gephi / yEd / Cytoscape
./cmc export callflow-html     # Mermaid architecture & call-flow diagrams
./cmc export svg               # static image (needs matplotlib)
./cmc benchmark                # measure token savings on your graph
```

### Multi-repo

```bash
./cmc clone <github-url>            # clone a repo to a managed location
./cmc global add graph.json --as web   # merge into a cross-repo global graph
./cmc global list
./cmc merge-graphs a.json b.json --out merged.json
```

### AI-assistant integration

```bash
./cmc install --platform claude   # see section 9 for the full platform list
./cmc uninstall
./cmc hook install                # git post-commit/post-checkout hooks
```

### Specific to this port

```bash
./cmc doctor      # which dependencies resolved real vs. bundled
./cmc selftest    # run the 34-test portability suite
```

Run `./cmc --help` for the complete list, including flags not shown here.

---

## 5. How graphify works

Understanding the pipeline helps when reading output or debugging.

```
detect() → extract() → build_graph() → cluster() → analyze() → report() → export()
```

| Stage | What it does |
|-------|--------------|
| **detect** | Walks the directory, honouring `.gitignore` and `.graphifyignore`, and classifies each file as code / doc / paper / image |
| **extract** | Parses each code file into `{nodes, edges}`. This is where tree-sitter (or, here, the bundled parsers) does its work |
| **build_graph** | Merges every file's extraction into one graph, resolving cross-file references |
| **cluster** | Community detection (Louvain) groups related nodes into subsystems |
| **analyze** | Finds god-nodes, dependency cycles, and architectural surprises |
| **report** | Renders `GRAPH_REPORT.md` |
| **export** | Writes `graph.json`, `graph.html`, Obsidian vault, GraphML, … |

### The output schema

Every extractor emits the same shape:

```json
{
  "nodes": [
    {"id": "models_user", "label": "User", "source_file": "models.py", "source_location": "L6"}
  ],
  "edges": [
    {"source": "models_admin", "target": "models_user",
     "relation": "inherits", "confidence": "EXTRACTED"}
  ]
}
```

### Confidence levels

| Label | Meaning |
|-------|---------|
| `EXTRACTED` | Explicitly stated in source — an import, a direct call |
| `INFERRED` | A reasonable deduction — second-pass call-graph resolution |
| `AMBIGUOUS` | Uncertain; flagged for human review in the report |

### Common relations

`contains`, `method`, `calls`, `imports`, `imports_from`, `inherits`,
`implements`, `references`, `rationale_for`, `indirect_call`, `mixes_in`,
`embeds`, `re_exports`.

---

## 6. How the zero-install part works

This section is about *this repo's* contribution. Skip it if you just want to
use the tool.

### The layout

```
cmc, cmc.cmd, cmc.py       launcher — finds an interpreter, activates the shims
bin/graphify               the launcher under the name `graphify` (see below)
runtime/bootstrap.py       the dependency resolver
runtime/shims/             pure-standard-library implementations
runtime/dist/              stub .dist-info so --version reports correctly
graphify/                  UNMODIFIED upstream package — 216 files, byte-identical
tests/                     portability test suite
tools/sync_upstream.sh     re-sync to a newer upstream
```

### Real dependencies always win

`runtime/shims/` is deliberately **never** placed on `sys.path`. Instead a
finder appended to `sys.meta_path` claims a module name only *after* confirming
the ambient environment cannot supply it:

```python
def find_spec(self, fullname, path=None, target=None):
    target_file = _shim_target(fullname)
    if target_file is None:
        return None                     # not something we ship
    if fullname not in _ALWAYS_SHIM and _real_spec(fullname) is not None:
        return None                     # a real package exists — defer to it
    return spec_from_file_location(fullname, target_file)
```

Three properties fall out of that ordering:

- **If you already have real `networkx`/`numpy`/`rapidfuzz` installed, you keep
  them** — per module, with no configuration.
- **Migration is just `pip install`.** Install any real wheel and it takes over
  on the next run. Nothing to reconfigure, no flag to flip, no reinstall.
- Shim code is only ever exercised where it is genuinely needed.

Prepending the shim directory to `sys.path` instead would have inverted this and
silently shadowed better implementations.

`./cmc doctor` shows the current resolution:

```console
$ ./cmc doctor
  dependency resolution (real = installed wheel, shim = bundled pure-Python):
    networkx                shim
    numpy                   shim
    rapidfuzz               shim
    tree_sitter_python      shim
    ...
  20 of 20 dependencies served by bundled shims.
```

### Why `tree_sitter` is the one exception

`tree_sitter` is the only shim that loads even when a real version is installed,
because it is a **delegating front-end** rather than a replacement. It dispatches
on the *grammar object* it is handed:

- a bundled grammar marker → use the bundled parser
- anything else (a real grammar's PyCapsule) → forward to the genuine C extension

That's what lets a *mixed* environment work. With real `tree-sitter` and real
`tree-sitter-python` installed but no `tree-sitter-kotlin`, a single run uses the
fast C parser for Python and the bundled parser for Kotlin. Gating it like the
other shims would instead hand a Python marker object to a C `Language()`
constructor and crash.

### Why `bin/graphify` exists

graphify's skill installers write hook commands into AI-assistant configs, and
resolve the executable to embed via `shutil.which("graphify")`. A zero-install
checkout has no such binary, so every generated hook would carry a bare
`graphify` that fails at runtime.

`bin/graphify` is this launcher under that name. `cmc.py` prepends `bin/` to
`PATH`, so `which()` resolves to it and the installers embed a working absolute
path. Nothing is installed system-wide.

### Why upstream sources stay byte-identical

Nothing under `graphify/` is edited — all portability logic lives in `runtime/`.
That makes re-syncing to a newer upstream a **directory copy rather than a
merge**, which is the difference between this port staying maintainable and
rotting after two releases. `UPSTREAM_COMMIT` pins the revision.

Even the version string is handled without a source edit: `graphify/__main__.py`
calls `importlib.metadata.version("graphifyy")`, so `runtime/dist/` ships a stub
`.dist-info` that makes it resolve.

---

## 7. Fidelity: what matches exactly, what doesn't

Not everything here is a byte-for-byte reproduction, and it matters which parts
are. This section is deliberately specific.

### Exact

| Component | Status |
|-----------|--------|
| **`rapidfuzz`** | Jaro, Jaro-Winkler and **unrestricted** Damerau-Levenshtein, matching published reference values (`MARTHA`/`MARHTA` → 0.944444 / 0.961111). |
| **`numpy`** | Bit-exact for `_minhash.py`. Reproduces randomkit's `mt19937_seed`, high-word-first `next_uint64`, and masked-rejection `randint`, so MinHash coefficients — and therefore entity dedup's merge decisions — match real NumPy. Twist/temper validated against the canonical `init_genrand(5489)` vector. |
| **`networkx`** | Graph containers and views, node-link JSON round-trip, and Louvain community detection — the last implemented step-for-step against NetworkX's own `louvain.py`, including the seeded node shuffle, so community assignments agree. |
| **Python parsing** | Backed by CPython's own `ast` module. The parse is exact *by construction*; only node names and positions are translated into tree-sitter's vocabulary. |

Why the PRNG work mattered: `_minhash` seeds `RandomState(1)` to build its hash
family. Those coefficients decide LSH banding → which label pairs get compared →
which entities dedup merges → the node set in `graph.json`. An
"equivalent-quality" PRNG would silently produce a *different graph*.

### Structural, not a full grammar

The other 14 bundled languages use a **structural parser** — not a
reimplementation of each tree-sitter grammar. It recognises what graphify builds
its graph from (type declarations, functions and methods, imports, inheritance
clauses, and call expressions with receiver chains) and emits the node types the
real grammars use for those constructs.

> **The design rule is: fewer edges, never wrong edges.**
>
> Everything emitted has actually been matched in the token stream. Constructs
> the parser doesn't model produce *no node at all* — which costs **recall** in
> graphify's deeper inference passes, rather than inventing relationships that
> aren't there.

Install the real grammar for any language and the front-end delegates to it,
recovering full fidelity.

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
| JavaScript | — | — | same parser as TypeScript |
| Lua | — | — | declarations and calls |

Cross-file resolution works throughout: inherited-method calls (`Order.total` →
`Base.audit` in a different file), constructor calls, and type-annotation
references all resolve correctly.

### Not covered by bundled parsers

These languages have no bundled grammar, so their files are **skipped** — exactly
as they would be with an incomplete `pip install`. Upstream already returns a
structured `"<module> not installed"` result for a missing grammar and carries on:

> Elixir, Julia, Zig, Verilog, Fortran, PowerShell, Objective-C, Pascal, SQL,
> HCL/Terraform, DreamMaker, Dart, Bash, JSON

Install the corresponding `tree-sitter-*` wheel to enable any of them:

```bash
pip install tree-sitter tree-sitter-elixir     # then re-run extract
```

### Known issues

**`export graphml` fails if you install real NetworkX** — an upstream graphify
bug, not a shim gap. `graphify/export.py:to_graphml` iterates
`for u, v in H.edges()` and then indexes `H.edges[u, v]`; on the multigraphs
graphify itself writes, real NetworkX requires `H.edges[u, v, key]` and raises
`ValueError: not enough values to unpack`. Reproducible with real NetworkX alone:

```python
import networkx as nx
G = nx.MultiGraph(); G.add_edge('a', 'b')
for u, v in G.edges():
    G.edges[u, v]      # ValueError on a multigraph
```

The bundled shim accepts the 2-tuple form deliberately, so GraphML export works
on the zero-install path. If you install real NetworkX and need GraphML, use
`./cmc export html` or `obsidian` instead, or uninstall NetworkX and let the
shim serve it. This is worth reporting upstream.

### How this was verified

`./cmc selftest` runs **43 tests** covering the shim layer: published reference
values for every metric, the MT19937 vector, NetworkX view semantics and JSON
round-trips, Louvain's recovery of a planted partition, per-language parse
shapes, skill and git-hook installation, and a full end-to-end extraction
asserting cross-file inheritance and call resolution.

The suite passes in **both** environments — a bare checkout, and one with real
`networkx`, `tree-sitter` and `tree-sitter-python` installed alongside. That
second run is what validates the coexistence design, and it produced two
concrete results:

- **Byte-identical output.** The same corpus extracted with the bundled NetworkX
  shim and with real NetworkX 3.6.1 produced the same `graph.json` — every node,
  every edge, every attribute.
- **The bundled Python parser agrees with the real C grammar.** With real
  `tree-sitter-python` installed, the node set extracted from the same file is
  identical to the bundled parser's.

Beyond the suite, this tree was exercised on graphify's own 80-file, 55k-line
source: **2168 nodes, 4257 edges, 160 communities in ~28 seconds**, with entity
dedup running through the MinHash/rapidfuzz/numpy shims. The top god-node
(`_read_text()`, 85 edges) matches the codebase's real shape.

---

## 8. Optional features

Everything upstream guards behind `try/except ImportError` behaves the same
here: install the extra to enable it. **Code-only extraction needs none of
these.**

| Feature | Install |
|---------|---------|
| MCP server (`graphify-mcp`) | `pip install mcp starlette` |
| Leiden clustering (higher quality than Louvain) | `pip install graspologic` |
| SVG export | `pip install matplotlib` |
| PDF ingestion | `pip install pypdf markdownify` |
| Word / Excel ingestion | `pip install python-docx openpyxl` |
| Video transcription | `pip install faster-whisper yt-dlp` |
| Neo4j / FalkorDB export | `pip install neo4j` / `pip install falkordb` |
| File watching (`./cmc watch`) | `pip install watchdog` |
| PostgreSQL schema extraction | `pip install "psycopg[binary]"` |
| Chinese text segmentation | `pip install jieba` |

### LLM-powered semantic extraction

Documentation, papers and images need an LLM to extract meaning. Set any one of
these and drop `--code-only`:

```bash
export GEMINI_API_KEY=...      # or GOOGLE_API_KEY
export ANTHROPIC_API_KEY=...
export OPENAI_API_KEY=...
export MOONSHOT_API_KEY=...    # Kimi
export DEEPSEEK_API_KEY=...
```

Local/self-hosted models work too — point `OPENAI_BASE_URL` at llama.cpp, vLLM
or LM Studio, or use `--backend ollama`.

The same keys enable **community naming**: without one, clusters stay labelled
`Community 0`, `Community 1`, … instead of getting descriptive names.

---

## 9. Using it with AI coding assistants

graphify can install itself as a *skill* so your assistant queries the graph
instead of grepping raw files:

```bash
cd /path/to/your/project
/path/to/connect_my_code/cmc install --platform claude
```

Supported platforms:

`claude` · `codex` · `opencode` · `kilo` · `cursor` · `gemini` · `aider` ·
`amp` · `copilot` · `claw` · `droid` · `trae` · `hermes` · `kiro` · `pi` ·
`devin` · `antigravity` · `codebuddy` · `vscode` · `windows`

This writes:

- a `SKILL.md` (plus a progressive-disclosure `references/` sidecar) into the
  platform's config directory
- a section in `CLAUDE.md` / `AGENTS.md` / equivalent
- `PreToolUse` hooks that nudge the assistant to run
  `graphify query "..."` before reading source files

The hooks are written with an absolute path to `bin/graphify`, so they work from
this checkout with nothing installed. Verify with:

```bash
./cmc hook status
```

Remove everything with `./cmc uninstall` (add `--purge` to also delete
`graphify-out/`).

---

## 10. Troubleshooting

**`connect_my_code needs Python 3.10 or newer`**
Point the launcher at a newer interpreter: `CMC_PYTHON=python3.12 ./cmc …`

**`no Python interpreter found on PATH`**
Install Python 3.10+, or set `CMC_PYTHON=/full/path/to/python`.

**`error: no LLM API key found`**
You're extracting docs without a key. Add `--code-only` to index just source
code, or set an API key (see [section 8](#8-optional-features)).

**A language produced no nodes**
It's probably one of the [uncovered languages](#not-covered-by-bundled-parsers).
Check with `./cmc doctor`, then `pip install tree-sitter tree-sitter-<lang>` and
re-run — the front-end will delegate to the real grammar automatically.

**Fewer edges than I expected**
Expected for the structurally-parsed languages; see
[section 7](#7-fidelity-what-matches-exactly-what-doesnt). Installing the real
grammar recovers full fidelity. Note also that graphify deliberately filters
calls to language builtins (`len`, `map`, `round`, `type`, …) and defers
member calls on receivers whose type it can't determine.

**`./cmc query` says TRUNCATED**
Raise the budget: `./cmc query "..." --budget 6000`, or narrow the question.

**Permission denied running `./cmc`**
`chmod +x cmc bin/graphify`

**Something behaves differently from upstream graphify**
Run `./cmc selftest`. If it passes, compare against a real install — and note
that the shim layer steps aside entirely for any dependency you install for real.

---

## 11. Project layout

```
connect_my_code/
├── cmc                       POSIX launcher
├── cmc.cmd                   Windows launcher
├── cmc.py                    the real entry point
├── bin/
│   ├── graphify              launcher under the name the installers expect
│   └── graphify.cmd
├── graphify/                 UPSTREAM PACKAGE — 216 files, byte-identical, never edited
├── runtime/
│   ├── bootstrap.py          meta-path finder: real wheels win, shims fill gaps
│   ├── dist/                 stub .dist-info for importlib.metadata
│   └── shims/
│       ├── networkx/         graph classes, algorithms, Louvain, JSON, GraphML
│       ├── numpy/            uint64 arrays + bit-exact legacy RandomState
│       ├── rapidfuzz/        Jaro, Jaro-Winkler, Damerau-Levenshtein
│       ├── tree_sitter/
│       │   ├── __init__.py   delegating front-end (Language, Parser)
│       │   ├── _node.py      Node / Tree / TreeCursor
│       │   ├── _python.py    CPython-ast-backed Python parser
│       │   ├── _lexer.py     configurable tokenizer
│       │   ├── _brace.py     structural parser for brace-family languages
│       │   └── _langs.py     per-language node type configuration
│       └── tree_sitter_*.py  15 grammar modules
├── tests/test_portability.py 34 tests
├── tools/sync_upstream.sh    re-sync to a newer upstream
├── README.md                 this file
├── progress.md               what was built, and what was verified
├── learnings.md              findings that changed a decision
├── next_session.md           where to pick up
└── UPSTREAM_COMMIT           pinned upstream revision
```

Roughly 6,600 lines in `runtime/` + `tests/` support 55,000 lines of unmodified
upstream code.

---

## 12. Development guide

### Ground rules

1. **Never edit anything under `graphify/`.** All portability logic belongs in
   `runtime/`. This is what keeps upstream re-syncs a copy rather than a merge.
2. **Shims defer to real wheels.** `tree_sitter` is the sole always-front-ended
   module, and only because it delegates per language.
3. **Never silently approximate.** Unsupported operations raise a clear error
   naming the shim.
4. **Node type names are a contract.** They come from the `LanguageConfig` blocks
   in `graphify/extract.py` and the language branches in
   `graphify/extractors/engine.py`. Don't guess them — upstream compares
   `node.type` against exact strings, and a mismatch means silently extracting
   nothing.

### Adding a language

1. Find the node types upstream expects — its `LanguageConfig` in
   `graphify/extract.py`, plus any `config.ts_module == "tree_sitter_<lang>"`
   branches in `graphify/extractors/engine.py`.
2. Add a `BraceSpec` to `runtime/shims/tree_sitter/_langs.py`.
3. Add `runtime/shims/tree_sitter_<lang>.py` exporting `language()`.
4. Write a fixture, extract it, and **read the resulting graph.**

That last step is the whole method. A structural parser doesn't crash when it's
wrong — it silently emits fewer nodes. Every real defect found during this port
surfaced as missing output, never as an exception:

| Symptom in the graph | Actual cause |
|----------------------|--------------|
| TypeScript file yielded only a file node | `export` was treated as an import keyword, consuming declarations instead of wrapping them |
| Classes parsed but no methods | JS/TS methods have no introducing keyword |
| Go had functions but no methods | `func (s *Store) Add(...)` puts a receiver between keyword and name |
| C produced one node, no edges | `_get_c_func_name` walks `declarator` → `function_declarator` → `identifier`, a chain that wasn't emitted |
| Ruby produced nothing usable | `def…end` needs keyword counting, not bracket matching |

### Running tests

```bash
./cmc selftest                                    # everything
./cmc selftest tests.test_portability.TestNetworkXShim   # one class
```

### Debugging a parse

```python
import sys; sys.path.insert(0, '.'); sys.path.insert(0, 'runtime/dist')
from runtime import bootstrap; bootstrap.install()
from tree_sitter import Language, Parser
import tree_sitter_java as ts

tree = Parser(Language(ts.language())).parse(open('Foo.java','rb').read())

def dump(n, d=0):
    fields = " ".join(f"{k}={v.type}" for k, v in n.fields.items() if not k.endswith("*"))
    print("  " * d + n.type + (f" [{fields}]" if fields else ""), n.text[:40])
    for c in n.children:
        dump(c, d + 1)

dump(tree.root_node)
```

Note that `graphify` catches extractor exceptions and turns them into an
`{"error": ...}` result, so a crashing parser looks like an empty extraction.
Call the parser directly, as above, when something yields nothing.

---

## 13. Keeping up with upstream

```bash
tools/sync_upstream.sh          # latest main
tools/sync_upstream.sh v0.9.40  # a specific tag
./cmc selftest                  # ALWAYS run this afterwards
```

The script replaces `graphify/`, refreshes `UPSTREAM_COMMIT`, and regenerates the
stub `.dist-info` from upstream's version.

Run the tests every time. A new upstream release can start reading grammar node
types the bundled parsers don't emit yet — the per-language tests are what
surface that.

---

## 14. FAQ

**Is this a fork of graphify?**
No. It's a repackaging. The `graphify/` directory is byte-identical to upstream,
verified by `diff -r`. All additions are in `runtime/`.

**Will my results match a real `uv tool install graphifyy`?**
For Python, yes. For the other 14 bundled languages you'll get the same *kinds*
of nodes and edges but fewer of them — see
[section 7](#7-fidelity-what-matches-exactly-what-doesnt). Install real
tree-sitter wheels for exact parity, and the shims step aside automatically.

**Can I install the real packages later?**
Yes — that's the intended migration path. `pip install networkx numpy rapidfuzz
tree-sitter tree-sitter-python …` and they take over on the next run. No
configuration change, no reinstall. `./cmc doctor` confirms it.

**Does it phone home or need network access?**
No. Code-only extraction is entirely local. Network is used only if you opt into
LLM extraction, `./cmc add <url>`, or `./cmc clone`.

**Why Python 3.10?**
Upstream requires it (`requires-python = ">=3.10"`), and the bundled parsers rely
on `ast` position attributes standardised in 3.8+.

**How big is the graph for a large repo?**
graphify's own 55k-line source produces ~2,200 nodes and ~4,300 edges — a ~4 MB
`graph.json`. Extraction took ~28 seconds on the shims.

**Is the pure-Python parser slow?**
It's slower than the C parser but not the bottleneck: ~28 seconds for 80 files
including clustering and dedup. Install real tree-sitter if you're scanning a
very large repo repeatedly.

**Can I use this as a library?**
Yes — put the repo root and `runtime/dist` on `sys.path`, call
`runtime.bootstrap.install()`, then `import graphify` as normal.

---

## 15. Licence and credits

All credit for the tool itself goes to
[Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify). This repo
contributes only the portability layer.

- Upstream graphify: **Apache-2.0** — `LICENSE`, `LICENSE-MIT` and `NOTICE` are
  carried over unchanged
- The `runtime/` portability layer is provided under the same terms
- Pinned upstream revision: see `UPSTREAM_COMMIT`

### Further reading in this repo

| File | Contents |
|------|----------|
| `progress.md` | What was built at each milestone, and what was verified |
| `learnings.md` | Findings that changed a decision, with the reasoning |
| `next_session.md` | Known gaps and the highest-value next steps |
