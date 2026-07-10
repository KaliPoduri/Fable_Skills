# Diagnosis playbooks — slow Spark jobs

Sources: Apache Spark 3.5.8 docs — Performance Tuning
(https://spark.apache.org/docs/3.5.8/sql-performance-tuning.html),
Web UI (https://spark.apache.org/docs/3.5.8/web-ui.html), Tuning Guide
(https://spark.apache.org/docs/3.5.8/tuning.html), Configuration
(https://spark.apache.org/docs/3.5.8/configuration.html); archived 3.1.3
docs for version deltas. Verified 2026-07-10.

How to use: match the symptom, confirm with the listed evidence before
concluding, fix SQL/code first and configs second (exact parameters,
defaults, and scopes in references/config-table.md). Every playbook has
version notes — check them against the user's exact minor version. If
the confirming evidence is absent, ask for it (see
references/evidence-gathering.md) instead of guessing.

---

## Playbook 1: Data skew

**Symptom in plain words.** The job sits at "199/200 tasks done" for a
long time; one stage takes forever because a handful of tasks run far
longer than the rest.

**What confirms it.**
- Spark UI → Stages tab → the slow stage → task list: sort by Duration;
  the slowest tasks run many times longer than the typical task, and
  their "Shuffle Read Size / Records" is much larger than the others'.
- "Aggregated metrics by executor" on the same page: one or two
  executors did most of the work.
- Plan: a `SortMergeJoin` (or aggregation) fed by
  `Exchange hashpartitioning(<key>, N)` — hash partitioning sends every
  row with the same key to the same task, so one giant key = one giant
  task.

**Why it happens (plain).** A few key values own most of the rows —
NULLs, a default/placeholder ID, one huge customer. Hashing by key puts
all of them in one bucket.

**Fix options (SQL/code first).**
1. Find the heavy keys (user runs in non-prod):
   `SELECT <key>, COUNT(*) c FROM <t> GROUP BY <key> ORDER BY c DESC LIMIT 20`.
2. NULL or junk keys: filter them out before the join, or handle them
   separately (they never match anyway in an inner join).
3. Broadcast the small side (`/*+ BROADCAST(dim) */`): no shuffle of
   the big side means key distribution stops mattering.
4. Salting (last resort, works everywhere): add a random suffix 0..N-1
   to the key on the big side; duplicate each small-side row N times,
   once per suffix; join on the salted key. N ≈ how many pieces the
   giant key must split into. This rewrites the query — keep results
   identical and say so.
5. AQE skew-join handling: with AQE on, Spark splits oversized
   partitions of a sort-merge join automatically
   (`spark.sql.adaptive.skewJoin.enabled`, default true). It triggers
   when a partition is both larger than 5x the median partition size
   (`skewedPartitionFactor`, default 5.0) AND larger than
   `skewedPartitionThresholdInBytes` (default 256MB). If the user's
   skewed partitions sit below these bars, lower the thresholds.

**Version notes.** AQE is on by default only since 3.2; on 3.0–3.1 set
`spark.sql.adaptive.enabled=true` first. Skew-join optimization exists
since 3.0 and handles sort-merge joins.
`spark.sql.adaptive.forceOptimizeSkewedJoin` (allow skew handling even
when it adds an extra shuffle) exists since 3.3, default false.

---

## Playbook 2: Spill (memory to disk)

**Symptom in plain words.** A stage is slow and the UI shows "Shuffle
spill" — tasks ran out of memory room and parked data on disk, which is
much slower than RAM.

**What confirms it.**
- Stages tab → slow stage: non-zero "Shuffle spill (memory)" (size of
  the data in memory before spilling) and "Shuffle spill (disk)" (size
  written to disk). Zero spill = this playbook does not apply.
- Often long "GC time" (garbage collection — the JVM reclaiming memory)
  on the same tasks.
- SQL tab node metrics can show "spill size" on sort/aggregate/join
  operators.

**Why it happens (plain).** Each task gets a share of its executor's
memory; when a sort/aggregation/join working set exceeds it, Spark
spills to disk and the task crawls.

**Fix options.**
1. Make partitions smaller so each task holds less: raise
   `spark.sql.shuffle.partitions`, or with AQE let coalescing target a
   size (`spark.sql.adaptive.advisoryPartitionSizeInBytes`, default
   64MB — but see the 3.2+ `parallelismFirst` note in the config
   table).
2. Shrink the data earlier: select only needed columns before the wide
   operation, filter before joining, drop exploding joins (check
   "number of output rows" of the join vs its inputs — a join that
   multiplies rows may be missing a key).
3. If only a few tasks spill → that is skew; use Playbook 1.
4. Give each task more memory: raise `spark.executor.memory`, or lower
   `spark.executor.cores` (an executor runs one task per core by
   default — `spark.task.cpus` default 1 — all sharing the executor's
   memory, so fewer concurrent tasks = more memory each).
5. Last resort only: `spark.memory.fraction` / `storageFraction`. The
   tuning guide says typical users should not need to adjust them.

**Version notes.** All configs here exist across 3.0–3.5; the AQE items
require AQE on (default only since 3.2).

---

## Playbook 3: Partition count (too many / too few)

**Symptom in plain words.** Either thousands of tiny tasks that each do
almost nothing (overhead eats the runtime), or a handful of huge tasks
while most of the cluster sits idle.

**What confirms TOO MANY.**
- Stages tab: task count in the tens of thousands, per-task Duration
  tiny, "Scheduler Delay" / "Task Deserialization Time" comparable to
  actual work; shuffle read/write per task in KBs.

**What confirms TOO FEW.**
- Stages tab: task count far below total cluster cores (Executors tab
  shows cores); each task processes hundreds of MBs to GBs and runs for
  minutes while other cores are idle.

**Fix options.**
1. Set `spark.sql.shuffle.partitions` (default 200) so that typical
   shuffle partitions land near
   `spark.sql.adaptive.advisoryPartitionSizeInBytes` (default 64MB) —
   rough sizing: total shuffled bytes / 64MB, rounded to a multiple of
   the cluster's cores. The tuning guide's general rule is 2–3 tasks
   per CPU core.
2. With AQE, partition coalescing merges small shuffle partitions
   automatically (`spark.sql.adaptive.coalescePartitions.enabled`,
   default true) — the cheap fix for "too many" on the shuffle side.
   On 3.2+ note: `coalescePartitions.parallelismFirst` (default true)
   makes Spark coalesce only down to `minPartitionSize` (1MB) to keep
   parallelism, ignoring the 64MB advisory size — set it to false to
   actually target the advisory size.
3. In code: `repartition(n)` (full shuffle, even output) vs
   `coalesce(n)` (merges partitions without a full shuffle; only
   reduces count). Define both when advising.
4. "Too few" right after reading files: check
   `spark.sql.files.maxPartitionBytes` (default 128MB) — huge files
   split into read tasks of at most this size.

**Version notes.** On 3.0–3.1 there is no `minPartitionSize` /
`parallelismFirst`; the floor is `coalescePartitions.minPartitionNum`
(default: the cluster's default parallelism).

---

## Playbook 4: Join strategy problems

**Symptom in plain words.** A join dominates the runtime: a big
shuffle-and-sort for a join against a tiny table, a broadcast that takes
minutes or times out, or a join with no `=` condition grinding forever.

**What confirms it.**
- Plan: which join operator (see references/physical-plan-reading.md) —
  `SortMergeJoin` against a side the user knows is small;
  `BroadcastNestedLoopJoin` on large inputs; `BroadcastExchange`
  feeding a join when the "small" side is not small.
- UI SQL tab: join node metrics — e.g., ShuffledHashJoin's "data size
  of build side" and "time to build hash map"; Exchange's "shuffle
  bytes written".
- Timeout errors mentioning `spark.sql.broadcastTimeout` (default
  300 s). If the job actually FAILS on this, triage says etl-assistant;
  stay here only while the user's question is why it is slow / how to
  tune the join.

**Fix options.**
1. Small side under ~10MB but Spark still sort-merge joins: Spark's
   size estimate is likely wrong (fresh table, no stats). Add
   `/*+ BROADCAST(alias) */` — the hinted side is broadcast regardless
   of `spark.sql.autoBroadcastJoinThreshold` (default 10MB). Or raise
   the threshold job-scoped, cautiously: everything under it gets
   broadcast, and broadcasting something big can stall the job.
2. Broadcast slow or timing out: first ask if the broadcast side is
   really small. If not, remove the hint / lower the threshold (-1
   disables automatic broadcasting entirely) and let it sort-merge
   join. Only raise `spark.sql.broadcastTimeout` when the side is
   legitimately small and the cluster was just busy.
3. `BroadcastNestedLoopJoin`: the join has no equality condition. Add
   one (even a coarse bucketing equality) and keep ranges as residual
   filters — this usually beats any config change by far.
4. On 3.2+ with AQE: `spark.sql.adaptive.autoBroadcastJoinThreshold`
   sets a runtime-statistics threshold for converting sort-merge join
   to broadcast (defaults to the static threshold). AQE also converts
   sort-merge join to broadcast automatically when a side turns out
   small at runtime.
5. Medium-sized both sides where the Sorts hurt: try a SHUFFLE_HASH
   hint (skips sorting; builds a hash table on the smaller side).

**Version notes.** Join hints (MERGE, SHUFFLE_HASH,
SHUFFLE_REPLICATE_NL, plus BROADCAST) verified present in 3.1 and 3.5
docs. `spark.sql.adaptive.autoBroadcastJoinThreshold` exists since
3.2. AQE sort-merge-to-shuffled-hash conversion is gated by
`spark.sql.adaptive.maxShuffledHashJoinLocalMapThreshold` (since 3.2,
default 0 = effectively off).

---

## Playbook 5: Small-files problem

**Symptom in plain words.** The job spends most of its time just
reading the input, and the input directory holds a huge number of tiny
files (thousands of KB-sized files instead of hundreds of ~100MB ones).

**What confirms it.**
- Ask the user to list the source directory: file count and typical
  file size (e.g., `hdfs dfs -count` / `-du -h` on the path — user
  runs it, not you).
- Stages tab: the scan stage has a very large task count while total
  input bytes are modest; per-task input is tiny.

**Why it happens (plain).** Each file costs time to open and list;
Spark charges every file an accounting cost of
`spark.sql.files.openCostInBytes` (default 4MB) — millions of opens
dwarf the actual reading.

**Fix options.**
1. Fix the producer (best, durable): the upstream job should write
   fewer, bigger files — `repartition(n)` before the write so files
   land near `spark.sql.files.maxPartitionBytes` (default 128MB), the
   size Spark packs into one read task. Changing another team's job is
   advise-only: name the change, hand it to that job's owner.
2. Compact existing data: a one-off job that reads the directory and
   rewrites it with fewer files (same idea; needs data-owner
   approval and a non-prod trial).
3. Reader-side relief (helps, does not cure):
   `spark.sql.files.maxPartitionBytes` packs multiple small files into
   one task up to 128MB; raising `spark.sql.files.openCostInBytes`
   makes Spark pack more small files per task.

**Version notes.** Both `spark.sql.files.*` settings exist since 2.0 —
present on every 3.x.

---

## Playbook 6: Missing filter/partition pushdown

**Symptom in plain words.** The query only needs a slice (one day, one
country) but Spark reads the entire table.

**What confirms it.**
- Plan `FileScan`: `PartitionFilters: []` even though the WHERE clause
  filters a partition column; `PushedFilters: []` even though there are
  simple predicates on scanned columns; `ReadSchema` far wider than the
  columns used.
- Stages tab: input size of the scan stage ≈ whole table, not the
  expected slice.
- SQL tab: the Scan node's "number of output rows" is huge and the
  Filter right above it discards almost everything.

**Why it happens (plain).** Wrapping the column in a function or cast
(`date(ts) = '2026-07-01'`, `CAST(part_col AS STRING) = ...`), filtering
through a UDF (user-defined function — opaque to Spark), type
mismatches between literal and column, or filtering only after joins/
transformations — all of these stop Spark from pushing the filter down
to the files.

**Fix options (all SQL — no configs needed).**
1. Filter on the raw partition column with a literal of the column's
   own type: `WHERE part_date = DATE'2026-07-01'` — functions go on the
   literal side, never on the column side.
2. Replace UDF filters on scan columns with built-in expressions where
   possible.
3. Select only the needed columns (shrinks `ReadSchema`; columnar
   formats like Parquet then skip whole columns).
4. Move selective filters before joins/aggregations when semantics
   allow — flag any semantic difference to the user.
5. Re-check the plan afterwards: `PartitionFilters` / `PushedFilters`
   must now list the predicates, and the scan stage input size must
   drop.

**Version notes.** Plan field names verified on 3.5 docs; behavior
applies across 3.x.
