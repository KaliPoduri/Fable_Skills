# SOURCES.md — source manifest

Every normative claim in this skill traces to a source below. Never rely on
model memory alone (risk R6).

| Standard / source | Exact version | Official URL | Last verified | Offline fallback |
|---|---|---|---|---|
| Use The Index, Luke (Markus Winand) — free web edition of "SQL Performance Explained" | Web edition, maintained (copyright through 2026) | https://use-the-index-luke.com/ | 2026-07-06 | Indexing, SARGability, and pagination guidance distilled in references/indexing.md and references/anti-patterns.md |
| PostgreSQL documentation, ch. 14.1 "Using EXPLAIN" | PostgreSQL 18 (docs "current"; 18.4 at verification) | https://www.postgresql.org/docs/current/using-explain.html | 2026-07-06 | Plan-reading concepts and operator vocabulary distilled in references/execution-plans.md |
| MySQL Reference Manual, §10.8.2 "EXPLAIN Output Format" | MySQL 8.4 | https://dev.mysql.com/doc/refman/8.4/en/explain-output.html | 2026-07-06 | EXPLAIN columns, join types, and Extra values distilled in references/execution-plans.md |

Verification notes (2026-07-06):

- use-the-index-luke.com fetched; live, authored by Markus Winand, states
  it is the free web edition of "SQL Performance Explained", covers
  Oracle, MySQL, PostgreSQL, SQL Server, and Db2, with content updated
  through 2026.
- postgresql.org/docs/current/using-explain.html fetched; resolves to the
  PostgreSQL 18 manual (18.4 at verification), section 14.1 "Using
  EXPLAIN" in ch. 14 "Performance Tips".
- dev.mysql.com page fetched; confirmed as MySQL 8.4 Reference Manual
  §10.8.2 "EXPLAIN Output Format" including the output-column table and
  join-type list used in references/execution-plans.md.
- SQL Server and Oracle notes in the reference files are cross-engine
  translations of the concepts above plus vendor terminology as presented
  on use-the-index-luke.com (which tests against both engines); no
  separate vendor manual was verified for them — treat vendor-specific
  operator names for SQL Server/Oracle as [lower-confidence] and confirm
  against the local team's engine documentation when precision matters.
