# etl-knowledge-builder

Builds or regenerates `etl-knowledge/` — the sharded markdown knowledge
base mapping the org's ETL estate (job chunks, lineage, error playbook,
indexes) — from the code repos, landing every regeneration as a reviewable
git branch + PR. Batch, dev-run, rare; every claim is pointer-backed and
mechanically cross-checked in the terminal.

## Example prompts

- "Rebuild the ETL knowledge base for the billing-etl repo."
- "The KB is stale — regenerate it and open a PR."
- "Set up etl-knowledge for our pipelines; here's the scheduler export."

## Install

Copy this folder into your project's skill directory (see
[docs/PER-HARNESS-SETUP.md](../../docs/PER-HARNESS-SETUP.md) for all
harnesses and current install methods):

| Harness | Path |
|---|---|
| GitHub Copilot (VS Code) | `.agents/skills/etl-knowledge-builder/` |
| Copilot cloud agent | `.github/skills/etl-knowledge-builder/` |
| Claude Code | `.claude/skills/etl-knowledge-builder/` (also reads `.agents/skills/`) |
| Cursor | `.cursor/skills/etl-knowledge-builder/` |
| Codex | `.agents/skills/etl-knowledge-builder/` |

## Notes

- ALWAYS requires agent mode: the skill writes KB files and runs git and
  terminal commands (cross-checks, stamping, branch + PR). It does not
  work in ask-style chat modes.
- Never modifies application code — it writes only KB files, and
  regenerations land as a branch + PR, never a silent overwrite.
- Everyday questions about jobs (why a job failed, explain a flow, improve
  this SQL/script) are owned by **etl-assistant**. Slow-job tuning from
  runtime evidence (physical plans, Spark UI) is owned by
  **spark-performance-advisor**.
- KB home default: a dedicated small git repo (an `etl-knowledge/`
  subdirectory of an existing repo is supported when preferred).
- Copilot billing is usage-based: the workflow requires a HARD-stop budget
  cap before any full build and measures per-job cost on one pilot repo
  before extrapolating to the estate.
- No scripts; the skill is instructions + offline reference files only
  (library policy).
