# etl-assistant

Diagnoses failed ETL/Spark jobs (error to root cause with evidence and
confidence), explains how pipeline flows work in newbie language, and
improves ETL SQL/PySpark scripts statically — navigating the sharded
`etl-knowledge/` knowledge base and verifying every claim in live repo
code. Advise-only: it never changes application code; the only writes it
ever proposes are KB playbook entries via PR.

## Example prompts

- "job orders_daily failed with FetchFailedException, what's the root
  cause?"
- "explain how the billing flow works"
- "improve this PySpark script — I haven't run it yet, just review the
  code"

## Install

Copy this folder into your project's skill directory (see
[docs/PER-HARNESS-SETUP.md](../../docs/PER-HARNESS-SETUP.md) for all
harnesses and current install methods):

| Harness | Path |
|---|---|
| GitHub Copilot (VS Code) | `.agents/skills/etl-assistant/` |
| Copilot cloud agent | `.github/skills/etl-assistant/` |
| Claude Code | `.claude/skills/etl-assistant/` (also reads `.agents/skills/`) |
| Cursor | `.cursor/skills/etl-assistant/` |
| Codex | `.agents/skills/etl-assistant/` |

## Notes

- **Slow (not failed) jobs with runtime evidence** — physical plans,
  Spark UI, timings, event logs — are owned by
  **spark-performance-advisor**. This skill handles FAILED jobs and
  static (code-only) advice; there is no automatic handoff, it tells the
  user which skill to invoke.
- **KB (re)generation** is owned by **etl-knowledge-builder** (agent
  mode). This skill only reads the KB; if the KB is missing or lacks the
  job, it declares the gap and falls back to live-repo search.
- **Database EXPLAIN tuning** (PostgreSQL/MySQL/SQL Server/Oracle) is
  owned by **sql-optimizer**; **non-ETL application bugs** by
  **systematic-debugger**.
- **Agent mode is needed for the staleness check** (comparing KB
  source-commit stamps to the live repo via the terminal). Without it,
  the skill declares the step unchecked in the answer ("staleness
  unchecked — KB may lag the repo"). Adoption default pending the M0
  Copilot-mode verification: agent mode required.
- **Runtime state is never covered by the KB** (stamps cover code only):
  answers that depend on deployed configs, schedules, or schemas carry
  "KB covers code only — verify the live value before acting." at
  point-of-use.
- **Repo setup:** paste `assets/repo-instructions-snippet.md` into each
  code repo's `copilot-instructions.md` / `AGENTS.md` (three-skill
  routing + chunk-protocol note; fill in the KB repo path placeholder).
- No scripts; the skill is instructions + offline reference files only.
