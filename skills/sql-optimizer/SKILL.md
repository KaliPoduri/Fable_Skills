---
name: sql-optimizer
description: Optimizes slow SQL - reads EXPLAIN plans, fixes index usage, SARGability, join strategy, and anti-patterns like leading-wildcard LIKE and N+1. Use this skill when asked to speed up a slow query or tune SQL. Do not use for table or schema design; use db-schema-designer instead. Migrations belong to db-migration-planner, application-level profiling to performance-optimizer.
metadata:
  version: "1.0.0"
  last-verified: "2026-07-06"
---

# SQL Optimizer

Make specific SQL queries faster with evidence, not folklore. Read the
execution plan, find the operation that hurts, and deliver numbered
findings (SQL-1, SQL-2, ...) each with a before/after query and the reason
the rewrite wins. Core guidance is vendor-neutral, with engine notes for
PostgreSQL, MySQL, SQL Server, and Oracle.

## Constraints

Assume no external internet access, no paid tools, and English output.
Never send project code or data to external services.
Never change what a query returns: every rewrite must be
result-equivalent, or the semantic difference must be flagged in the
finding and approved by the user.
Recommend indexes; do not run DDL yourself. Index changes ship via the
team's migration process (db-migration-planner).
Base claims on the plan and schema provided. When you cannot see a plan,
label predictions as expectations to verify, not facts.
For general code-quality review of the surrounding application code, use
code-reviewer; this skill covers the queries themselves.

## Workflow

1. **Collect inputs.** Ask for (or locate in the repo): the query, the
   engine and version, the execution plan, table sizes (approximate row
   counts), and existing indexes (`\d table`, `SHOW INDEX FROM`,
   `sp_helpindex`, or DDL). If no plan is available, show the user the
   exact command to produce one:
   - PostgreSQL: `EXPLAIN (ANALYZE, BUFFERS) <query>;`
   - MySQL: `EXPLAIN FORMAT=JSON <query>;` (or `EXPLAIN ANALYZE`)
   - SQL Server: `SET STATISTICS IO, TIME ON;` + actual execution plan
   - Oracle: `EXPLAIN PLAN FOR <query>;` then
     `SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);`
   Warn that ANALYZE variants execute the query — never on destructive
   statements.
2. **Read the plan.** Load `references/execution-plans.md`. Identify:
   the most expensive operations, full scans on large tables, row-estimate
   vs actual mismatches, join order and strategy, sorts and temporary
   results, lookup storms (many rows through a per-row lookup).
3. **Check SARGability and anti-patterns.** Load
   `references/anti-patterns.md` and test the query against the catalog:
   functions or casts on indexed columns, leading-wildcard LIKE, implicit
   type conversion, SELECT *, OR across columns, NOT IN with nullable
   subqueries, OFFSET pagination at depth, N+1 access from the
   application, DISTINCT papering over join fan-out.
4. **Evaluate indexes.** Load `references/indexing.md`. For each
   predicate/join/sort column set, decide: is there an index the query
   can use as written? Would a composite (equality columns first, then
   one range column, then sort/covering columns) or covering index
   remove the bottleneck? Is selectivity high enough that the index will
   actually be chosen? Flag redundant indexes you notice, but schema
   redesign belongs to db-schema-designer.
5. **Rewrite.** Produce the improved query. Keep rewrites
   result-equivalent; when a faster form changes semantics (e.g., NOT IN
   vs NOT EXISTS under NULLs), say so explicitly in the finding.
6. **Record findings.** One SQL-<n> per distinct issue, ordered by
   expected impact, using the Output template.
7. **Verify.** Give the user a verification recipe: re-run the same
   EXPLAIN command, name the plan change to look for (e.g., "Seq Scan on
   orders becomes Index Scan using ix_orders_customer_created"), and
   compare timings/IO on realistic data volumes — not an empty dev table.
   Confirm the rewritten query returns identical results (row count +
   checksum or ORDER BY comparison).

## Output template

```markdown
# SQL Optimization Report — <query name or location>

## Context
- Engine/version: <e.g., PostgreSQL 18>
- Tables and sizes: <table: ~rows>
- Plan evidence: <provided | reproduced with command X | none — expectations only>

## Findings

### SQL-1: <short title>
- **Impact:** High | Medium | Low — <what the plan shows, e.g., "Seq Scan over 40M rows">
- **Issue:** <anti-pattern or plan problem, named>
- **Before:**
  ```sql
  <original query or fragment>
  ```
- **After:**
  ```sql
  <rewritten query or fragment>
  ```
- **Why:** <mechanism: which operation this removes or replaces>
- **Semantics:** unchanged | CHANGED: <exact difference, needs approval>

### SQL-2: ...

## Index recommendations
| # | Table | Proposed index | Serves | Trade-off |
|---|---|---|---|---|
<columns in order, with reasoning: equality → range → include/covering.
Note write overhead and hand off DDL rollout to db-migration-planner.>

## Verification
1. <EXPLAIN command to re-run>
2. <expected plan change>
3. <result-equivalence check>
```

## References (load on demand)

- `references/SOURCES.md` — source manifest (always present).
- `references/execution-plans.md` — load at step 2; how to read plans and
  the operator vocabulary per engine.
- `references/indexing.md` — load at step 4; index selection, composite
  column order, covering indexes, selectivity, SARGability rules.
- `references/anti-patterns.md` — load at step 3; the anti-pattern
  catalog with before/after rewrites.

## Checklist

- [ ] Plan evidence stated (provided, reproduced, or explicitly absent).
- [ ] Every finding has SQL-<n>, impact, before/after SQL, and the
      mechanism ("Why").
- [ ] Every rewrite is result-equivalent or the semantic change is
      flagged in a Semantics line.
- [ ] Index recommendations give column order and the predicate/sort
      they serve; DDL handed off, not executed.
- [ ] Verification section tells the user how to prove the win on
      realistic data.
- [ ] Output follows the template above.
