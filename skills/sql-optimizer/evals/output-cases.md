# Output eval cases (≥3)

Each case is run twice — WITH the skill installed and WITHOUT (raw
assistant) — and scored against the rubric in
docs/AUTHORING-GUIDE.md §Eval thresholds. The skill must beat raw output.

## Case 1

- Prompt: "This report query is slow — here's the query and the
  EXPLAIN (ANALYZE, BUFFERS) output. Make it fast." Query contains
  `WHERE YEAR(created_at) = 2025`, `SELECT *`, and an ORDER BY + LIMIT
  with a Sort node spilling to disk; plan shows Seq Scan over ~40M rows.
- Input artifacts (if any): the query text plus a pasted PostgreSQL plan.
- Rubric focus: source accuracy (plan read correctly: Seq Scan, sort
  spill, rows-removed-by-filter), template compliance (SQL-<n>, impact,
  before/after, Why, Semantics line).
- Expected qualities: SARGable date-range rewrite; explicit column list;
  composite index recommendation with column order justified
  (equality → range → order); verification section with the exact
  EXPLAIN command and the expected plan change; no semantics changes,
  each finding marked "Semantics: unchanged".

## Case 2

- Prompt: "Our customer list endpoint runs one query per customer for
  their latest 3 orders, and paginates with OFFSET. Fix the SQL." with
  the two queries and approximate table sizes.
- Input artifacts (if any): the list query, the per-row query, row
  counts; no execution plan provided.
- Rubric focus: completeness (both N+1 and OFFSET findings), actionability
  (lateral/apply top-N-per-group rewrite that actually runs), honesty
  (states plan evidence absent — expectations to verify, per constraint).
- Expected qualities: single set-based rewrite (JOIN LATERAL / APPLY);
  keyset pagination rewrite with deterministic tiebreaker and matching
  index; flags that keyset removes random page jumps (semantic/UX
  change); hands index DDL rollout to db-migration-planner.

## Case 3

- Prompt: "MySQL picks type: ALL on this query even though
  possible_keys shows an index, and there's a NOT IN subquery. EXPLAIN
  output attached — what's wrong?"
- Input artifacts (if any): query with `numeric_col = '42'` implicit
  cast, `NOT IN (SELECT nullable_col ...)`, and the tabular EXPLAIN
  output.
- Rubric focus: source accuracy (MySQL EXPLAIN columns/join types read
  per the 8.4 manual), correctness trap handling (NOT IN + NULL rewritten
  to NOT EXISTS with the semantic difference flagged as CHANGED).
- Expected qualities: implicit-cast finding with type-matched rewrite;
  NOT EXISTS rewrite whose Semantics line says results differ when the
  subquery contains NULLs and that NOT EXISTS is almost always intended;
  explanation of type: ALL vs range; verification via re-running EXPLAIN
  and comparing the key column.
