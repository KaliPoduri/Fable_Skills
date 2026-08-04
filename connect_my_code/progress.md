# Progress — connect_my_code

Portable, zero-install replica of [graphify](https://github.com/Graphify-Labs/graphify).

- **Upstream pinned at:** `00efd6e7969837ae4a9f11d8d504dcd3b20b09df` (v0.9.32)
- **Goal:** `git clone` → `./cmc <command>`. No `uv`, no `pip`, no `npm`, no build step.
- **Last updated:** milestone 4 (networkx shim green)

---

## Status board

| # | Milestone | State |
|---|-----------|-------|
| 1 | Analyze graphify architecture + dependency surface | ✅ done |
| 2 | Repo skeleton + zero-install launchers | ✅ done |
| 3 | `rapidfuzz` + `numpy` shims | ✅ done |
| 4 | `networkx` shim | ✅ done |
| 5 | `tree_sitter` shim + language parsers | ⏳ in progress |
| 6 | End-to-end parity verification | ⬜ pending |

---

## The core design decision

Upstream graphify is installed with `uv tool install graphifyy`, which pulls
**33 required wheels** — `networkx`, `numpy`, `rapidfuzz`, `tree-sitter` and 29
compiled tree-sitter grammars. Those grammars are per-platform C extensions, so
"vendor the wheels" can never be portable.

Instead: **keep the upstream package byte-identical and supply its dependencies
from a bundled pure-standard-library shim layer.**

```
cmc / cmc.cmd / cmc.py     launcher — picks an interpreter, no install
runtime/bootstrap.py       meta-path finder: real wheels win, shims fill gaps
runtime/shims/*            pure-stdlib implementations
runtime/dist/*.dist-info   makes importlib.metadata.version("graphifyy") resolve
graphify/                  UNMODIFIED upstream package (216 files, byte-identical)
```

### Why the shim layer is a meta-path finder, not a `sys.path` entry

`runtime/shims/` is deliberately **never** put on `sys.path`. A `ShimFinder`
appended to `sys.meta_path` claims a module name only after confirming the
ambient environment cannot supply it. Consequences:

- A user who already has real `networkx`/`numpy`/`rapidfuzz` installed keeps
  them, per module, with zero configuration.
- Migration is a no-op: install the real wheels any time and they take over.
- `tree_sitter` is the single exception — its shim always loads, because it is a
  *delegating front-end* that hands off to the real C parser per language when a
  real grammar is present. That is what lets a mixed environment (real
  tree-sitter + real tree-sitter-python, but no tree-sitter-kotlin) use the C
  parser for Python and the bundled pure parser for Kotlin in one run.

### Why upstream sources stay byte-identical

All portability logic lives in `runtime/`. Nothing under `graphify/` is edited.
Re-syncing to a newer upstream is therefore a directory copy, not a merge.

---

## Dependency inventory

Established by AST-walking every import in the upstream package.

**Required** (graphify will not start without these):

| Module | Upstream use | Shim status |
|--------|--------------|-------------|
| `networkx` | 18 modules — graph containers, JSON round-trip, Louvain, algorithms | ✅ done |
| `numpy` | 1 module (`_minhash.py`) — uint64 MinHash sketches | ✅ done, bit-exact |
| `rapidfuzz` | 1 module (`dedup.py`) — Jaro / Jaro-Winkler / Damerau-Levenshtein | ✅ done, exact |
| `tree_sitter` + 29 grammars | 18 modules — all code extraction | ⏳ milestone 5 |

**Optional** (already guarded by `try/except ImportError` upstream, so a
zero-install checkout degrades exactly the way an incomplete `pip` install does):
`mcp`, `starlette`, `uvicorn`, `pydantic`, `neo4j`, `falkordb`, `pypdf`,
`markdownify`, `watchdog`, `graspologic`, `matplotlib`, `python-docx`,
`openpyxl`, `faster_whisper`, `yt_dlp`, `openai`, `tiktoken`, `boto3`,
`anthropic`, `psycopg`, `jieba`, `yaml`, `tomli`.

---

## What is verified so far

Everything below was executed, not assumed.

**`numpy` shim** — `_minhash.py` runs unmodified.
- MT19937 twist/temper validated against the canonical `init_genrand(5489)`
  vector: `[3499211612, 581869302, 3890346734, 3586334585, 545404204]` ✅
- Seeding reproduces randomkit's `mt19937_seed` (not the reference
  `init_genrand`), and `next_uint64` draws the high word first — both required
  for coefficient parity with real NumPy.
- LSH band/row search returns `b=25, r=5` for `threshold=0.5, num_perm=128`.

**`rapidfuzz` shim** — all published reference values match:

| pair | Jaro | Jaro-Winkler |
|------|------|--------------|
| MARTHA / MARHTA | 0.944444 ✅ | 0.961111 ✅ |
| DWAYNE / DUANE | 0.822222 ✅ | 0.840000 ✅ |
| DIXON / DICKSONX | 0.766667 ✅ | 0.813333 ✅ |

Damerau-Levenshtein is the **unrestricted** variant (`CA`→`ABC` = 2, not the
OSA answer of 3), matching RapidFuzz.

**`networkx` shim** — every call site graphify makes, exercised:
node/edge/degree views incl. `data=True` and `keys=True`, attribute mutation
through `G.nodes[n][k] = v`, node-link JSON round-trip preserving attributes for
both `Graph` and `MultiDiGraph`, `shortest_path` + `NetworkXNoPath` +
`NodeNotFound`, Louvain (recovers the planted 3-community structure, and
`inspect.signature` exposes `max_level` as `graphify.cluster` requires),
betweenness, edge-betweenness, bounded `simple_cycles`, `compose`,
`relabel_nodes`, GraphML write.

---

## Next up — milestone 5

See `next_session.md`.
