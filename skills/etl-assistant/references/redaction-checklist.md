# Safe-to-share checklist — content-based redaction

Internal spec: PLAN.md §5/§7. Redaction is CONTENT-based: it names the
content types that must never be analyzed unreviewed or persisted.
Length caps (like the 10-line excerpt rule) are brevity rules, NOT
privacy controls — a one-line secret is still a secret.

## When to run it

1. **Artifact receipt — always the FIRST response.** The moment the user
   pastes or attaches a log, physical plan, screenshot, config, or data
   sample, run this checklist and ask the user to confirm or redact
   BEFORE any analysis. Newbies paste first and read warnings second;
   that is exactly why the checklist comes first.
2. **Before any playbook entry persists.** Nothing lands in the KB (via
   PR) until the entry passes this checklist. Anything persisted to the
   KB is stripped of data VALUES regardless of length.

## The content types to scan for

| Content type | What it looks like in ETL artifacts |
|---|---|
| Secrets | Passwords or passphrases in JDBC/connection strings (`password=...`), private keys, keytab contents, wallet/credential files quoted in logs or configs |
| Tokens / credentials | API keys, bearer/session tokens, cloud access keys, service-account credentials echoed by drivers or client libraries at startup |
| Customer identifiers | Names, email addresses, phone numbers, account or card numbers, national IDs — often inside logged WHERE clauses, failed-record dumps, or screenshot table views |
| Raw data row values | Any actual field values from data rows — malformed-record echoes (e.g. the corrupt-record column), sample rows in stack traces, values printed by debug statements. Treat ALL row values as unsafe for persistence, not only obvious PII |

## How to run it on artifact receipt

1. Scan the artifact for each content type above. Screenshots count:
   read what is visible in them.
2. If anything matches (or plausibly matches), reply FIRST with: what
   was found (named by type and location — do not repeat the value),
   and ask the user to confirm sharing is acceptable or to re-paste a
   redacted version. Offer the redaction recipe below.
3. Only proceed to analysis after the user confirms or redacts.
4. If nothing matches, proceed — no ceremony needed beyond having
   actually looked.

## Redaction recipe (offer this to the user)

- Replace each secret/token with `[REDACTED]`, keeping the key name
  (`password=[REDACTED]` — the key name is diagnostic, the value never
  is).
- Replace customer identifiers and row values with typed placeholders:
  `<customer-id>`, `<email>`, `<amount>`. Keep the row STRUCTURE if the
  shape matters to the diagnosis.
- Keep: exception class names, stack frames, job/table/column names,
  file paths, timestamps, host names (unless org policy says otherwise),
  config KEYS and non-secret values. These carry the diagnostic signal.
- Watch paths and table names that embed customer names or IDs — they
  are identifiers too.

## Before a playbook entry persists (the stricter pass)

- The entry contains error PATTERNS, causes, and fixes — never data
  values. Re-check the symptom/error-pattern field especially: pasted
  error lines love to smuggle row values.
- Strip or placeholder every data value even if it looks harmless;
  "stripped of data values regardless of length" is the rule.
- Record the check: the entry schema has a "redaction-check done" field
  (references/playbook-entry.md) — set it only after this pass actually
  ran.
