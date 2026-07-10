# Output eval cases (≥3)

Each case is run twice — WITH the skill installed and WITHOUT (raw
assistant) — and scored against the rubric in
docs/AUTHORING-GUIDE.md §Eval thresholds. The skill must beat raw output.

## Case 1

- Prompt: "Our orders-enrichment job went from 30 minutes to 4 hours.
  It doesn't fail. I'm on Spark 3.3. Here's the plan and what I see in
  the UI." Plan shows `AdaptiveSparkPlan isFinalPlan=false` over a
  `SortMergeJoin` fed by two `Exchange hashpartitioning(customer_id,
  200)` nodes; Stages tab shows 198 of 200 tasks finishing in under a
  minute and 2 tasks running ~2 hours with Shuffle Read Size ~12 GB
  each vs ~60 MB median.
- Input artifacts (if any): pasted physical plan text plus copied task
  summary numbers from the Stages tab.
- Rubric focus: source accuracy (skew diagnosed from THEIR task-spread
  and shuffle-read numbers, not generic advice), template compliance
  (Diagnosis → Why tied to their evidence → Fix → experiment protocol
  → Confidence → runtime-state caveat), safe-to-share checklist as the
  FIRST response to the pasted artifacts.
- Expected qualities: identifies hash-partitioned join skew; asks or
  confirms the heavy keys (NULL/default IDs) before salting advice;
  offers AQE skew-join settings valid for 3.3 (AQE default-on since
  3.2; skewedPartitionFactor 5.0 / threshold 256MB with why their
  partitions may sit under the trigger); SQL-first alternatives
  (filter junk keys, broadcast small side, salting with
  result-equivalence note); configs marked job-scoped with job-owner
  approval; minimum-improvement threshold recorded BEFORE runs; ≥3
  runs, median + p95, rollback, cost note.

## Case 2

- Prompt: "Every stage of our hourly job launches ~40,000 tasks that
  each finish in under a second. The whole job takes 50 minutes on
  Spark 3.1. The input folder has about 500,000 small JSON files."
- Input artifacts (if any): Stages-tab description (task counts,
  per-task duration, tiny per-task input), no plan initially.
- Rubric focus: completeness (BOTH the small-files read problem and
  the shuffle-partition/AQE-coalescing angle addressed), honesty
  (states what it cannot tell without the plan and asks for it),
  version correctness (3.1: AQE is NOT on by default and
  minPartitionSize/parallelismFirst do not exist — advice must not
  cite 3.2+ knobs as present).
- Expected qualities: producer-side compaction named as the durable
  fix (advise-only, owner approval); reader-side
  spark.sql.files.maxPartitionBytes / openCostInBytes with plain
  meanings; for shuffle stages on 3.1: enable spark.sql.adaptive.enabled
  and coalescing, or lower spark.sql.shuffle.partitions with sizing
  arithmetic; teaches how to pull the physical plan and which Stages
  numbers to bring back; experiment protocol with pre-agreed threshold
  and rollback.

## Case 3

- Prompt: "On Spark 3.4 our join broadcasts a table and sits there for
  minutes; sometimes we see warnings about the 300 second broadcast
  timeout. The 'small' table is 800 MB. Should I just set
  spark.sql.broadcastTimeout to 3600?"
- Input artifacts (if any): plan fragment with `BroadcastExchange
  HashedRelationBroadcastMode` feeding a `BroadcastHashJoin`; the user's
  proposed config change.
- Rubric focus: correctness trap (the right answer is usually NOT to
  raise the timeout — 800 MB is far over the 10 MB default
  autoBroadcastJoinThreshold, so something forced this broadcast),
  actionability (find the hint or threshold override that caused it),
  honesty/triage (if runs actually FAIL on the timeout, route the
  failure analysis to etl-assistant by name).
- Expected qualities: explains broadcast joins in plain words; asks
  what set the broadcast (hint vs raised threshold); recommends
  removing the hint / restoring the threshold so the join becomes a
  sort-merge join, with AQE (default-on in 3.4) re-checking at runtime;
  presents raising broadcastTimeout only as the narrow case where the
  side is legitimately small; job-scoped configs with owner approval;
  experiment protocol comparing median + p95 of ≥3 runs against a
  pre-recorded improvement threshold; rollback and cost-vs-runtime
  noted.
