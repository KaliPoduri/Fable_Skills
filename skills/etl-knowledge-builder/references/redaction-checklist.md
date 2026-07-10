# Redaction checklist — run before ANY text persists to the KB

The rule (internal spec PLAN.md §7, verified 2026-07-10): redaction is
CONTENT-based. Anything persisted to the KB is stripped of data values
regardless of length. The ≤10-line excerpt cap is a brevity rule, NOT a
privacy control — a one-line excerpt can still leak a secret.

## Content types that must never persist

1. **Secrets and credentials:** passwords, API keys, tokens (OAuth, JWT,
   session), private keys, cloud account keys, connection strings with
   embedded credentials.
2. **Customer identifiers:** names, emails, phone numbers,
   account/customer IDs, government IDs, addresses — anything identifying
   a person or a customer organization.
3. **Raw row values:** literal data values from tables or files — sample
   rows, query results, log lines echoing record contents, test fixtures
   holding production-like values.
4. **Whatever org policy adds:** check the M0 fact-lock outcome for "do
   pasted logs contain customer data / secrets" and apply any stricter org
   rule on top.

Structural names are fine and are the KB's whole point: table names, column
names, job names, file paths, and parameter NAMES stay. Parameter VALUES
are where the risk lives.

## Procedure (per file, before it is written or committed)

1. Scan every excerpt, every quoted line, and every table cell in the file
   against the four content types above.
2. **Replace, don't delete** — keep the text readable with typed
   placeholders: `<REDACTED:token>`, `<REDACTED:connection-string>`,
   `<REDACTED:customer-id>`, `<REDACTED:row-values>`.
3. Parameter claims: record WHERE the value is set (the pointer) always;
   record the value itself only when it is not a data value
   (`spark.sql.shuffle.partitions=400` is fine; `db.password=...` is not).
4. When unsure whether a value is sensitive, redact it and keep the
   pointer — the reader can open the live file if they are entitled to.
5. Error-playbook entries (`errors/<YYYY-MM>.md`): the schema's
   `Redaction-check done: yes` line may be written only after this
   checklist has run on that entry.
6. Report findings by TYPE and count only (for example "1 connection
   string redacted") — never quote a redacted value, even partially, even
   in the build report or a commit message.

## Quick pattern sweep (heuristic aid — NOT the control)

Terminal patterns that catch common leaks before commit. The content-type
judgment above is the control; these only assist, and false negatives are
expected.

```
git grep -inE "password|passwd|secret|token|api[_-]?key|PRIVATE KEY" -- .
```

PowerShell fallback:

```
Select-String -Path <file> -Pattern "password|passwd|secret|token|api[_-]?key"
```

Also give long random-looking strings (base64/hex runs of 20+ characters) a
second look — keys rarely announce themselves.

## Examples

| Never persist | Persist instead |
|---|---|
| `jdbc:oracle:thin:...user=etl_svc&password=Xy9...` | "JDBC connection string with embedded credentials — `<REDACTED:connection-string>`; set at `billing-etl:conf/db.properties:14`" |
| Excerpt containing `WHERE customer_email = 'jane@example.com'` | "filters on `customer_email` — literal test value `<REDACTED:customer-id>`; see `billing-etl:sql/dedupe.sql:88`" |
| Sample output rows pasted from a job log | "job log echoes processed rows — `<REDACTED:row-values>`; logged at `billing-etl:jobs/rollup.sh:42`" |

## Sign-off

A file may persist only when the answer to this question is NO:

> Does any line of this file contain a data value — a secret, token,
> customer identifier, or raw row value?
