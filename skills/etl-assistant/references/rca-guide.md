# Spark/ETL failure-class catalog — RCA guide for newbies

Every Spark-specific claim below (exception names, config names,
defaults, semantics) was verified against the official Apache Spark
3.5.8 documentation and the official Hadoop/Java/POSIX sources listed in
references/SOURCES.md (verified 2026-07-10). The org runs Spark 3.x; the
exact minor version is an M0 fact-lock item — confirm it before relying
on a default value, because defaults can differ between minor versions.

Two words used everywhere below:

- **Driver** — the process where the SparkContext is initialized (the
  "coordinator" of the job; per the `spark.driver.memory` docs).
- **Executor** — a worker process that runs the job's tasks on cluster
  machines.

## First: find the logs

- The driver and each executor write separate logs. The error the user
  pastes is often only the LAST symptom; the first failure usually sits
  in another container's log, earlier in time.
- On YARN (the cluster manager), fetch everything at once:
  `yarn logs -applicationId <app ID>` — this "will print out the
  contents of all log files from all containers from the given
  application" (Spark 3.5.8, Running on YARN).
- With log aggregation enabled, container logs are copied to HDFS and
  can be viewed from anywhere with that command. Without it, logs stay
  on each machine under `YARN_APP_LOGS_DIR` (usually `/tmp/logs` or
  `$HADOOP_HOME/logs/userlogs`) and you must look on the host itself.
- Read from the FIRST failure, not the last: retries and cascades bury
  the root cause under repeated later errors.

## Quick routing table — symptom to class

| Symptom in the log | Start with class |
|---|---|
| `java.lang.OutOfMemoryError: Java heap space` / `GC overhead limit exceeded` | 1 (executor) or 3 (driver) — check which process logged it |
| Executor/container died with exit code 137 | 2 |
| Results too large for the driver / failure on `collect()` | 3 |
| `FetchFailedException` / failed to fetch shuffle data | 4 |
| Same task failing 4 times, then the job aborts | 5 |
| `java.io.NotSerializableException` / serialization failure | 6 |
| Column cannot be resolved / cast failure / `Path does not exist` / corrupt or garbled records | 7 |
| `AnalysisException` / table or view not found | 8 |
| `AccessControlException` / permission denied | 9 |
| Job accepted but never starts running | 10 |
| `No space left on device` | 11 |

## Class 1 — Executor out of memory (JVM heap)

- **Symptom pattern:** an executor log ends with
  `java.lang.OutOfMemoryError: Java heap space` or
  `java.lang.OutOfMemoryError: GC overhead limit exceeded`.
- **What it means in plain words:** the worker process ran out of the
  memory pool the JVM (Java virtual machine) uses for objects. "Java
  heap space" means "an object could not be allocated in the Java heap";
  "GC overhead limit exceeded" means the garbage collector (the JVM's
  memory cleaner) "is running most of the time, and the Java application
  is making very slow progress" (Oracle Java 17 troubleshooting guide).
- **Where to look:** the failing executor's log (via `yarn logs`); the
  job chunk `jobs/<job>.md` for what the stage does; the live code at
  the pointers for wide operations (`groupByKey`, big joins,
  aggregations, caching).
- **Typical causes:**
  - code — one task's working set is too large. The Spark tuning guide
    states this directly: "Sometimes, you will get an OutOfMemoryError
    not because your RDDs don't fit in memory, but because the working
    set of one of your tasks, such as one of the reduce tasks in
    `groupByKey`, was too large"; the documented first fix is to
    increase parallelism (more, smaller partitions). Also: caching too
    much data.
  - data — the input grew, or one key became huge (skew — most rows
    sharing one key, so one task carries them all).
  - infra — the deployed memory setting shrank. `spark.executor.memory`
    (default 1g) sets executor memory. Deployed values are runtime
    state: KB covers code only — verify the live value before acting.
- **Safe verification:** in non-prod, rerun with more partitions or a
  reduced input slice and watch whether the same stage survives; compare
  today's input volume to a normal day before touching any config.

## Class 2 — Container killed by YARN (exit code 137)

- **Symptom pattern:** an executor disappears; YARN reports the
  container exited with code 137, often followed by class-4 or class-5
  symptoms in other executors.
- **What it means in plain words:** exit code 137 = 128 + 9, the shell
  convention for "terminated by signal 9 (SIGKILL)" — a kill the process
  cannot refuse (GNU Bash manual; POSIX `kill`). YARN enforces a memory
  limit per container ("Whether physical memory limits will be enforced
  for containers" — `yarn.nodemanager.pmem-check-enabled`, default
  true), and its strict memory control "kills each container that has
  exceeded its limits", producing exit code 137 (Hadoop NodeManager
  memory-control docs). Unlike class 1, the JVM heap may have been fine:
  the whole process group's memory — heap plus everything outside it —
  exceeded the container's allocation.
- **Where to look:** the NodeManager diagnostics for the killed
  container in `yarn logs` output; the job's memory settings in the live
  repo (the job chunk lists key params and where they are set).
- **Typical causes:**
  - infra — container sized too tightly. Memory outside the JVM heap is
    budgeted by `spark.executor.memoryOverhead` (default: executor
    memory × `spark.executor.memoryOverheadFactor`, minimum 384 MiB);
    too small an overhead gets the container killed even though the heap
    never overflowed.
  - code — heavy use of memory outside the JVM heap (native libraries,
    Python worker processes in PySpark), which counts against the
    container limit but not the heap.
  - data — input growth or skew pushing one container over the line.
- **Safe verification:** confirm 137 in the container diagnostics, then
  compare the container's allocation (runtime state — "KB covers code
  only — verify the live value before acting") with what the job
  actually used per the diagnostics; test a larger overhead in non-prod
  only, with the job owner's approval.

## Class 3 — Driver out of memory / result too large

- **Symptom pattern:** the DRIVER log (not an executor's) shows an
  `OutOfMemoryError`, or the job aborts complaining about the size of
  results sent to the driver.
- **What it means in plain words:** actions like `collect()` pull data
  from all executors back into the single driver process. Spark caps the
  "total size of serialized results of all partitions for each Spark
  action (e.g. collect)" with `spark.driver.maxResultSize` (default 1g);
  results under the cap can still overflow the driver's own memory
  (`spark.driver.memory`, default 1g).
- **Where to look:** the driver log; the live code at the job chunk's
  pointers for `collect()`, `toPandas()`-style conversions, or building
  large in-driver structures.
- **Typical causes:**
  - code — collecting a full dataset to the driver when an aggregation
    or a write-to-table would do. This is the common one.
  - data — a result set that used to be small grew past the limits.
  - infra — driver memory reduced in deployment (runtime state — verify
    the live value).
- **Safe verification:** count the rows/bytes the collecting step would
  return (a cheap `count()` in non-prod) before assuming limits must be
  raised; prefer removing the collect over raising limits.

## Class 4 — Shuffle fetch failure (FetchFailedException)

- **Symptom pattern:** `FetchFailedException` in task logs — the
  exception name Spark's own configuration docs use for a failed shuffle
  fetch (see `spark.shuffle.detectCorrupt.useExtraMemory`).
- **What it means in plain words:** a shuffle is the phase where
  executors exchange data between stages (for joins, groupings). This
  error means a "Task failed to fetch shuffle data from a remote node"
  and "probably means we have lost the remote executors the task is
  trying to fetch from, and thus need to rerun the previous stage"
  (Spark `FetchFailed` API docs). The failing task is usually the
  VICTIM: the real problem is on the machine that should have served
  the data.
- **Spark's own handling (so retries in the log are expected):** fetch
  failures do not count toward the normal per-task failure limit;
  Spark goes back to the stage that generated the map output and
  regenerates the missing data (`FetchFailed` API docs). IO-related
  fetch failures are retried `spark.shuffle.io.maxRetries` times
  (default 3) with `spark.shuffle.io.retryWait` (default 5s) between
  attempts — documented as stabilizing "large shuffles in the face of
  long GC pauses or transient network connectivity issues".
- **Where to look:** find the FIRST dying executor across all container
  logs (`yarn logs`), earlier in time than the fetch failures. Check
  whether one host appears in every failure.
- **Typical causes:**
  - infra — the serving executor was killed (often class 2/exit 137) or
    its node was lost; network trouble; long GC pauses (which also point
    back to class 1 pressure).
  - data — skew: one giant shuffle block overloads whoever serves or
    receives it.
  - code — rarely the fetch itself; but a shuffle-heavy plan (an
    unnecessary wide join or grouping) makes the job fragile. Check the
    job chunk's known failure points.
- **Safe verification:** trace the first failure, not the fetch error;
  if an executor died first, diagnose THAT death (class 1/2) — fixing
  the fetch symptom alone fixes nothing.

## Class 5 — Task/stage failure and retry semantics

- **Symptom pattern:** the same task fails repeatedly, then the job
  aborts; the final error names the LAST attempt.
- **What it means in plain words:** Spark retries failed tasks. A job
  gives up when one particular task fails `spark.task.maxFailures` times
  continuously (default 4). A stage (a group of tasks between shuffles)
  is aborted after `spark.stage.maxConsecutiveAttempts` consecutive
  failed attempts (default 4). Fetch failures take the special path in
  class 4 instead of counting toward the task limit.
- **Where to look:** scroll UP from the abort message to attempt 0 of
  the first failing task — that stack trace is the root cause; the
  final message is just the retry budget running out.
- **Typical causes:** whatever the underlying per-attempt error is —
  route it through this catalog (OOM → 1/2, serialization → 6, data →
  7...). A cause that fails on every host is usually code or data; a
  cause tied to one host is usually infra.
- **Safe verification:** confirm every attempt of the task failed with
  the SAME error; if attempts differ, diagnose the earliest one first.

## Class 6 — Serialization errors

- **Symptom pattern:** `java.io.NotSerializableException`, or a
  serialization error naming a class, raised when the job starts doing
  distributed work.
- **What it means in plain words:** Spark must package code and data to
  send from the driver to executors (serialization). By default it uses
  Java's `ObjectOutputStream` and "can work with any class you create
  that implements `java.io.Serializable`" (Spark tuning guide). An
  object that does not implement that interface cannot be shipped —
  `NotSerializableException` is "thrown when an instance is required to
  have a Serializable interface" and its message carries the class name
  (Java SE 17 API docs).
- **Where to look:** the class named in the exception message; the live
  code where a function passed to Spark (a closure) captures that
  object — database connections, clients, loggers, or `self`/outer-class
  references are the usual suspects.
- **Typical causes:**
  - code — almost always: a closure captures a non-serializable object;
    create such objects inside the task instead, or mark fields
    transient. If the org job uses Kryo (a faster serializer selected
    with `spark.serializer` = `org.apache.spark.serializer.KryoSerializer`),
    note that Kryo "does not support all Serializable types and requires
    you to register the classes you'll use" (tuning guide) — an
    unregistered/unsupported class fails at serialization time.
  - data/infra — effectively never.
- **Safe verification:** reproduce in non-prod with a tiny input — this
  class fails identically at any data size, which itself is evidence.

## Class 7 — Data-shaped failures

Schema drift, bad values, missing input, corrupt files, encoding. The
code is often innocent; the evidence must show it.

### 7a. Schema drift (columns changed upstream)

- **Symptom:** error conditions like `UNRESOLVED_COLUMN` ("A column or
  function parameter with name <objectName> cannot be resolved"),
  `COLUMN_NOT_FOUND`, or `CAST_INVALID_INPUT` ("The value <expression>
  of the type <sourceType> cannot be cast to <targetType> because it is
  malformed") — Spark 3.5.8 error-conditions list.
- **Plain words:** the job's SQL/script expects a column or type that
  the incoming data no longer has (or newly has).
- **Where to look:** the job chunk's read-tables list with pointers;
  live code for the referenced column; upstream job's chunk for recent
  output changes. Schemas are runtime state: KB covers code only —
  verify the live value before acting.
- **Causes:** data (upstream changed shape) or code (job's own query
  wrong after an edit — check recent commits to the cited file).
- **Safe verification:** print the actual schema of the input in
  non-prod (read a small sample and show its schema) and diff against
  what the code expects.

### 7b. Unexpected nulls and bad values

- **Symptom:** `DIVIDE_BY_ZERO` ("Division by zero. Use `try_divide` to
  tolerate divisor being 0 and return NULL instead...") and similar
  value errors; or the job "succeeds" upstream and fails only in a later
  consumer.
- **Plain words:** a value the logic never expected arrived — a zero, a
  null (missing value), an out-of-range number.
- **Causes:** data (quality regression upstream) more often than code
  (missing guard). Both fixes are valid; say which one is being
  proposed and why.
- **Safe verification:** count offending rows in non-prod (`WHERE
  divisor = 0`, `WHERE col IS NULL`) and check whether they exist on a
  normal day too.

### 7c. Missing partition or path

- **Symptom:** `PATH_NOT_FOUND` — "Path does not exist: <path>" (Spark
  3.5.8 error conditions).
- **Plain words:** the input folder/partition (often a dated
  subdirectory like `dt=2026-07-10`) is not there — usually the
  upstream job that produces it has not run, is late, or wrote somewhere
  else.
- **Where to look:** the upstream/downstream section of the job chunk;
  the schedule (runtime state — verify the live value). List the parent
  path with `hadoop fs -ls <path>` (Hadoop FileSystem Shell) to see what
  actually exists.
- **Causes:** data/infra (upstream delay, schedule drift, cleanup jobs)
  far more often than code (a wrongly built path — check the path
  construction at its pointer).
- **A trap to flag:** the `ignoreMissingFiles` option only covers files
  "deleted ... after you construct the DataFrame" (Spark generic file
  source options) — it is NOT a fix for input that was never produced.

### 7d. Corrupt files

- **Symptom:** read failures on specific files; behavior depends on the
  read mode. For CSV (and similar text formats), documented modes are:
  `PERMISSIVE` (default — malformed record goes into the field named by
  `columnNameOfCorruptRecord`, malformed fields become null),
  `DROPMALFORMED` (drops whole corrupted records), `FAILFAST` (throws on
  the first corrupted record) — Spark 3.5.8 CSV data source docs.
- **Plain words:** one or more input files are damaged or half-written;
  with `FAILFAST` the whole job dies on the first bad record.
- **Causes:** data/infra (interrupted upstream write, transfer
  truncation) — rarely code.
- **Caution:** `spark.sql.files.ignoreCorruptFiles` (or the
  `ignoreCorruptFiles` option) makes jobs "continue to run when
  encountering corrupted files" with partial contents returned — that
  silently drops data. Recommend it only with the job owner's explicit
  sign-off, never as a default fix.
- **Safe verification:** identify the exact file from the error, check
  its size against siblings (`hadoop fs -ls`, `hadoop fs -du`), and try
  reading only that file in non-prod.

### 7e. Encoding

- **Symptom:** garbled text values, or malformed-record failures on a
  file that "looks fine".
- **Plain words:** the file was written in a different character
  encoding than the reader assumes; the CSV reader's `encoding` option
  defaults to UTF-8 (Spark 3.5.8 CSV data source docs).
- **Causes:** data (a producer changed encoding) or code (reader option
  wrong for a known-legacy source).
- **Safe verification:** read a small sample of the raw bytes and
  compare against the declared encoding before changing any option.

## Class 8 — SQL analysis errors

- **Symptom pattern:** `org.apache.spark.sql.AnalysisException`, e.g.
  with `TABLE_OR_VIEW_NOT_FOUND` ("The table or view <relationName>
  cannot be found. Verify the spelling and correctness of the schema and
  catalog...") or `SCHEMA_NOT_FOUND` (Spark 3.5.8 error conditions).
- **What it means in plain words:** the exception is "thrown when a
  query fails to analyze, usually because the query itself is invalid"
  (Spark API docs) — Spark rejected the query while checking it, before
  doing the work. Typically the job dies quickly at start.
- **Where to look:** the exact name in the error vs the live SQL at the
  job chunk's pointer; the KB glossary for the org's table-naming
  conventions.
- **Typical causes:**
  - code — a typo, or the wrong database/catalog prefix in the script.
  - infra/runtime — the table genuinely does not exist HERE: it exists
    in prod but not in the environment the job ran in, or a create step
    upstream did not run. Which tables exist is runtime state: KB
    covers code only — verify the live value before acting.
- **Safe verification:** list the target database's tables in the SAME
  environment the job ran in and compare spelling character by
  character.

## Class 9 — Permission and access failures

- **Symptom pattern:** `AccessControlException` when reading or writing
  a path.
- **What it means in plain words:** HDFS (the cluster file system)
  checks POSIX-like permissions — owner, then group, then other — and
  "all methods that use a path parameter will throw
  `AccessControlException` if permission checking fails" (HDFS
  Permissions Guide). The job's service account is not allowed to do
  what it tried on that path.
- **Where to look:** the exact path and operation in the error;
  `hadoop fs -ls <path>` shows the path's permissions, owner (userid)
  and group (Hadoop FileSystem Shell docs). Compare with the account the
  job runs as (runtime state — verify the live value).
- **Typical causes:** infra almost always — path ownership or
  permissions changed, the job's account changed, a new output location
  was created with the wrong owner. Code only when the script writes to
  a newly wrong path (check the path construction at its pointer).
- **Safe verification:** `hadoop fs -ls` the path and its parent;
  confirm with the platform team which account the job runs as before
  proposing any permission change (permission changes are for the
  platform/owner, not this skill).

## Class 10 — Resource/queue starvation on YARN

- **Symptom pattern:** the job is submitted but never starts working; no
  task errors at all.
- **What it means in plain words:** YARN runs applications out of
  queues with capacity limits. An application in state ACCEPTED has
  been "accepted by the scheduler" but is not yet RUNNING ("application
  which is currently running") — YARN API docs. If the queue is full,
  the app waits in ACCEPTED. Spark submits to the queue named by
  `spark.yarn.queue` (default: "default").
- **Where to look:** application state via
  `yarn application -status <ApplicationId>` (prints "the status of the
  application" — YARN commands docs) or the ResourceManager web UI;
  what else occupies the queue via `yarn application -list`.
- **Typical causes:** infra — queue over capacity, another heavy app
  hogging it, cluster-wide resource pressure, or the job asked for
  containers larger than the queue can grant. The queue assignment and
  cluster load are runtime state: KB covers code only — verify the live
  value before acting. Code: essentially never.
- **Safe verification:** check whether the app reached RUNNING at all;
  if it sat in ACCEPTED, no code change can be the fix — hand the
  evidence to whoever operates the cluster.

## Class 11 — Disk-space failures

- **Symptom pattern:** tasks fail with IO errors carrying the OS
  message "No space left on device" (POSIX errno `ENOSPC`).
- **What it means in plain words:** a disk filled up. Spark uses
  "scratch" space for shuffle map output files and data spilled to disk,
  located by `spark.local.dir` (default `/tmp`) — Spark configuration
  docs. Big shuffles can fill that disk even when the data warehouse has
  plenty of room.
- **Where to look:** WHICH host and path the error names; whether
  failures cluster on one machine (that host's scratch disk) or hit
  many (the job's shuffle is simply too big).
- **Typical causes:**
  - infra — scratch disk too small, or leftover files from crashed jobs
    on one node.
  - data — input growth/skew inflating shuffle size.
  - code — an avoidable wide operation multiplying shuffled data.
- **Safe verification:** check free space on the disk holding
  `spark.local.dir` on the affected host (e.g. with `df`); compare this
  run's input size to a normal run. Where `spark.local.dir` actually
  points in the deployed cluster is runtime state — verify the live
  value before acting.

## When the cause is NOT in the code

Say it plainly, show why the code is exonerated (e.g. "unchanged since
commit <hash>, and the same code succeeded yesterday — evidence at
repo:path:line"), and walk the user through the non-code checks in this
order, zero Spark knowledge assumed:

1. **Upstream delay / missing input** — does the input path or
   partition for the failed run exist? (`hadoop fs -ls <path>`; class
   7c.) Did the upstream job finish before this one started?
2. **Data quality** — did the input's shape or values change? (schema
   diff, null/zero counts on a sample; classes 7a/7b.)
3. **Infra / YARN** — did the app ever reach RUNNING
   (`yarn application -status`; class 10)? Did containers die with exit
   137 (class 2)? Did one host account for all failures (classes 4/11)?
4. **Permissions** — any `AccessControlException`? Check path owner and
   mode with `hadoop fs -ls` (class 9).
5. **Deployed config / schedule** — memory settings, queue, schedule,
   or connection endpoints changed in deployment? These are runtime
   state: KB covers code only — verify the live value before acting.

## Insufficient evidence — the minimum bar

Do not name a root cause without, at minimum: the job identified, the
first failure (not just the last), and one piece of corroborating
evidence (code pointer, data check, or container diagnostic) consistent
with the proposed class. Below that bar, use the Insufficient-evidence
output template and list exactly what is missing and the command that
obtains it.
