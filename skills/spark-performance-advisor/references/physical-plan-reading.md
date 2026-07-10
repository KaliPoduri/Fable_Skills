# Reading Spark physical plans — for first-timers

Sources: Apache Spark 3.5.8 docs — EXPLAIN statement
(https://spark.apache.org/docs/3.5.8/sql-ref-syntax-qry-explain.html),
Hints (https://spark.apache.org/docs/3.5.8/sql-ref-syntax-qry-select-hints.html),
Performance Tuning (https://spark.apache.org/docs/3.5.8/sql-performance-tuning.html),
PySpark 3.5.8 DataFrame.explain API, and the PySpark "Bug Busting" user
guide (4.1.2). All verified 2026-07-10. Defaults quoted are the 3.5.x
documented values; version differences are flagged inline.

## What a physical plan is

A physical plan is the exact recipe Spark will use to execute a query:
which files it reads, how it moves data between machines, and which join
algorithm it picks. The SQL you wrote is the *what*; the physical plan is
the *how*. Slow jobs are diagnosed from the *how*.

## Getting a plan (pick whichever the user can do)

- **PySpark / Scala code:** call `.explain()` on the DataFrame.
  `df.explain()` prints the physical plan only. Better:
  `df.explain(mode="formatted")` prints a readable outline plus per-node
  details. All modes (available since Spark 3.0, so on every 3.x):
  `simple` (physical plan only), `extended` (logical + physical plans),
  `codegen` (generated code), `cost` (plan statistics if available),
  `formatted` (outline + node details). Printing a plan does NOT run
  the job — it is safe.
- **SQL:** `EXPLAIN <query>` or
  `EXPLAIN [EXTENDED | CODEGEN | COST | FORMATTED] <query>`.
- **Spark UI:** SQL / DataFrame tab → click the query → the "Details"
  link at the bottom shows the logical plans and the physical plan.
  This is the only way to see the plan of a job you cannot rerun (via
  the History Server for finished jobs — see
  references/evidence-gathering.md).

## Reading order

Plan text starts with `== Physical Plan ==` and is a tree drawn with
`+-` branches. **Read bottom-up**: the deepest indented nodes (the
scans) run first and feed the nodes above them. The top node produces
the final result.

## AdaptiveSparkPlan — the wrapper you will see on Spark 3

With AQE (Adaptive Query Execution — Spark re-optimizes the plan at
runtime using real statistics; on by default since Spark 3.2, opt-in via
`spark.sql.adaptive.enabled` on 3.0–3.1) the whole plan is wrapped in:

```
== Physical Plan ==
AdaptiveSparkPlan isFinalPlan=false
+- ...
```

`isFinalPlan=false` means: this is the starting plan, and Spark may
still change it while running (e.g., swap a sort-merge join for a
broadcast join once it sees one side is small). The plan that actually
ran is shown in the Spark UI's SQL / DataFrame tab after execution — for
tuning, prefer that final plan over the pre-run printout.

## Exchange = shuffle (the expensive part)

`Exchange` nodes move data between machines — a shuffle (data
reshuffling between machines, written to disk and sent over the
network). Shuffles are usually the most expensive operations in a job,
so count the Exchanges first.

```
+- Exchange hashpartitioning(_1#6L, 200), ENSURE_REQUIREMENTS, [plan_id=41]
```

- `hashpartitioning(col, 200)` — rows are routed by hash of `col` into
  **200** buckets; that number is the shuffle partition count
  (`spark.sql.shuffle.partitions`, default 200). If you see 200 on a
  huge job, nobody tuned it.
- `Exchange RoundRobinPartitioning(100)` — from `repartition(100)` in
  code or a `REPARTITION(100)` hint: rows dealt evenly into 100
  buckets, no key.
- `BroadcastExchange` — NOT a shuffle: one small table is copied whole
  to every executor (worker process) so the big table never moves.

## Sort

`Sort` nodes appear (a) feeding a SortMergeJoin, which needs both sides
sorted, and (b) from ORDER BY / window functions. A big explicit Sort
that exists only to enable a join is a hint that a different join
strategy might be cheaper.

## Join operators — which one you have and when to worry

| Operator in plan | What it does (plain) | When it appears | Red flag? |
|---|---|---|---|
| `BroadcastHashJoin` | Copies the small side to every executor; big side never shuffles | One side under the broadcast threshold (`spark.sql.autoBroadcastJoinThreshold`, default 10 MB), or a BROADCAST hint | Good for small dimension tables. Red flag if the "small" side is actually large: slow broadcast, `spark.sql.broadcastTimeout` (default 300 s) pressure, memory pressure |
| `SortMergeJoin` | Shuffles BOTH sides by the join key, sorts, then merges | The default for large equi-joins (joins with `=` conditions) | Normal for big-to-big joins. Red flag when one side is small enough to broadcast, or when skew makes a few partitions huge |
| `ShuffledHashJoin` | Shuffles both sides, builds a hash table on the smaller | SHUFFLE_HASH hint; AQE can convert to it on 3.2+ | Fine; watch the "data size of build side" metric in the UI |
| `BroadcastNestedLoopJoin` | Compares row pairs without a hash/sort — broadcast one side, loop | Joins with NO equality condition (e.g., `ON a.x > b.y`) | RED FLAG on large inputs — often the whole problem. Fix: add an equality key to the join condition |

Join strategy hints exist for all of these (verified in 3.1 and 3.5
docs): `BROADCAST`, `MERGE` (sort-merge), `SHUFFLE_HASH`,
`SHUFFLE_REPLICATE_NL` (shuffle-and-replicate nested loop). Priority
when several apply: BROADCAST > MERGE > SHUFFLE_HASH >
SHUFFLE_REPLICATE_NL. A hint is a suggestion — Spark ignores it when the
strategy does not support the join type. The BROADCAST hint gives a
broadcast hash join when there is an equi-join key, otherwise a
broadcast nested loop join.

## Scan nodes — is Spark reading too much?

File-based reads appear as `FileScan`:

```
+- FileScan parquet default.t[name#29,c#30] Batched: true, DataFilters: [],
   Format: Parquet, Location: CatalogFileIndex[file:/spark/spark-warehouse/t],
   PartitionFilters: [], PushedFilters: [], ReadSchema: struct<name:string>
```

What each field tells you:

- `ReadSchema` — the columns actually read. A wide list on a query that
  needs 3 columns means `SELECT *` waste.
- `PartitionFilters` — filters applied to partition columns (the folder
  structure of the table), so whole folders are skipped without
  reading. If the query filters on a partition column but this shows
  `[]`, partition pruning is NOT happening — a top red flag.
- `PushedFilters` — simple filters pushed into the file reader so
  non-matching data is skipped early. `[]` despite a simple WHERE on
  scanned columns is worth investigating (see the pushdown playbook).
- `Scan ExistingRDD` — data comes from an in-memory RDD, not files; no
  file pruning is possible there.

## WholeStageCodegen — the `*` and `(N)` marks

Spark fuses chains of operators into single generated functions
("whole-stage code generation") for speed. In plan text, fused nodes
carry a `*` prefix (e.g., `*(2) HashAggregate(...)`), and
`EXPLAIN FORMATTED` shows `[codegen id : 1]` per node — nodes sharing a
codegen id run as one fused function. In the UI the DAG groups them
into WholeStageCodegen blocks. This is informational: presence is the
fast path; you rarely tune it directly.

## What to look for first (in order)

1. `AdaptiveSparkPlan`? Note `isFinalPlan`; on the UI prefer the final
   executed plan.
2. Count `Exchange` nodes — each is a shuffle; can any be removed
   (broadcast a small side, filter earlier)?
3. Name every join operator. Any `BroadcastNestedLoopJoin` on large
   inputs? Any `SortMergeJoin` where one side is tiny?
4. Check every `FileScan`: `ReadSchema` width, `PartitionFilters: []`,
   `PushedFilters: []`.
5. Check the shuffle partition count inside `hashpartitioning(...)` —
   default 200 is rarely right at scale.
6. Then cross-check against Spark UI numbers ("number of output rows"
   per operator, task-time spread) before concluding anything — the
   plan says what Spark did, the UI says what it cost.
