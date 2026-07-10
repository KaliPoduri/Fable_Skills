# Gathering evidence — Spark UI, History Server, YARN logs

Sources: Apache Spark 3.5.8 docs — Web UI
(https://spark.apache.org/docs/3.5.8/web-ui.html), Monitoring
(https://spark.apache.org/docs/3.5.8/monitoring.html), Running on YARN
(https://spark.apache.org/docs/3.5.8/running-on-yarn.html). Verified
2026-07-10.

Reminder before anything is pasted back: run the safe-to-share checklist
(secrets/passwords; tokens/credentials/API keys; customer identifiers;
raw data row values) on every artifact FIRST, and have the user confirm
or redact before analysis.

Access caveat to repeat with every instruction below: whether the user
can reach the Spark UI, the History Server, or YARN logs — and how long
event logs are retained — depends on org setup. Tell the user to
**confirm access and retention with their cluster admin** if a step
fails.

## The Spark UI (live, while the job runs)

Every running Spark application serves its own web UI, by default at
port 4040 on the driver host (`http://<driver-node>:4040`; a second app
on the same host takes 4041, then 4042, ...). It disappears when the
application ends — for finished jobs use the History Server below.

### Jobs tab

Shows every job (one per action the code triggers) with status,
duration, and progress, plus an event timeline. Click a job for its DAG
visualization and stages.

**Bring back:** the duration of the slowest job(s), and which stage(s)
inside them dominate.

### Stages tab — the most important tab for slowness

All stages with status and summary counts. Click the slow stage; the
detail page has:

- **Summary metrics for all tasks** — a table plus timeline of task
  metrics: duration, GC time, scheduler delay, task deserialization
  time, shuffle read size / records, shuffle read fetch wait time,
  shuffle write time, peak execution memory, and — when present —
  **Shuffle spill (memory)** (size of the data in memory) and
  **Shuffle spill (disk)** (size written to disk).
- **Aggregated metrics by executor** — the same numbers per executor;
  one overloaded executor stands out here.
- **Tasks list** — every task individually; sort by Duration and
  compare the slowest tasks against the typical one (skew shows up
  here), and check their shuffle read sizes.

**Bring back:** stage duration; task count; typical vs slowest task
duration; shuffle read size of the slowest tasks vs the rest; any
non-zero spill numbers.

### SQL / DataFrame tab

One row per query with duration and its jobs. Click the query: the
execution DAG with per-operator metrics (e.g., "number of output rows",
shuffle bytes written, spill size), and a **Details** link at the bottom
that prints the logical plans and the physical plan — this is where to
copy the plan of a job that already ran.

**Bring back:** the physical plan text from Details, plus "number of
output rows" for the scan, join, and aggregate nodes on the slow path.

### Executors tab

Summary per executor: memory and disk used, cores, task time, GC time,
shuffle read/write, storage memory (memory used and reserved for
caching data).

**Bring back:** executor count and sizes actually granted; GC time
relative to task time; whether some executors sit idle.

### Storage tab

Cached (persisted) DataFrames/RDDs: storage level, size in memory/disk,
partitions cached. Only populated when the job caches something.

**Bring back:** what is cached and how big — cache state must be noted
in the experiment protocol.

## Spark History Server (for FINISHED jobs)

The History Server rebuilds the same UI from persisted event logs after
the application has completed — everything above works there too.

- It runs where the org started it (`sbin/start-history-server.sh`) and
  serves `http://<server-url>:18080` by default, listing completed and
  incomplete applications. **Ask the admin for the org's History Server
  URL** — the host and port may differ.
- Jobs appear ONLY if event logging was on when the job ran:
  `spark.eventLog.enabled=true` (default false) and
  `spark.eventLog.dir` pointing at the shared log directory. If a
  finished job is missing, it likely ran without event logging — it
  must be rerun with these settings to become inspectable.
- Retention is org-specific: the server can clean old logs
  (`spark.history.fs.cleaner.enabled`, default false; when the org
  enables it, the documented defaults are check interval 1d and max age
  7d). **Old runs may already be deleted — confirm retention with the
  admin.**
- Find the job by its application ID or name in the server's list; the
  ID is printed in the submission output/logs — ask the team where
  submissions are logged if the user does not have it.

**Bring back:** same artifacts as the live UI (stage metrics, SQL tab
physical plan).

## YARN logs (driver and executor output)

For jobs on YARN, container logs (driver + every executor) are
retrievable after the run **if log aggregation is enabled on the
cluster** (`yarn.log-aggregation-enable` — a cluster admin setting):

```
yarn logs -applicationId <app ID>
```

prints the contents of all log files from all containers of that
application. Without aggregation, logs stay on the individual worker
machines under the YARN log directory and need admin help to reach.

These logs are large. Have the user search rather than paste
everything: GC-related lines, "spill" mentions, Kryo/serialization
errors, broadcast timeout warnings, and the timestamps of long gaps.
Remind them of the safe-to-share checklist before pasting excerpts.

**Bring back:** the specific warning/error lines with a few lines of
context, not the whole log.

## Minimum evidence checklist for a useful diagnosis

1. Exact Spark 3.x minor version (intake gate — always first).
2. The physical plan (from code `explain`, SQL `EXPLAIN`, or UI SQL tab
   Details).
3. The slow stage's numbers: task count, typical vs slowest task
   duration, shuffle read/write, spill columns.
4. Data shape: rough input size, and for joins the rough size of each
   side.
5. What changed (data growth? code change? cluster change?) and the
   before/after durations.

With fewer than these, prefer "I cannot tell from what I have — please
bring item N" over guessing.
