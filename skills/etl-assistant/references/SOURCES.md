# SOURCES.md — source manifest

Every normative claim in this skill traces to a source below. Never rely
on model memory alone (risk R6). The org runs Spark 3.x; the exact minor
version is an M0 fact-lock item (PLAN.md U1) — Spark claims were
verified against 3.5.8, the newest 3.x documentation line at
verification. Re-verify defaults against the org's minor version once
U1 is locked.

| Standard / source | Exact version | Official URL | Last verified | Offline fallback |
|---|---|---|---|---|
| Apache Spark docs — Configuration | Spark 3.5.8 | https://spark.apache.org/docs/3.5.8/configuration.html | 2026-07-10 | Config names/defaults/semantics distilled in references/rca-guide.md |
| Apache Spark docs — Running on YARN | Spark 3.5.8 | https://spark.apache.org/docs/3.5.8/running-on-yarn.html | 2026-07-10 | `yarn logs` command, log aggregation, `spark.yarn.queue` distilled in references/rca-guide.md |
| Apache Spark docs — Tuning | Spark 3.5.8 | https://spark.apache.org/docs/3.5.8/tuning.html | 2026-07-10 | Serialization (Java default, Kryo) and task-working-set OOM guidance distilled in references/rca-guide.md |
| Apache Spark docs — Error Conditions | Spark 3.5.8 | https://spark.apache.org/docs/3.5.8/sql-error-conditions.html | 2026-07-10 | Error-condition names/messages distilled in references/rca-guide.md |
| Apache Spark docs — Generic File Source Options | Spark 3.5.8 | https://spark.apache.org/docs/3.5.8/sql-data-sources-generic-options.html | 2026-07-10 | ignoreCorruptFiles / ignoreMissingFiles semantics distilled in references/rca-guide.md |
| Apache Spark docs — CSV Files (data source options) | Spark 3.5.8 | https://spark.apache.org/docs/3.5.8/sql-data-sources-csv.html | 2026-07-10 | Read modes (PERMISSIVE/DROPMALFORMED/FAILFAST), columnNameOfCorruptRecord, encoding default distilled in references/rca-guide.md |
| Apache Spark API — org.apache.spark.FetchFailed (JavaDoc) | Spark 3.5.8 | https://spark.apache.org/docs/3.5.8/api/java/org/apache/spark/FetchFailed.html | 2026-07-10 | Fetch-failure meaning and special retry path distilled in references/rca-guide.md |
| Apache Spark API — org.apache.spark.sql.AnalysisException (JavaDoc) | Spark 3.5.8 | https://spark.apache.org/docs/3.5.8/api/java/org/apache/spark/sql/AnalysisException.html | 2026-07-10 | Analysis-failure meaning distilled in references/rca-guide.md |
| Apache Hadoop — yarn-default.xml | Hadoop docs "stable" line at verification | https://hadoop.apache.org/docs/stable/hadoop-yarn/hadoop-yarn-common/yarn-default.xml | 2026-07-10 | pmem/vmem enforcement defaults distilled in references/rca-guide.md |
| Apache Hadoop — NodeManager memory control (CGroups) | Hadoop docs "stable" line at verification | https://hadoop.apache.org/docs/stable/hadoop-yarn/hadoop-yarn-site/NodeManagerCGroupsMemory.html | 2026-07-10 | Container kill on limit + exit code 137 distilled in references/rca-guide.md |
| Apache Hadoop — HDFS Permissions Guide | Hadoop docs "stable" line at verification | https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsPermissionsGuide.html | 2026-07-10 | AccessControlException + POSIX-like permission model distilled in references/rca-guide.md |
| Apache Hadoop — FileSystem Shell | Hadoop docs "stable" line at verification | https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/FileSystemShell.html | 2026-07-10 | `hadoop fs -ls` / `-du` usage distilled in references/rca-guide.md |
| Apache Hadoop — YARN Commands | Hadoop docs "stable" line at verification | https://hadoop.apache.org/docs/stable/hadoop-yarn/hadoop-yarn-site/YarnCommands.html | 2026-07-10 | `yarn application -status` / `-list` distilled in references/rca-guide.md |
| Apache Hadoop API — YarnApplicationState (JavaDoc) | Hadoop 3.3.5 API (as reported by the page) | https://hadoop.apache.org/docs/stable/api/org/apache/hadoop/yarn/api/records/YarnApplicationState.html | 2026-07-10 | ACCEPTED/RUNNING state meanings distilled in references/rca-guide.md |
| Oracle Java troubleshooting guide — OutOfMemoryError | Java SE 17 | https://docs.oracle.com/en/java/javase/17/troubleshoot/troubleshooting-memory-leaks.html | 2026-07-10 | OOM message variants + causes distilled in references/rca-guide.md |
| Java SE API — java.io.NotSerializableException | Java SE 17 | https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/NotSerializableException.html | 2026-07-10 | Exception meaning distilled in references/rca-guide.md |
| GNU Bash Reference Manual — exit status of signaled commands | Bash manual, current at verification | https://www.gnu.org/software/bash/manual/bash.html | 2026-07-10 | 128+n convention distilled in references/rca-guide.md |
| POSIX (IEEE Std 1003.1) — kill utility | Issue 7, 2018 edition (pubs.opengroup.org "9699919799") | https://pubs.opengroup.org/onlinepubs/9699919799/utilities/kill.html | 2026-07-10 | Signal 9 = SIGKILL distilled in references/rca-guide.md |
| POSIX (IEEE Std 1003.1) — errno.h | Issue 7, 2018 edition (pubs.opengroup.org "9699919799") | https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/errno.h.html | 2026-07-10 | ENOSPC "No space left on device." distilled in references/rca-guide.md |
| PLAN.md §3, §5, §7 (this repo) | FINAL v5 (council complete) | ../../PLAN.md (repo root; internal) | 2026-07-10 | Internal spec for the KB layout, chunk protocol, RCA flow/template, playbook governance, and content-based redaction — distilled in SKILL.md and references/chunk-protocol.md, redaction-checklist.md, playbook-entry.md |

Verification notes (2026-07-10):

- All Spark pages fetched from the 3.5.8 documentation set (3.5.1 URLs
  now return 404; 3.5.8 is the newest 3.5.x listed on
  https://spark.apache.org/documentation.html at verification).
  Confirmed quotes include: `spark.task.maxFailures` default 4;
  `spark.stage.maxConsecutiveAttempts` default 4;
  `spark.executor.memory` / `spark.driver.memory` default 1g;
  `spark.executor.memoryOverhead` default executorMemory ×
  `spark.executor.memoryOverheadFactor` with minimum 384 (MiB);
  `spark.driver.maxResultSize` default 1g; `spark.local.dir` default
  /tmp; `spark.serializer` default org.apache.spark.serializer.JavaSerializer;
  `spark.shuffle.io.maxRetries` 3 / `spark.shuffle.io.retryWait` 5s;
  `spark.network.timeout` 120s; `spark.yarn.queue` default "default".
- The exception name "FetchFailedException" is verified through the
  Spark 3.5.8 configuration page itself (the
  `spark.shuffle.detectCorrupt.useExtraMemory` description states
  "FetchFailedException will be thrown to retry previous stage"); the
  class's own page is not published in the public 3.5.8 API docs, so
  fetch-failure SEMANTICS are sourced from the org.apache.spark.FetchFailed
  JavaDoc ("Task failed to fetch shuffle data from a remote node... need
  to rerun the previous stage"; fetch failures bypass the 4-task-failure
  abort).
- Spark error-condition messages quoted in rca-guide.md
  (UNRESOLVED_COLUMN, TABLE_OR_VIEW_NOT_FOUND, PATH_NOT_FOUND,
  SCHEMA_NOT_FOUND, CAST_INVALID_INPUT, DIVIDE_BY_ZERO, COLUMN_NOT_FOUND)
  were confirmed present on the 3.5.8 Error Conditions page.
- Hadoop pages fetched via the docs/stable alias; the YarnApplicationState
  JavaDoc page self-reports "Hadoop Main 3.3.5 API". Exit code 137 for
  over-limit containers is stated verbatim on the NodeManager
  memory-control page ("kills each container that has exceeded its
  limits", "exit code 137").
- Version caveat: defaults and error-condition names can differ across
  Spark 3.x minors. When U1 (exact org minor version) is locked at M0,
  re-verify against that version's docs and update this manifest and
  rca-guide.md; log the event in /VERIFICATION-LOG.md.
