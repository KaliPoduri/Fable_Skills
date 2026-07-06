# Reading execution plans — cross-engine

Sources: PostgreSQL 18 docs §14.1 "Using EXPLAIN"
(https://www.postgresql.org/docs/current/using-explain.html) and MySQL 8.4
Reference Manual §10.8.2 "EXPLAIN Output Format"
(https://dev.mysql.com/doc/refman/8.4/en/explain-output.html), both
verified 2026-07-06; cross-engine framing per use-the-index-luke.com.
SQL Server/Oracle operator names are translations — confirm locally when
precision matters.

## Universal reading method

1. **Estimated vs actual.** An estimated plan (EXPLAIN) shows what the
   optimizer intends; an actual plan (EXPLAIN ANALYZE / actual execution
   plan) shows real row counts and timing. Prefer actual plans; ANALYZE
   executes the query, so never use it on INSERT/UPDATE/DELETE without a
   wrapping transaction you roll back.
2. **Find where the work is.** Look for the node with the largest actual
   time or cost share, not the top node. In tree-shaped plans, children
   feed parents; the innermost expensive node is usually the root cause.
3. **Compare estimated rows to actual rows.** A 100x+ mismatch means the
   optimizer chose the plan on wrong assumptions — usually stale
   statistics, correlated columns, or non-SARGable predicates hiding
   selectivity. Fix statistics/predicates before micro-tuning the plan.
4. **Name the access path per table.** Full scan, index range scan,
   index-only/covering access, or per-row lookup. Then ask: is this path
   reasonable for the row counts involved? A full scan over a small table
   is fine; a per-row lookup executed a million times is not.
5. **Check join order and strategy** (see below), then sorts,
   temporary/spill operations, and repeated subplan executions.

## Access paths (vocabulary per engine)

| Concept | PostgreSQL | MySQL (type column) | SQL Server | Oracle |
|---|---|---|---|---|
| Full table scan | Seq Scan | ALL | Table Scan / Clustered Index Scan | TABLE ACCESS FULL |
| Index range access | Index Scan | range / ref | Index Seek | INDEX RANGE SCAN |
| Single-row by unique key | Index Scan (unique) | const / eq_ref | Index Seek (unique) | INDEX UNIQUE SCAN |
| Index satisfies query alone | Index Only Scan | "Using index" in Extra | Index Seek, no lookup (covering) | INDEX FAST FULL SCAN / no table access |
| Fetch row after index hit | Heap Fetches (in Index Only Scan) / implicit | — (always via PK in InnoDB secondary) | Key Lookup / RID Lookup | TABLE ACCESS BY INDEX ROWID |
| Bitmap combination | Bitmap Index Scan + Bitmap Heap Scan | index_merge | — | BITMAP CONVERSION |
| Walk whole index in order | Index Scan (full) | index | Index Scan | INDEX FULL SCAN |

Danger signs:
- Full scan on a large table driven by a selective WHERE → missing or
  unusable index (check SARGability first).
- Many executions ("loops=N" in PostgreSQL, high Key Lookup count in SQL
  Server) of a lookup node → lookup storm; consider a covering index or a
  different join strategy.
- MySQL `type: ALL` with a non-NULL `possible_keys` → the index exists
  but was rejected; check predicate form, selectivity, and implicit casts.

## Join strategies

- **Nested loop:** for each outer row, probe the inner side. Great when
  the outer side is small and the inner probe is an index seek. Terrible
  when the outer side is large and the inner side is scanned per row.
- **Hash join:** build a hash table from one side, probe with the other.
  Good for large unsorted inputs with equality joins; watch for memory
  spills. (MySQL supports hash join from 8.0.18; PostgreSQL/SQL Server/
  Oracle native.)
- **Merge join:** both inputs sorted on the join key, merged in one pass.
  Wins when inputs are already ordered (by index); a plan that adds two
  big explicit Sorts to enable a merge join may indicate missing indexes.

Reviewer questions: is the small side the outer/build side? Is the join
predicate an equality on indexed columns? Is a per-row nested loop being
fed by thousands of outer rows because of a bad row estimate?

## MySQL EXPLAIN specifics (8.4, §10.8.2)

Columns: id, select_type, table, partitions, type, possible_keys, key,
key_len, ref, rows, filtered, Extra. JSON names include select_id,
access_type, rows.

Join types from best to worst (abridged): system, const, eq_ref, ref,
fulltext, ref_or_null, index_merge, range, index, ALL.

Extra values that matter:
- `Using index` — covering access, no row fetch needed (good).
- `Using index condition` — index condition pushdown (usually good).
- `Using where` — post-access filtering; fine unless it discards most
  rows (then the access path is too broad).
- `Using filesort` — an explicit sort will run; check if an index could
  deliver the order.
- `Using temporary` — intermediate materialization (GROUP BY/DISTINCT/
  UNION); often removable with better indexes or rewrites.

Prefer `EXPLAIN FORMAT=JSON` (adds cost detail) or `EXPLAIN ANALYZE` for
actual timing.

## PostgreSQL EXPLAIN specifics (18, §14.1)

- Costs read as `cost=startup..total rows=N width=B`; with ANALYZE:
  `actual time=start..total rows=N loops=L`. Total contribution of a node
  = actual time x loops.
- `EXPLAIN (ANALYZE, BUFFERS)` shows shared hit/read counts — high
  `read` = real IO; high buffers overall = wide scans.
- `Rows Removed by Filter` large relative to rows returned → the access
  path fetched far more than needed; index the filter column(s).
- Sort nodes report method: `Sort Method: external merge Disk: NNkB`
  means the sort spilled — consider index-provided order or more
  work_mem (setting changes belong to the platform team).
- Index Only Scan with high `Heap Fetches` → visibility map not covering;
  VACUUM matters, or the "index-only" benefit is illusory.
- Stale estimates → run ANALYZE on the table; re-check before deeper
  tuning.

## SQL Server and Oracle notes ([lower-confidence] terminology)

- SQL Server: read graphical actual plans right-to-left. Warnings on
  operators (yellow triangles) flag spills and implicit conversions —
  `CONVERT_IMPLICIT` on a column side kills index seeks. Key Lookup with
  a high execution count suggests adding included columns (covering
  index via INCLUDE). `SET STATISTICS IO ON` logical reads are the
  comparable IO metric.
- Oracle: generate plans with `EXPLAIN PLAN FOR ...` +
  `DBMS_XPLAN.DISPLAY`, or `DBMS_XPLAN.DISPLAY_CURSOR` for actuals.
  TABLE ACCESS FULL on large tables with selective predicates and
  INDEX RANGE SCAN + TABLE ACCESS BY INDEX ROWID storms are the analogues
  of the patterns above.
