# SQL anti-pattern catalog — with rewrites

Sources: Use The Index, Luke — Markus Winand
(https://use-the-index-luke.com/) for SARGability, pagination, and
index-use patterns; PostgreSQL 18 §14.1 and MySQL 8.4 §10.8.2 for the
plan symptoms. Verified 2026-07-06. Every rewrite below is
result-equivalent unless the entry says otherwise.

For each entry: symptom in the plan → rewrite.

## 1. Leading-wildcard LIKE

`WHERE name LIKE '%smith%'` cannot seek a B-tree (no known prefix).
Plan symptom: full scan despite an index on name.
Rewrites, in order of preference:
- If the real requirement is prefix search: `LIKE 'smith%'` (seekable).
- Substring/word search: engine full-text features (PostgreSQL
  tsvector/GIN or pg_trgm; MySQL FULLTEXT; SQL Server Full-Text; Oracle
  Text).
- If requirements allow, search a normalized column (e.g., reversed
  string for suffix search).
Semantics: switching to full-text changes matching behavior (tokenizing,
stemming) — flag it.

## 2. Functions or arithmetic on indexed columns

`WHERE YEAR(order_date) = 2026`, `WHERE UPPER(email) = ?`.
Plan symptom: full scan; MySQL `possible_keys` set but `key` NULL.
Rewrite: move the computation to the constant side
(`order_date >= '2026-01-01' AND order_date < '2027-01-01'`;
store/compare a canonical-case email) or create an expression index.
See indexing.md SARGability table.

## 3. Implicit type casts

Comparing a string column to a number (or mismatched collations/Unicode).
Plan symptom: full scan; SQL Server shows CONVERT_IMPLICIT on the column
side.
Rewrite: match the parameter type to the column type; fix ORM parameter
types; align join-column types. Casting the CONSTANT is fine; casting the
COLUMN kills the index.

## 4. N+1 query pattern

Application issues one query for a list, then one query per row.
Plan symptom: not visible in a single plan — visible in logs as the same
statement executed N times with different parameters.
Rewrite: one set-based query — JOIN the child table, or
`WHERE parent_id IN (...)` / `= ANY(...)`, or a lateral/apply for top-N
per parent:
```sql
-- instead of one query per customer:
SELECT c.id, o.*
FROM customers c
JOIN LATERAL (
  SELECT * FROM orders o
  WHERE o.customer_id = c.id
  ORDER BY o.created_at DESC LIMIT 3
) o ON true
WHERE c.segment = 'vip';
```
(SQL Server/Oracle: `CROSS/OUTER APPLY`.) Application-side batching or
caching decisions belong to performance-optimizer; fix the SQL shape
here.

## 5. SELECT *

Fetches columns nobody uses; defeats covering indexes; drags wide
columns (blobs/JSON) through sorts and network.
Plan symptom: no Index Only Scan / no `Using index` even though the
needed columns are all indexed; wide `width=` in PostgreSQL.
Rewrite: list the needed columns. This alone can turn a seek+lookup plan
into index-only access.

## 6. OFFSET pagination at depth

`ORDER BY created_at DESC LIMIT 20 OFFSET 200000` reads and discards
200,000 rows on every page; cost grows with page number.
Rewrite: keyset (seek) pagination — remember the last row's sort key and
seek past it:
```sql
SELECT ... FROM orders
WHERE (created_at, id) < (:last_created_at, :last_id)
ORDER BY created_at DESC, id DESC
LIMIT 20;
```
Requires a deterministic sort key (add a tiebreaker column) and an index
matching the order. Row-value comparison is native in PostgreSQL/MySQL;
in SQL Server/Oracle expand to
`(a < :a) OR (a = :a AND id < :id)`.
Semantics: no random page jumps ("page 4000") — flag if the UI needs
them.

## 7. OR across different columns

`WHERE email = ? OR phone = ?` often prevents a single index path.
Plan symptom: full scan, or an expensive index_merge/BitmapOr.
Rewrite (equivalent when both sides are indexed):
```sql
SELECT ... WHERE email = :x
UNION
SELECT ... WHERE phone = :x;
```
Use UNION ALL + dedup key when duplicates are impossible or handled;
UNION adds a dedup step (that is what makes it equivalent).

## 8. NOT IN with a nullable subquery

`WHERE id NOT IN (SELECT customer_id FROM blacklist)` returns ZERO rows
if the subquery yields any NULL — a correctness trap and usually a bad
plan.
Rewrite:
```sql
WHERE NOT EXISTS (
  SELECT 1 FROM blacklist b WHERE b.customer_id = t.id
)
```
Semantics: CHANGED vs NOT IN when NULLs are present (NOT EXISTS is
almost always what was meant) — state this in the finding.

## 9. DISTINCT masking join fan-out

DISTINCT (or GROUP BY on everything) added to hide row multiplication
from a one-to-many join.
Plan symptom: large intermediate row counts collapsed late by a
dedup/sort node (`Using temporary` in MySQL).
Rewrite: aggregate or EXISTS before/instead of joining:
```sql
SELECT c.* FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);
```
instead of `SELECT DISTINCT c.* FROM customers c JOIN orders o ...`.

## 10. Correlated subquery executed per row

A scalar subquery in SELECT/WHERE referencing the outer row, run once
per outer row.
Plan symptom: subplan with loops = outer row count (PostgreSQL
SubPlan; MySQL DEPENDENT SUBQUERY).
Rewrite: JOIN to a grouped derived table / window function:
```sql
SELECT o.*, t.order_count
FROM orders o
JOIN (SELECT customer_id, COUNT(*) AS order_count
      FROM orders GROUP BY customer_id) t
  ON t.customer_id = o.customer_id;
```

## 11. Index-order-blind ORDER BY + LIMIT

Top-N query sorting the full result because no index provides the order.
Plan symptom: Sort (possibly spilling) feeding a Limit; MySQL
`Using filesort`.
Rewrite: index matching the ORDER BY (directions included), so the plan
becomes a pipelined top-N read. See indexing.md.

## 12. Wrapping predicates in COALESCE/ISNULL for optional filters

`WHERE col = COALESCE(:param, col)` (catch-all/kitchen-sink filters)
defeats index selection for all parameter combinations.
Rewrite: build the query with only the predicates actually supplied
(dynamic SQL with parameterized values), or engine-specific: split into
UNION ALL branches per case. Never concatenate values — parameterize
(also a security requirement; see security-code-reviewer).

## Triage order when tuning

1. Correctness traps first (entry 8).
2. Plan-breaking predicate forms (entries 1–3, 12) — cheapest wins.
3. Access-shape problems (entries 5, 6, 11) — often index + small
   rewrite.
4. Query-shape problems (entries 4, 7, 9, 10) — bigger rewrites, verify
   equivalence carefully.
