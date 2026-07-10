# M0 Fact-Lock table

Record verified facts here during the M0 spike. Each row: fill VALUE, cite
HOW VERIFIED (who/where — admin console, `spark-submit --version`, config
file path, etc.), and set STATUS to `LOCKED` only when confirmed (not
assumed). Rows marked **M1-gate** must be LOCKED before M1 starts.

## Cost / billing (R1)

| Fact | Value | How verified | Status |
|---|---|---|---|
| Copilot billing plan (usage-based since 2026-06-01 vs legacy premium-request) | | | |
| Budget cap amount + who owns it | | | |
| Cap set as a **HARD stop** (blocks at limit, no overage allowed)? | | | |
| Cap covers BOTH KB builds AND acceptance-matrix / eval runs? | | | |
| Approx. token/credit cost of one canary + one small eval run (observed) | | | |

> GitHub budget controls can allow overage unless explicitly set to block.
> The cap must be a hard stop and must cover eval runs, not just builds.

## Platform / Spark (U1 — **M1-gate**)

| Fact | Value | How verified | Status |
|---|---|---|---|
| Platform is on-prem Hadoop/YARN? (confirm, don't assume) | | | |
| **Exact Apache Spark minor version** (e.g. 3.2.x / 3.4.x) | | | |
| AQE default-on? (yes only if ≥ 3.2 — `spark.sql.adaptive.enabled`) | | | |
| Cluster manager (YARN / standalone / k8s) | | | |

> Exact minor version is REQUIRED before any Skill C config advice — which
> configs exist and which default on depend on it.

## Scheduler (U9)

| Fact | Value | How verified | Status |
|---|---|---|---|
| Scheduler type (Airflow / Oozie / cron / control-m / …) | | | |
| Is there a scheduler export or human-maintained job list (the seed)? | | | |
| Are all jobs defined in-repo, or some only in the scheduler UI? (A8) | | | |

## Runtime evidence access (U5 / A9 — **M1-gate**)

| Fact | Value | How verified | Status |
|---|---|---|---|
| Devs have Spark History Server access? | | | |
| History Server URL / how to reach it | | | |
| **Event-log retention** (how long finished-job logs survive) | | | |
| How to fetch full YARN logs (command / UI path) | | | |

## Permissions / policy

| Fact | Value | How verified | Status |
|---|---|---|---|
| Copilot agent/skills policy name + scope (A5) | | | |
| **Dev may change Spark configs at job scope?** (A10 — **M1-gate**) | | | |
| Config-change scope: job-level only, or cluster-level too? | | | |
| Can every dev see/clone all 3-10 repos? (A7) | | | |
| Do pasted logs ever contain customer data / secrets? (A11) | | | |

## Decisions recorded at M0

| Decision | Value | Status |
|---|---|---|
| KB home (dedicated repo preferred — PLAN §3) | | |
| Skill names confirmed (or renamed): etl-knowledge-builder / etl-assistant / spark-performance-advisor | | |
| Non-prod environment available for Skill C experiments? | | |

---

**M1 entry checklist:** U1 (Spark minor version), U5 (history-server access
+ retention), A10 (config-change scope) all `LOCKED` above.
