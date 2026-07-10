---
name: etl-knowledge-builder
description: "Builds or regenerates the etl-knowledge KB (the sharded markdown map of the org's ETL jobs) from the repos in Copilot agent mode. Use this skill when asked to rebuild, regenerate, or update the ETL knowledge base or generate the KB for a repo. Do not use to answer questions about jobs — that is etl-assistant; slow-job tuning is spark-performance-advisor. Covers first-time etl-knowledge setup and incremental updates; writes only KB files, never app code; regens land as a PR."
metadata:
  version: "1.0.0"
  last-verified: "2026-07-10"
---

# ETL Knowledge Builder

(Re)generate `etl-knowledge/` — the sharded markdown knowledge base that maps
the org's ETL estate (3–10 repos of SQL, shell scripts, Python/PySpark, and
scheduler configs) — as a reviewable git change. Work from an authoritative
job seed, trace one job at a time, prove every claim with a mechanical
cross-check, and checkpoint after every job so a cut-short session resumes
cleanly. The KB holds pointers and plain-language narrative, never code
copies; the live repos stay the source of truth.

## Constraints

Assume no external internet access, no paid tools, and English output.
Never send project code or data to external services.
Agent mode required: this skill writes files and runs git and terminal
commands; refuse to run in a mode that cannot do both.
Never modify application code: write only files inside the KB directory
(`etl-knowledge/`); a build that would touch anything else stops and reports.
Regeneration lands as a branch + PR (or reviewable diff) — never a silent
overwrite, never a direct push to the default branch.
Run `references/redaction-checklist.md` on every file before it persists;
anything persisted is stripped of data values (secrets, tokens, customer
identifiers, raw row values) regardless of length.
A claim that fails its mechanical cross-check is marked unverified in the
chunk — never stated as fact.
Confirm a HARD-stop budget cap exists before any full build: Copilot billing
is usage-based, and a full KB build is token-heavy.
Never guess org facts (scheduler type, job inventory, KB home): detect from
the repos, then confirm with the user.
Write narratives for Spark newbies: plain language, jargon defined in
parentheses at first use.

## Workflow

1. **Preconditions (step 0 — before anything is generated).**
   - Confirm agent mode: file writes and terminal commands both available.
   - Confirm with the user that a budget cap exists and is configured as a
     HARD stop (blocks at the limit — no overage) covering this build. Do
     not start a full build without it.
   - First full build of the estate: build ONE pilot repo first, record its
     per-job cost (prompts / approximate tokens / wall time) in
     `meta/generation.md`, extrapolate to the whole estate, and get the
     user's explicit go-ahead before continuing.
   - Locate the KB. Default home is a dedicated small git repo; if none
     exists, bootstrap it per `references/build-protocol.md` (a subdirectory
     of an existing repo is supported when the user prefers it).
2. **Resume or start.** Read `meta/generation.md`. If its build-state
   checklist shows an unfinished build, resume at the first unchecked item —
   never redo finished jobs. Otherwise agree the mode with the user: full
   build, or incremental (one changed repo — see step 8's scope rule).
3. **Get the authoritative job seed.** A scheduler export or a
   human-maintained job list is the inventory of record; LLM tracing only
   fills per-job detail — it never decides which jobs exist. If neither
   exists, build the list interactively with the user and mark it
   human-confirmed in the KB. Details in `references/build-protocol.md`.
4. **Detect scheduler artifacts (scheduler-agnostic).** Do not assume a
   scheduler type. Scan each repo for Airflow DAG files, Oozie XML, cron
   entries, Control-M exports, and custom job configs using the signatures
   in `references/build-protocol.md`. Treat every detection as a hypothesis.
5. **Confirm the inventory.** Present the detected jobs next to the seed and
   have the user resolve every mismatch (in seed but not found; found but
   not in seed). Record unresolved items as coverage gaps in
   `meta/generation.md`.
6. **Trace each job — small steps, checkpoint each.** For each confirmed
   job, one at a time: follow the entry script; identify tables/files read
   and written, key params and where they are set, upstream/downstream jobs,
   and known failure points — every claim with a `repo:path:line` pointer
   and excerpts of at most 10 lines. Then run step 7's cross-checks for that
   job, write its `jobs/<job>.md` chunk per `references/kb-format.md`, run
   the redaction checklist, and tick the job in `meta/generation.md` with
   its cost line. Never batch several jobs into one unsaved step — the
   session may end at any time.
7. **Mechanical cross-checks (agent-mode terminal, no scripts).** Before a
   claim persists:
   - Every claimed table/file read or write is grep-confirmed at the cited
     site: `git grep -n "<table_name>" -- "<cited-path>"` must hit the cited
     line (PowerShell fallback: `Select-String -Path "<cited-path>"
     -Pattern "<table_name>"`).
   - Every entry script's existence is path-confirmed:
     `git ls-files -- "<path>"` returns it (or `Test-Path` is True).
   A claim that fails is written into the chunk marked
   `[unverified: <reason>]` — never stated as fact. Record per-repo accuracy
   (checks passed / checks run) in `meta/generation.md`.
8. **Write shared files in this exact order.** After a repo's jobs:
   `lineage/<domain>.md` files, then `repos/<repo>-index.md`. After ALL
   repos in scope: root `INDEX.md` LAST, so it never links to files that do
   not exist yet. Incremental mode regenerates only: the changed repo's
   `jobs/` chunks, its per-repo index, affected `lineage/` files, and the
   root `INDEX.md`; everything else — especially the human-curated `errors/`
   files and glossary entries — is preserved byte-for-byte.
9. **Stamp everything.** Every generated file's header records the source
   repo commit hashes plus the scope note that stamps cover CODE ONLY (not
   runtime scheduler state, deployed configs, or schemas) — exact header in
   `references/kb-format.md`. Finalize `meta/generation.md`: repos +
   commits, generated-when, coverage gaps, per-repo accuracy %, build-state
   checklist, per-job cost log.
10. **Land as a reviewable diff.** Commit on a KB branch (for example
    `kb/full-<date>` or `kb/update-<repo>-<date>`), push, open a PR with the
    build-session report below as its description — or hand the user the
    diff. Never merge it yourself.

## Output template

```markdown
# KB build session report — <date>

## Mode and scope
- Mode: full | incremental | resume
- Repos processed: <repo> @ <commit hash>, ...
- KB branch / PR: <branch, PR link, or "diff handed to user">

## Built
| Repo | Jobs traced | Chunks written | Lineage files touched | Index |
|---|---|---|---|---|

## Cross-check results
- Checks run / passed: <n>/<n> — per-repo accuracy: <repo>: <n>%
- Claims marked [unverified]: <count> — <job>: <claim>: <reason>; ...

## Coverage gaps
- <job or artifact>: <why it could not be traced, or seed mismatch left open>

## Cost
- This session, per job: <job>: <prompts / ~tokens / minutes>; ...
- Running estimate vs budget cap: <under | approaching | pilot extrapolation: X>

## Redaction
- Checklist run on every persisted file: yes.
- Findings by type only: <none | e.g. "1 connection string redacted"> —
  never quote a redacted value.

## Next resume point
- <first unchecked item in meta/generation.md, or "build complete">
```

## References (load on demand)

- `references/SOURCES.md` — source manifest (always present).
- `references/kb-format.md` — load before writing ANY KB file; the sharded
  layout, per-file specs and budgets, header/stamp template, slug rules.
- `references/build-protocol.md` — load at steps 1–8; KB bootstrap, seed
  handling, scheduler detection signatures, per-job tracing method,
  cross-check command patterns, checkpointing, incremental rules, cost
  logging, PR landing.
- `references/redaction-checklist.md` — load before any text persists to
  the KB.

## Checklist

- [ ] Agent mode confirmed; HARD-stop budget cap confirmed before a full
      build; first full build costed on one pilot repo and approved.
- [ ] Authoritative seed identified — or built interactively and marked
      human-confirmed.
- [ ] Detected inventory confirmed with the user; mismatches recorded as
      coverage gaps.
- [ ] Every claim carries a repo:path:line pointer; excerpts ≤10 lines.
- [ ] Every table/file and entry-script claim cross-checked; failures
      marked [unverified], never stated as fact.
- [ ] Redaction checklist run on every persisted file.
- [ ] Every generated file stamped with source commits + the code-only
      scope note in its header.
- [ ] meta/generation.md updated after every job (checklist tick, cost
      line) and finalized (gaps, accuracy %).
- [ ] Root INDEX.md written last; incremental runs touched only the
      permitted file set.
- [ ] Landed as branch + PR/diff; no direct overwrite; no application code
      modified.
- [ ] Output follows the template above.
