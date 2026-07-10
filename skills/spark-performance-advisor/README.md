# spark-performance-advisor

Tunes slow (not failed) Apache Spark jobs interactively from the user's
own runtime evidence — physical plan text, Spark UI observations, YARN
logs. Plain-language interview for Spark newbies, then a diagnosis with
SQL rewrites and/or specific config parameters, delivered with a
non-prod experiment protocol. Advise-only: it never executes anything
against a cluster and requires the exact Spark 3.x minor version before
any config advice.

## Example prompts

- "This Spark job is slow, here's the physical plan — what's wrong?"
- "My pipeline used to take 20 minutes, now it takes 2 hours. Nothing
  failed. Where do I start?"
- "The Spark UI shows 2 tasks in one stage taking 25 minutes while the
  other 198 finish in seconds."

## Install

Copy this folder into your project's skill directory (see
[docs/PER-HARNESS-SETUP.md](../../docs/PER-HARNESS-SETUP.md) for all
harnesses and current install methods):

| Harness | Path |
|---|---|
| GitHub Copilot (VS Code) | `.agents/skills/spark-performance-advisor/` |
| Copilot cloud agent | `.github/skills/spark-performance-advisor/` |
| Claude Code | `.claude/skills/spark-performance-advisor/` (also reads `.agents/skills/`) |
| Cursor | `.cursor/skills/spark-performance-advisor/` |
| Codex | `.agents/skills/spark-performance-advisor/` |

## Notes

- FAILED jobs (error → root cause), "explain flow X", and static
  improvement of ETL SQL/scripts are owned by **etl-assistant** — this
  skill triages failed-vs-slow at intake and tells the user to invoke
  etl-assistant for failures (no automatic handoff exists).
- Database-engine SQL tuning with EXPLAIN plans (PostgreSQL, MySQL,
  SQL Server, Oracle) is owned by **sql-optimizer**; Spark jobs are not
  its territory, and classic DB queries are not this skill's.
- (Re)generating the etl-knowledge KB is owned by
  **etl-knowledge-builder**.
- Advise-only: never executes against clusters or production; config
  changes are job-scoped by default, cluster-scoped items are flagged
  "requires cluster admin", and all config changes need job-owner
  approval.
- This skill itself requires only chat access (read/advise-only); wider
  agent-mode behavior is pending M0 verification — the suite's adoption
  default is "agent mode required".
- No scripts; the skill is instructions + source-verified offline
  reference files only (defaults verified against Apache Spark 3.5.8
  docs, with 3.0–3.5 version notes).
