# Playbook entries — schema, example, and the PR-only landing flow

Internal spec: PLAN.md §5 (playbook governance). Playbook entries turn a
CONFIRMED root cause into reusable knowledge in the KB's `errors/`
shard. Drafting is offered only AFTER the user confirms the root cause —
never for unconfirmed hypotheses.

## Entry schema (`errors/<YYYY-MM>.md`)

Each entry in the month file carries exactly these fields:

```markdown
## <short symptom title>

- Date: <YYYY-MM-DD>
- Job: <job slug (real name per repos/<repo>-index.md)>
- Symptom / error pattern: <the recognizable pattern — exception name,
  error condition, the shape of the failure. Patterns, never data
  values.>
- Confirmed cause: <plain-language cause + category (code | data |
  infra), confirmed by <who/how>>
- Fix: <what resolved it, advise-only phrasing, with repo:path:line
  pointers where the fix landed>
- Verification evidence: <how the fix was proven safe/effective —
  non-prod run, data check, pointer to the change>
- Redaction-check done: yes (<date>)
```

## Filled example (fictional, fully redacted)

```markdown
## orders load fails on missing daily partition

- Date: 2026-07-08
- Job: orders-daily-load (ORDERS_DAILY_LOAD)
- Symptom / error pattern: PATH_NOT_FOUND — "Path does not exist:" on
  the dt=<run-date> input partition at job start; no task-level errors.
- Confirmed cause: data/infra — the upstream export job finished after
  this job's start time on high-volume days; the partition appeared ~40
  minutes late. Code exonerated: reader path construction unchanged for
  6 months (etl-orders:jobs/orders_daily/load.py:41) and the same code
  succeeded the next run. Confirmed by the job owner on 2026-07-08.
- Fix: owner added an upstream-completion check before the read step
  (etl-orders:jobs/orders_daily/load.py:38); schedule dependency change
  tracked by the scheduling team (runtime state — KB covers code only).
- Verification evidence: non-prod rerun with the partition absent now
  waits and exits cleanly; with the partition present, output row count
  matched the prior good run.
- Redaction-check done: yes (2026-07-08)
```

## The index update — same PR, always

`errors/index.md` maps symptom/pattern → dated file + entry anchor,
because errors are retrieved by SYMPTOM, not by date. Every entry PR
also adds (or updates) its index line:

```markdown
| PATH_NOT_FOUND on daily input partition | [orders load fails on missing daily partition](2026-07.md#orders-load-fails-on-missing-daily-partition) |
```

An entry without an index line is undiscoverable — treat the pair as
one change.

## Landing flow — PR only

1. Draft the entry and the `errors/index.md` line in the KB repo on a
   branch. Never write to the KB's main branch directly, and never
   land entries by any path other than a PR.
2. Run the redaction checklist (references/redaction-checklist.md) on
   the drafted entry; set "Redaction-check done" only after it ran.
3. Open the PR and request review from the playbook reviewer named in
   the governance sheet (recorded at M0).
4. Approval criteria the reviewer checks:
   - the root cause was CONFIRMED by the user/job owner (no
     hypothesis-only entries);
   - evidence is cited (pointers, verification evidence field filled);
   - the redaction check was done — no secrets, tokens, customer
     identifiers, or raw row values anywhere in the entry;
   - advise-only respected: the entry documents what was done and by
     whom; the skill itself changed no application code.
5. Disputed causes: if the cause is contested, the entry stays OUT of
   the KB, or lands explicitly marked contested — per the governance
   sheet's disputed-cause handling. Never present a contested cause as
   confirmed.
