# Index selection and SARGability

Source: Use The Index, Luke — Markus Winand
(https://use-the-index-luke.com/, free web edition of "SQL Performance
Explained", verified 2026-07-06). Engine-neutral B-tree guidance; engine
notes flagged inline.

## How a B-tree index is used

An index is an ordered structure. A query benefits when it can descend to
a start point and read a contiguous range. Everything below follows from
that single fact:

- Equality predicates pin an exact position → cheapest.
- One range predicate (>, <, BETWEEN, LIKE 'abc%') defines a scan
  interval → cheap, but columns AFTER the range column in the index no
  longer narrow the scan.
- Predicates the engine cannot map to the index order (functions on the
  column, leading wildcards, type-mismatched comparisons) make the index
  unusable for seeking — at best it is fully scanned.

## SARGability rules (Search ARGument able)

A predicate is SARGable when the indexed column stands alone on one side,
untransformed:

| Not SARGable | SARGable rewrite |
|---|---|
| `WHERE UPPER(name) = 'X'` | function/expression index on UPPER(name), or store normalized column |
| `WHERE created_at + interval '1 day' > now()` | `WHERE created_at > now() - interval '1 day'` |
| `WHERE YEAR(order_date) = 2026` | `WHERE order_date >= '2026-01-01' AND order_date < '2027-01-01'` |
| `WHERE CAST(id_text AS INT) = 42` | fix the column type, or compare as text `id_text = '42'` |
| `WHERE amount * 1.1 > 100` | `WHERE amount > 100 / 1.1` |
| `WHERE name LIKE '%son'` | see anti-patterns: leading wildcard cannot seek |
| `WHERE numeric_col = '42'` (implicit cast) | compare with matching type `= 42` |

Implicit casts hide easily: parameter types from ORMs/drivers (e.g.,
sending Unicode for a non-Unicode column in SQL Server), joining columns
of different types, comparing strings to numbers. The plan shows a
conversion on the COLUMN side when the index is lost; conversion on the
parameter side is harmless.

When the transformation is genuinely needed, index the expression:
PostgreSQL and Oracle support expression/function-based indexes; MySQL
8.0+ supports functional index parts; SQL Server uses computed columns
(optionally persisted) with an index.

## Composite index column order

Order columns by how the query constrains them, not by selectivity
folklore:

1. Columns compared with EQUALITY (in any query the index should serve).
2. Then AT MOST ONE range column (the range ends index-assisted
   narrowing).
3. Then ORDER BY / covering columns.

Example: `WHERE tenant_id = ? AND status = ? AND created_at > ? ORDER BY
created_at` → index `(tenant_id, status, created_at)`. The same index
serves `tenant_id+status` equality-only queries too.

Consequences:
- An index on `(a, b)` serves `WHERE a = ?` but generally NOT `WHERE
  b = ?` alone (leftmost-prefix rule).
- `(a, b)` plus a separate `(a)` is usually redundant — the composite
  covers the prefix. Flag redundant indexes; removal ships via
  db-migration-planner.
- Putting the range column first (`(created_at, tenant_id)`) forces
  scanning the whole date interval across all tenants — a common
  real-world mistake.

## Covering indexes

If the index contains every column the query touches (predicates, join
keys, ORDER BY, and selected columns), the engine never visits the table:
PostgreSQL Index Only Scan, MySQL `Using index`, SQL Server seek without
Key Lookup (add non-key columns with `INCLUDE`), Oracle avoids TABLE
ACCESS BY INDEX ROWID.

Use covering indexes to kill lookup storms: a seek returning 10k rows
that each trigger a row fetch is often slower than a slightly wider
index. Cost: bigger index, slower writes — cover deliberately, not by
adding every column.

## Selectivity and when an index will not be chosen

- Selectivity = fraction of rows a predicate keeps. Indexes win on
  selective predicates; if a predicate keeps a large share of the table
  (rule of thumb: more than roughly 5–15%, engine- and width-dependent),
  a full scan is usually correct and the optimizer is right to ignore
  the index.
- Low-cardinality columns (status with 3 values, booleans) rarely
  deserve a standalone index — but work well as the FIRST equality
  column of a composite, or as a partial/filtered index:
  `CREATE INDEX ... WHERE status = 'PENDING'` (PostgreSQL partial,
  SQL Server filtered; MySQL: no direct equivalent — use composite
  order instead).
- If the optimizer ignores a suitable index, check in this order:
  (1) predicate SARGable? (2) statistics fresh (ANALYZE / UPDATE
  STATISTICS)? (3) selectivity actually good? (4) implicit cast?
  Only then consider engine-specific hints — and treat hints as a
  last-resort finding with the reason documented.

## ORDER BY, GROUP BY, and indexes

- An index whose column order matches the ORDER BY (same directions, or
  all-reversed) lets the engine skip the sort entirely — this is what
  makes keyset pagination fast (see anti-patterns).
- A pipelined top-N (`ORDER BY indexed_col LIMIT n`) reads only n index
  entries; the same query without index order sorts the whole result.
- GROUP BY on the leading index columns can aggregate without a
  temporary/hash step (MySQL: avoids `Using temporary`).

## Index cost honesty

Every index slows INSERT/UPDATE/DELETE and consumes space. Recommend the
smallest set of indexes serving the observed queries; prefer widening or
reordering an existing index over adding near-duplicates. DDL rollout
(online build, locking, replication lag) belongs to db-migration-planner.
