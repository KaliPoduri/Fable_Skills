# SOURCES.md — source manifest

Every normative claim in this skill traces to a source below. Never rely
on model memory alone (risk R6). All Spark defaults and since-versions
were read from these official pages, not recalled.

| Standard / source | Exact version | Official URL | Last verified | Offline fallback |
|---|---|---|---|---|
| Apache Spark docs — Performance Tuning (AQE family, join hints, broadcast/shuffle/file-read SQL options) | Spark 3.5.8 | https://spark.apache.org/docs/3.5.8/sql-performance-tuning.html | 2026-07-10 | Distilled in references/config-table.md and references/diagnosis-playbooks.md |
| Apache Spark docs — Configuration (executor sizing, dynamic allocation, memory, serializer, speculation, event log, task cpus, deploy-vs-runtime property note) | Spark 3.5.8 | https://spark.apache.org/docs/3.5.8/configuration.html | 2026-07-10 | Distilled in references/config-table.md |
| Apache Spark docs — Monitoring and Instrumentation (History Server, port 18080, event-log settings, cleaner/retention defaults) | Spark 3.5.8 | https://spark.apache.org/docs/3.5.8/monitoring.html | 2026-07-10 | Distilled in references/evidence-gathering.md |
| Apache Spark docs — Web UI (tabs, task summary metrics, spill metric definitions, SQL-tab plan Details, executor metrics) | Spark 3.5.8 | https://spark.apache.org/docs/3.5.8/web-ui.html | 2026-07-10 | Distilled in references/evidence-gathering.md and references/diagnosis-playbooks.md |
| Apache Spark docs — Running on YARN (spark.executor.instances, yarn logs -applicationId, log aggregation) | Spark 3.5.8 | https://spark.apache.org/docs/3.5.8/running-on-yarn.html | 2026-07-10 | Distilled in references/evidence-gathering.md and references/config-table.md |
| Apache Spark docs — EXPLAIN statement (modes, plan output shape) | Spark 3.5.8 | https://spark.apache.org/docs/3.5.8/sql-ref-syntax-qry-explain.html | 2026-07-10 | Distilled in references/physical-plan-reading.md |
| Apache Spark docs — Hints (join hint semantics; FileScan example with PartitionFilters/PushedFilters) | Spark 3.5.8 | https://spark.apache.org/docs/3.5.8/sql-ref-syntax-qry-select-hints.html | 2026-07-10 | Distilled in references/physical-plan-reading.md |
| Apache Spark docs — Tuning Guide (Kryo serialization, memory management overview, 2–3 tasks per core, GC note) | Spark 3.5.8 | https://spark.apache.org/docs/3.5.8/tuning.html | 2026-07-10 | Distilled in references/config-table.md and references/diagnosis-playbooks.md |
| PySpark API — DataFrame.explain (modes; mode parameter since 3.0) | PySpark 3.5.8 | https://spark.apache.org/docs/3.5.8/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.explain.html | 2026-07-10 | Distilled in references/physical-plan-reading.md |
| PySpark user guide — "Bug Busting: Debugging PySpark" (AdaptiveSparkPlan isFinalPlan plan examples; SortMergeJoin/BroadcastHashJoin node names) | PySpark 4.1.2 (latest; the AQE plan display applies to 3.x with AQE on) | https://spark.apache.org/docs/latest/api/python/user_guide/bugbusting.html | 2026-07-10 | Distilled in references/physical-plan-reading.md |
| Apache Spark archived docs — 3.1.3 Performance Tuning and Configuration (AQE disabled by default pre-3.2; minPartitionNum; pre-3.3 memoryOverhead default text) | Spark 3.1.3 | https://archive.apache.org/dist/spark/docs/3.1.3/sql-performance-tuning.html and https://archive.apache.org/dist/spark/docs/3.1.3/configuration.html | 2026-07-10 | Version notes in references/config-table.md and references/diagnosis-playbooks.md |
| Apache Spark archived docs — 3.3.4 Configuration (shuffleTracking default false through 3.3.x) | Spark 3.3.4 | https://archive.apache.org/dist/spark/docs/3.3.4/configuration.html | 2026-07-10 | Version note in references/config-table.md |
| Apache Spark archived docs — 3.4.4 Configuration (shuffleTracking default true from 3.4) | Spark 3.4.4 | https://archive.apache.org/dist/spark/docs/3.4.4/configuration.html | 2026-07-10 | Version note in references/config-table.md |

Verification notes (2026-07-10):

- All URLs above fetched successfully on 2026-07-10. Older per-patch doc
  paths on spark.apache.org (e.g., /docs/3.5.5/, /docs/3.1.3/) return
  404 — only the newest patch of a minor stays on the live site; use
  archive.apache.org/dist/spark/docs/<version>/ for the rest.
- AQE default flip: the 3.5.8 Performance Tuning page states AQE is
  "enabled by default since Apache Spark 3.2.0"; the archived 3.1.3
  page states "AQE is disabled by default". Both fetched.
- `spark.dynamicAllocation.shuffleTracking.enabled` default flip:
  3.3.4 configuration docs show default false; 3.4.4 and 3.5.8 show
  default true (all list "Since Version 3.0.0").
- Defaults and since-versions in references/config-table.md were taken
  from the per-property tables of the 3.5.8 pages above. A summarized
  fetch of the full 3.5.8 configuration page was truncated and its SQL
  section discarded as unreliable; SQL-option values come from the
  Performance Tuning page's tables instead.
- Plan node names: SortMergeJoin, BroadcastHashJoin, Exchange,
  BroadcastExchange, Sort, HashAggregate, Filter, Project, Scan,
  FileScan (with PartitionFilters/PushedFilters/DataFilters/ReadSchema),
  AdaptiveSparkPlan isFinalPlan — all quoted from example plans on the
  official pages above. ShuffledHashJoin and its metrics ("data size of
  build side", "time to build hash map") from the Web UI page's SQL
  metrics table. BroadcastNestedLoopJoin is confirmed on
  spark.apache.org (Spark 3.4.0 release notes reference
  BroadcastNestedLoopJoinExec; the strategy "broadcast nested loop
  join" is named on the 3.5.8 Performance Tuning page).
- History-server access and event-log retention are org-specific
  ([OPEN] U5 in PLAN.md): the skill teaches the standard paths and
  always defers actual access/retention to the cluster admin.
