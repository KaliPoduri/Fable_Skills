# SOURCES.md — source manifest

Every normative claim in this skill traces to a source below. Never rely on
model memory alone (risk R6). This skill is mostly internal-spec-driven:
the KB format and builder behaviors come from the repo's own PLAN.md.

| Standard / source | Exact version | Official URL | Last verified | Offline fallback |
|---|---|---|---|---|
| Fable Skills PLAN.md — §3 (KB sharded data model, budgets, stamps, pointers rule), §4 (builder behaviors: seed, cross-checks, resumable/incremental, reviewable diff), §5 (error-entry schema), §7 (content-based redaction, newbie contract), §9 R1 (usage-based Copilot billing, budget cap) | FINAL v5 (council complete, 3 rounds) | repo-internal: /PLAN.md | 2026-07-10 | Distilled into SKILL.md, references/kb-format.md, references/build-protocol.md, references/redaction-checklist.md |
| Apache Airflow documentation, core concepts "DAGs" — DAG declaration forms and schedule argument | Airflow 3.3.0 (docs "stable" at verification) | https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html | 2026-07-10 | Detection signatures distilled in references/build-protocol.md §3 |
| Apache Oozie Workflow Functional Specification — workflow-app root element, workflow.xml convention, control nodes, oozie XML namespace | Oozie 5.2.1 (project retired upstream) | https://oozie.apache.org/docs/5.2.1/WorkflowFunctionalSpec.html | 2026-07-10 | Detection signatures distilled in references/build-protocol.md §3 |

Verification notes (2026-07-10):

- Airflow page fetched; documents three DAG declaration methods (`with
  DAG(...)` context manager, standard constructor, `@dag` decorator) and
  the `schedule` argument, against Airflow 3.3.0 where imports are
  `from airflow.sdk import DAG`. Import paths differ in 2.x — so
  build-protocol.md matches loosely on `airflow` in import lines rather
  than asserting one exact path.
- Oozie spec fetched; confirms root element `<workflow-app>`, conventional
  filename `workflow.xml`, namespace `uri:oozie:workflow:*`, control nodes
  start/action/end/kill (plus decision/fork/join), spec version 5.2.1, and
  that the project is retired. Exact coordinator/bundle filenames were NOT
  individually confirmed — build-protocol.md therefore matches any XML
  carrying a `uri:oozie:` namespace instead of asserting filenames.
- cron and Control-M signatures are deliberately generic (no exact-format
  claims that would need a source): cron entries described as five time
  fields plus a command in crontab-style files; Control-M described as
  org-exported XML/JSON whose field meanings must come from the scheduling
  team, with the export itself becoming the authoritative seed. The
  workflow confirms ALL detections with the user against the seed (PLAN.md
  §4), so detection signatures are hypotheses, not normative claims.
- Org-specific facts (scheduler type, billing plan/budget cap, KB home
  decision) are M0 fact-lock items in /m0/FACT-LOCK.md — the skill detects
  or asks; it never assumes them.
