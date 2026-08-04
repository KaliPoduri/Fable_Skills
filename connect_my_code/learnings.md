# Learnings — porting graphify to a zero-install layout

Findings worth keeping, recorded as they were established. Each one changed a
decision.

---

## 1. The dependency surface is far narrower than the dependency *count*

`pyproject.toml` lists 33 required distributions, which reads like an
unportable project. AST-walking every import told a different story:

| Package | Modules importing it |
|---------|---------------------|
| `numpy` | **1** (`_minhash.py`) |
| `rapidfuzz` | **1** (`dedup.py`) |
| `networkx` | 18 |
| `tree_sitter` | 18 |

29 of the 33 are tree-sitter *grammars*, each used by one extractor. So the real
work is three shims plus a parser layer — not 33 reimplementations.

**Lesson:** count import sites, not dependency-list entries, before calling a
project unportable.

## 2. No tree-sitter `Query` API is used anywhere

Grepping for the tree-sitter API surface actually exercised:

```
type 804 · child_by_field_name 302 · parent 208 · start_point 178 · is_named 79
start_byte 30 · end_byte 25 · text 24 · root_node 24 · walk 11
next_named_sibling 2 · has_error 1 · children_by_field_name 1 · child_count 1
```

Zero uses of `Query`, `QueryCursor`, or S-expression patterns — graphify walks
trees by hand. That collapses the compatibility target from "implement
tree-sitter's query engine" to "produce node objects with ~14 members and the
right `type` strings".

**Lesson:** the size of a C dependency is not the size of its used surface. This
single finding is what made milestone 5 tractable.

## 3. tree-sitter is a *hard* requirement, unlike the others

`extract.py:_check_tree_sitter_version()` raises `ImportError` outright when
tree-sitter is absent — there is no soft-degrade path. Individual grammars *do*
degrade (`extractors/elixir.py` returns `{"nodes": [], "edges": [],
"error": "..."}`), but the core parser does not.

So a shim is mandatory for the tool to run at all; leaning on upstream's
existing fallbacks was never an option.

## 4. Confirming the premise beats assuming it

`python3 -c "import networkx, numpy, rapidfuzz, tree_sitter"` failed on every
one in the target environment. Upstream graphify genuinely could not start here.
That is the whole justification for the port, and it took one command to
establish rather than reasoning about it.

## 5. Shim precedence should be "real wins", and that is free

Putting the shims behind a `sys.meta_path` finder that defers whenever
`PathFinder.find_spec` succeeds gets three properties at once:

- real wheels are preferred automatically, per module;
- migration to the real thing is "install it", with no config change;
- shim code is only ever exercised where it is genuinely needed.

Prepending `runtime/shims` to `sys.path` would have inverted this and silently
shadowed better implementations.

**Caveat found while designing it:** a *mixed* environment breaks naive
per-module gating. Real `tree_sitter` + shim `tree_sitter_kotlin` would hand a
Python marker object to a C `Language()` constructor. Hence `tree_sitter` is
always shimmed as a thin front-end that delegates per language, rather than
being gated like the rest.

## 6. Bit-exactness in the PRNG is worth the effort

`_minhash.py` seeds `RandomState(1)` to build its MinHash hash family. Those
coefficients decide LSH banding → which label pairs are compared → which
entities `dedup.py` merges → the node set in `graph.json`. An "equivalent
quality" PRNG would silently produce a different graph.

Three details had to be right, and the first is easy to get wrong:

1. NumPy's integer seeding is randomkit's `mt19937_seed`, **not** the reference
   `init_genrand` — it stores the running seed *before* advancing and adds
   `pos + 1` each step.
2. `mt19937_next64` draws the **high** 32-bit word first.
3. `randint` uses masked rejection sampling with `rng = high - low - 1` and
   accepts `value <= rng`.

Validated the twist/temper against the canonical `init_genrand(5489)` vector so
the core was known-good before layering NumPy's seeding on top.

## 7. Some fidelity questions turn out not to matter — check before agonising

RapidFuzz's Jaro-Winkler applies the prefix bonus only above a 0.7 similarity
threshold; some implementations skip that gate. Rather than guess, bound the
impact: `dedup.py` only ever compares against 92.0 and 97.0, and a Jaro of 0.7
with the maximum possible bonus reaches just 0.82. **Both variants agree on
every decision graphify makes.**

Same shape of answer for `simple_cycles` enumeration order — `analyze.py` sorts
by length and canonicalises rotations afterwards, so only the early-`break`
cutoff could differ.

**Lesson:** when exact parity is expensive, compute whether the divergence can
reach an observable output before paying for it.

## 8. NetworkX's views are dual-natured, and graphify uses both natures

`G.nodes` / `G.edges` / `G.degree` are each simultaneously iterable *and*
callable, and `G.degree(n)` returns a scalar while `G.degree()` returns pairs.
graphify relies on all of it, plus write-through attribute access
(`H.nodes[n][k] = v` in `export.py` mutates the live graph).

Reproducing NetworkX's internal `_node`/`_adj`/`_pred`/`_succ` layout made these
fall out naturally instead of needing special cases. Undirected edges share one
attribute dict between both directions — matching NetworkX and making
write-through work.

## 9. `subgraph()` as a copy is a safe superset

NetworkX returns a frozen, read-only view. Returning an independent copy accepts
every operation a view would; it can only diverge if a caller mutates the parent
and expects the child to track — which a read-only view forbids anyway.

## 10. A fake `.dist-info` restores version reporting with no source edits

`graphify/__main__.py` reads `importlib.metadata.version("graphifyy")` and falls
back to the string `"unknown"`. Shipping
`runtime/dist/graphifyy-0.9.32.dist-info/METADATA` and putting that directory on
`sys.path` makes the real version resolve — keeping `graphify/` byte-identical
while `--version` and the skill version stamps stay correct.
