# sql-optimizer

Optimizes slow SQL queries by reading execution plans, fixing index usage
and SARGability, and rewriting anti-patterns — delivering SQL-numbered
findings with before/after queries and a verification recipe. Vendor-
neutral core with PostgreSQL, MySQL, SQL Server, and Oracle notes.

## Example prompts

- "This query takes 30 seconds — here's the EXPLAIN ANALYZE output, make
  it fast."
- "Why isn't my index on orders(customer_id) being used?"
- "Our order-list page does a query per row and paginates with OFFSET
  200000 — tune the SQL."

## Install

Copy this folder into your project's skill directory (see
[docs/PER-HARNESS-SETUP.md](../../docs/PER-HARNESS-SETUP.md) for all
harnesses and current install methods):

| Harness | Path |
|---|---|
| GitHub Copilot (VS Code) | `.agents/skills/sql-optimizer/` |
| Copilot cloud agent | `.github/skills/sql-optimizer/` |
| Claude Code | `.claude/skills/sql-optimizer/` (also reads `.agents/skills/`) |
| Cursor | `.cursor/skills/sql-optimizer/` |
| Codex | `.agents/skills/sql-optimizer/` |

## Notes

- Table and schema design (normalization, data types, partitioning
  strategy) is owned by **db-schema-designer** (future tier).
- Rolling out index/DDL changes safely is owned by
  **db-migration-planner** (future tier) — this skill recommends indexes
  but does not execute DDL.
- Application-level performance work (profiling, caching, concurrency) is
  owned by **performance-optimizer** (future tier); this skill only fixes
  the SQL and index side of N+1-style problems.
- No scripts; the skill is instructions + offline reference files only.
