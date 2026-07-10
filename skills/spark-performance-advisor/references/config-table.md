# Spark config table — plain meanings, defaults, versions, scope

Sources: Apache Spark 3.5.8 docs — Configuration
(https://spark.apache.org/docs/3.5.8/configuration.html), Performance
Tuning (https://spark.apache.org/docs/3.5.8/sql-performance-tuning.html),
Tuning Guide (https://spark.apache.org/docs/3.5.8/tuning.html), Running
on YARN (https://spark.apache.org/docs/3.5.8/running-on-yarn.html);
archived 3.1.3 / 3.3.4 / 3.4.4 configuration docs for version deltas.
Verified 2026-07-10. Defaults below are the 3.5.x documented values;
differences per minor version are in the Version notes column. Confirm
the user's exact minor version before quoting any of this.

## How to apply changes (job-scoped by default)

- **Per job at submit:** `spark-submit --conf key=value ...` or a
  properties file passed with `--properties-file`. This is the default
  mechanism to recommend.
- **In code:** `spark.conf.set(...)` works for SQL runtime settings
  (the `spark.sql.*` ones), but deploy-related properties — executor
  sizing, dynamic allocation — "may not be affected when setting
  programmatically through SparkConf in runtime" (3.5.8 configuration
  docs): set those via spark-submit or the properties file.
- **Cluster-scoped** (defaults in the cluster's spark-defaults.conf,
  YARN services like the external shuffle service, YARN queue/container
  limits): flag as "requires cluster admin" — do not present as
  something the dev can just change.
- Every config change needs job-owner approval before any run, even in
  non-prod.

## Adaptive Query Execution (AQE) family

AQE re-optimizes the query plan at runtime using real statistics. The
sub-features below only act when the master switch is on.

| Parameter | Plain meaning | Default (3.5.x) | When to change | Version notes | Scope |
|---|---|---|---|---|---|
| `spark.sql.adaptive.enabled` | Master switch for runtime re-optimization | true | On 3.0–3.1 turn it on for slow shuffles, joins, or skew; on 3.2+ leave on | Default false on 3.0–3.1; **on by default since 3.2.0** | Job |
| `spark.sql.adaptive.coalescePartitions.enabled` | Merge small shuffle partitions to avoid many tiny tasks | true | Leave on; the cure for too-many-tiny-tasks after shuffles | Since 3.0.0 | Job |
| `spark.sql.adaptive.coalescePartitions.parallelismFirst` | When true, coalescing keeps max parallelism and only respects the 1MB floor — it IGNORES the 64MB advisory size | true | Set false to make coalescing actually target `advisoryPartitionSizeInBytes` | Since 3.2.0 (not on 3.0–3.1) | Job |
| `spark.sql.adaptive.coalescePartitions.minPartitionSize` | Floor for coalesced partition size | 1MB | Rarely | Since 3.2.0; on 3.0–3.1 the floor is `...minPartitionNum` (default: cluster default parallelism) | Job |
| `spark.sql.adaptive.coalescePartitions.initialPartitionNum` | Shuffle partition count BEFORE coalescing | (none) = `spark.sql.shuffle.partitions` | Set generously high and let AQE shrink per stage | Since 3.0.0 | Job |
| `spark.sql.adaptive.advisoryPartitionSizeInBytes` | Target shuffle-partition size during AQE optimization | 64MB | Smaller when tasks spill; larger when tasks are tiny | Since 3.0.0; see `parallelismFirst` | Job |
| `spark.sql.adaptive.skewJoin.enabled` | Auto-split oversized partitions in sort-merge joins | true | Leave on; check trigger thresholds below when skew persists | Since 3.0.0 | Job |
| `spark.sql.adaptive.skewJoin.skewedPartitionFactor` | Skew trigger: partition > factor × median size | 5.0 | Lower when skewed partitions sit under the trigger | Since 3.0.0 | Job |
| `spark.sql.adaptive.skewJoin.skewedPartitionThresholdInBytes` | Skew trigger: absolute size floor | 256MB | Lower on smaller datasets | Since 3.0.0 | Job |
| `spark.sql.adaptive.forceOptimizeSkewedJoin` | Handle skew even when it costs an extra shuffle | false | Stubborn skew the normal rule declines | Since 3.3.0 only | Job |
| `spark.sql.adaptive.localShuffleReader.enabled` | Read shuffle files locally when repartitioning became unnecessary (e.g., join converted to broadcast) | true | Leave on | Since 3.0.0 | Job |
| `spark.sql.adaptive.autoBroadcastJoinThreshold` | Broadcast threshold applied to RUNTIME sizes | (none) = same as `spark.sql.autoBroadcastJoinThreshold` | Set a separate runtime threshold for AQE join conversion | Since 3.2.0 only | Job |
| `spark.sql.adaptive.maxShuffledHashJoinLocalMapThreshold` | Gate for AQE converting sort-merge join to shuffled hash join | 0 (off) | Advanced; medium joins where sorting dominates | Since 3.2.0 only | Job |

## Shuffle and joins

| Parameter | Plain meaning | Default (3.5.x) | When to change | Version notes | Scope |
|---|---|---|---|---|---|
| `spark.sql.shuffle.partitions` | How many partitions every shuffle (join/aggregation) produces | 200 | The most-tuned knob: size to data volume (see Playbook 3); 200 is rarely right at scale | All 3.x | Job |
| `spark.sql.autoBroadcastJoinThreshold` | Max estimated table size Spark auto-broadcasts in a join | 10485760 (10MB) | Raise when a small dimension table sits just above it; -1 disables auto-broadcast | All 3.x | Job |
| `spark.sql.broadcastTimeout` | Seconds to wait for a broadcast in broadcast joins | 300 | Raise only when the broadcast side is legitimately small and the cluster was busy; otherwise fix the join strategy | All 3.x | Job |

## File reading

| Parameter | Plain meaning | Default (3.5.x) | When to change | Version notes | Scope |
|---|---|---|---|---|---|
| `spark.sql.files.maxPartitionBytes` | Max bytes packed into one read task | 134217728 (128MB) | Small-files problem; or read tasks too big/too small | Since 2.0 — all 3.x | Job |
| `spark.sql.files.openCostInBytes` | Accounting cost charged per file opened (in bytes) | 4194304 (4MB) | Raise to pack more small files into each task | Since 2.0 — all 3.x | Job |

## Executor sizing (set at submit time, not in code)

YARN container and queue limits cap all of these — the limits are set
by cluster admins; requests beyond them will not be granted.

| Parameter | Plain meaning | Default (3.5.x) | When to change | Version notes | Scope |
|---|---|---|---|---|---|
| `spark.executor.memory` | Heap memory per executor (worker process) | 1g | Spill or GC pressure after data-shrinking fixes | All 3.x | Job (submit-time); caps are admin |
| `spark.executor.cores` | Cores per executor = concurrent tasks per executor (`spark.task.cpus` default 1) | 1 in YARN mode; all worker cores in standalone | Fewer cores per executor = more memory per task | All 3.x | Job (submit-time) |
| `spark.executor.instances` | Number of executors (static allocation) | 2 | More parallelism — note the cost-vs-runtime trade in the output | Documented in Running on YARN | Job (submit-time); queue capacity is admin |
| `spark.executor.memoryOverhead` | Extra non-heap memory per executor, MiB | executorMemory × factor, min 384 | Raise for heavy off-heap use (e.g., Python workers) | Factor knob split out in 3.3.0; 3.0–3.2 docs state "executorMemory * 0.10, with minimum of 384" | Job (submit-time) |
| `spark.executor.memoryOverheadFactor` | The fraction in the row above | 0.10 | Rarely | Since 3.3.0 only | Job (submit-time) |

## Dynamic allocation

| Parameter | Plain meaning | Default (3.5.x) | When to change | Version notes | Scope |
|---|---|---|---|---|---|
| `spark.dynamicAllocation.enabled` | Grow/shrink executor count with workload | false | Bursty jobs on shared clusters | Requires ONE of: external shuffle service (`spark.shuffle.service.enabled`, default false — **cluster admin**), shuffle tracking (below), or shuffle-block decommissioning | Job flag; prerequisites may be cluster-scoped |
| `spark.dynamicAllocation.shuffleTracking.enabled` | Track shuffle files so dynamic allocation works WITHOUT the external shuffle service | true | On 3.0–3.3 set true when no external shuffle service exists | Since 3.0.0; default false through 3.3.x, **true since 3.4** (verified 3.3.4 vs 3.4.4 docs) | Job |
| `spark.dynamicAllocation.shuffleTracking.timeout` | How long to keep executors holding shuffle data | infinity | Lower if executors linger | Since 3.0.0 | Job |
| `spark.dynamicAllocation.minExecutors` | Lower bound | 0 | Guarantee a floor | All 3.x | Job |
| `spark.dynamicAllocation.maxExecutors` | Upper bound | infinity | ALWAYS set a cap — cost control | All 3.x | Job |
| `spark.dynamicAllocation.initialExecutors` | Starting count | = minExecutors | Warm start for known-big jobs | All 3.x | Job |
| `spark.dynamicAllocation.executorIdleTimeout` | Remove executors idle longer than this | 60s | Rarely | All 3.x | Job |

## Memory and serialization

| Parameter | Plain meaning | Default (3.5.x) | When to change | Version notes | Scope |
|---|---|---|---|---|---|
| `spark.memory.fraction` | Fraction of (heap − 300MB) shared by execution and storage | 0.6 | Last resort — the tuning guide says typical users should not need to adjust it | All 3.x | Job |
| `spark.memory.storageFraction` | Portion of the above where cached data is immune to eviction | 0.5 | Last resort, same warning | All 3.x | Job |
| `spark.serializer` | How objects are turned into bytes for network/caching | org.apache.spark.serializer.JavaSerializer | Set `org.apache.spark.serializer.KryoSerializer` for RDD-heavy jobs and serialized caching — often up to ~10x faster/compacter; register classes for best results. Since 2.0.0 Spark already uses Kryo internally when shuffling RDDs of simple types, arrays of simple types, or strings | All 3.x | Job |
| `spark.kryoserializer.buffer.max` | Max Kryo buffer size | 64m | Raise when serializing large objects with Kryo | All 3.x | Job |

## Other

| Parameter | Plain meaning | Default (3.5.x) | When to change | Version notes | Scope |
|---|---|---|---|---|---|
| `spark.speculation` | Re-launch suspiciously slow task copies on other nodes ("stragglers") | false | Slow tasks caused by flaky NODES. Useless against data skew — a re-run of a skewed task is just as slow (same data) | Trigger: task slower than 1.5× median (`spark.speculation.multiplier`) once 75% of tasks finished (`spark.speculation.quantile`) | Job |
| `spark.driver.maxResultSize` | Cap on total serialized results collected to the driver per action | 1g | Prefer NOT collecting big data to the driver; raise only when a large collect is genuinely required | All 3.x | Job |
| `spark.eventLog.enabled` / `spark.eventLog.dir` | Write event logs so the History Server can show finished jobs | false / file:///tmp/spark-events | Needed for post-run analysis; usually preset org-wide | All 3.x | Job-side setting, but the log directory and History Server are org/admin-managed |

## Example (job-scoped application)

```
spark-submit \
  --conf spark.sql.shuffle.partitions=600 \
  --conf spark.sql.autoBroadcastJoinThreshold=33554432 \
  --conf spark.executor.memory=4g \
  ... rest of the job's usual arguments ...
```

State in the output which values are proposals pending job-owner
approval, and include the rollback (the previous values, or "remove the
--conf overrides").
