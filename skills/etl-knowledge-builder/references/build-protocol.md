# Build protocol — bootstrap, seed, detection, tracing, checks, checkpoints

Operational detail behind the SKILL.md workflow. Distilled from the internal
spec PLAN.md §4 (verified 2026-07-10); scheduler signatures sourced per
`SOURCES.md`.

## 1. KB home and bootstrap

**Default: a dedicated small git repo.** It keeps stale KB text out of
Copilot's implicit context in the code repos, and keeps stamping and diffing
clean. Bootstrap:

1. Create an empty repo named `etl-knowledge` on the org's git host; clone
   it next to the code repos.
2. Lay down the initial structure per `kb-format.md`: placeholder
   `INDEX.md`, empty `repos/`, `jobs/`, `lineage/`, `errors/` directories
   (a `.gitkeep` in each), a `glossary.md` stub, and a `meta/generation.md`
   skeleton.
3. First commit directly to the default branch (the only time that is
   allowed): `git add -A` then
   `git commit -m "etl-knowledge: initial layout, no content yet"`, push.
4. Ask an admin to protect the default branch so all regenerations land via
   PR from then on.

**Alternative (supported, not the default):** an `etl-knowledge/`
subdirectory inside an existing repo. Same layout, same PR-only rule. Use it
only when the user prefers it; its drawbacks are that KB text enters
Copilot's implicit context for that repo and KB diffs interleave with
application history.

## 2. The authoritative job seed

- **What qualifies:** a scheduler export (any format the org's scheduler
  produces) or a human-maintained job list (spreadsheet, wiki page,
  runbook).
- **The rule:** the seed is the inventory of record. Tracing fills per-job
  detail; it never adds or removes jobs on its own authority.
- **No seed exists:** build the list interactively — walk the repos (and
  the scheduler UI, via the user) together; ask the user to name, confirm,
  or reject each candidate job. Write the confirmed list into the per-repo
  index with the provenance line
  `inventory: human-confirmed <date> by <user>`, and treat it as the seed
  from then on.
- **Seed vs detection mismatches:** list every one; the user arbitrates
  (add / remove / defer). Deferred items are coverage gaps in
  `meta/generation.md`. A job defined only in the scheduler UI (nothing in
  any repo) is always recorded as a gap — its schedule comes from the seed,
  and its chunk says the definition is out-of-repo.

## 3. Scheduler detection signatures

Start scheduler-agnostic. Scan every repo for ALL of the signatures below,
then confirm findings with the user against the seed. Every detection is a
hypothesis until confirmed.

### Airflow (verified against Airflow 3.3.0 docs — see SOURCES.md)

Python files that import from Airflow packages and declare a DAG (directed
acyclic graph — Airflow's unit of scheduling). Three declaration forms:
`with DAG(...)` context manager, `DAG(...)` constructor assignment, and the
`@dag` decorator. Import paths vary by major version (`from airflow.sdk
import DAG` in 3.x, other `airflow` paths in 2.x) — match loosely on
`airflow` in the import line. Look for `schedule` / `schedule_interval`
arguments; DAG files conventionally live under a `dags/` folder.

```
git grep -nE "^(from|import) airflow" -- "*.py"
git grep -nE "DAG\(|@dag" -- "*.py"
```

### Oozie (verified against the Oozie 5.2.1 workflow spec — see SOURCES.md)

XML files carrying a `uri:oozie:` namespace. Workflow definitions use root
element `<workflow-app>` (conventional filename `workflow.xml`) with control
nodes `<start>`, `<action>`, `<end>`, `<kill>` (plus decision/fork/join).
Coordinator/bundle definitions are separate oozie-namespaced XML — match on
the namespace rather than filenames. `job.properties` files usually sit
alongside. Note the Oozie project is retired upstream; orgs still run it.

```
git grep -n "uri:oozie:" -- "*.xml"
git ls-files -- "*workflow*.xml" "*coordinator*.xml" "*.properties"
```

### cron (generic — formats vary; read, don't pattern-match blindly)

Crontab-style lines: five time fields followed by a command, in files like
`crontab.txt`, files under a `cron.d/`-style directory, or deploy scripts
that invoke `crontab`. A rough sweep (expect false positives — confirm each
hit by eye):

```
git grep -nE "^[0-9*/,-]+ +[0-9*/,-]+ +[0-9*/,-]+ +[0-9*/,-]+ +[0-9*/,-]+ +\S" 
git grep -in "crontab"
```

### Control-M (generic — formats vary by version; never guess field meanings)

Job-definition exports produced by Control-M tooling, typically XML or JSON.
Do not interpret fields from memory: ask the scheduling team for a current
export and treat THAT as the seed.

```
git grep -ilE "control-?m"
```

### Custom / other

Anything that names jobs + schedules + commands: YAML/JSON/INI job configs,
shell wrapper scripts invoked by an external scheduler. If entry scripts
exist but NO scheduling artifact is found anywhere, schedules likely live
only in a scheduler UI — record that as a coverage gap and take schedules
from the seed.

## 4. Per-job tracing method

One job at a time, small steps:

1. **Entry.** Start at the entry script named by the seed/scheduler
   artifact. Path-confirm it exists before anything else.
2. **Follow the chain.** Read the entry script; follow what it invokes
   (spark-submit calls, Python modules, SQL files, child shell scripts) a
   few hops at most — record each hop with a `repo:path:line` pointer.
3. **Reads.** SQL `FROM`/`JOIN` targets; `spark.read` / `spark.table` /
   `spark.sql` sources; input file paths. Record the exact site of each.
4. **Writes.** `INSERT` / `CREATE TABLE` / `MERGE` targets; `saveAsTable` /
   `insertInto` / `.write` paths. Record the exact site of each.
5. **Key parameters.** Where each value comes from: CLI args, config/params
   files, environment variables, scheduler-injected variables. Record the
   setting site. A value injected at runtime and absent from the repo is
   stated as such (a code-only stamp limit) — never guessed.
6. **Upstream/downstream.** Prefer explicit scheduler dependencies. Where
   absent, infer writer→reader edges from shared tables and mark them
   `(inferred)`.
7. **Known failure points.** Only what the code shows (retry logic, error
   handling, fragile paths, TODO/FIXME) or the user states. Never invent.
8. **Narrative.** 1–3 short plain-language paragraphs for a Spark newbie:
   what comes in, what happens, what goes out, when it runs.

## 5. Mechanical cross-check patterns

Run in the agent-mode terminal — this library ships no scripts. These checks
exist because LLM tracing can be confidently wrong; a KB poisoned by wrong
lineage is worse than no KB.

- **Table/file claim:** for EVERY entry in Reads/Writes:
  `git grep -n "<name>" -- "<cited-path>"` — pass only if the cited line
  number appears in the output. PowerShell fallback:
  `Select-String -Path "<cited-path>" -Pattern "<name>"` (its line numbers
  serve the same purpose).
- **Entry script:** `git ls-files -- "<path>"` must return the path
  (tracked in git). PowerShell fallback: `Test-Path "<path>"` must be True.
- **Dynamic names** (table names assembled from variables at runtime): a
  grep for the final name will rightly fail. Cite the assembly site instead
  and mark the claim `[unverified: name assembled at runtime from <var> at
  <repo:path:line>]`.
- **On failure:** a failed check never blocks the build and never gets
  stated as fact — write the claim with its `[unverified: ...]` marker,
  count it, move on.
- **Accuracy:** per repo, record `checks passed / checks run` as a
  percentage in `meta/generation.md`. This feeds the owner-sampling review
  at M2.

## 6. Resumable checkpointing

Copilot's per-session agentic depth is unknown — assume the session can end
after any step.

- `meta/generation.md` holds the build-state checklist (format in
  `kb-format.md`): one line per job, plus lines for lineage, per-repo index,
  and root index, per repo in scope.
- **After EVERY job:** tick its line, append its cost row, and commit the KB
  branch. Small commits are fine — they are reviewed as one PR.
- **On resume:** read the checklist; verify the last ticked job's chunk file
  actually exists (a session can die between write and tick — trust the
  files first, then the ticks); continue at the first unchecked line.
- Never regenerate an already-ticked job within the same build unless the
  user asks.

## 7. Incremental mode

Use when one repo (or a small set) changed and the estate is otherwise
current.

- **Scope — regenerate ONLY:** (1) the changed repo's `jobs/` chunks — if
  the change is small, only jobs whose files changed: run
  `git diff --name-only <old-stamp-hash>..HEAD` in the code repo and map
  changed paths to jobs via the per-repo index; (2) that repo's
  `repos/<repo>-index.md`; (3) `lineage/` files that mention affected
  tables; (4) root `INDEX.md`.
- **Preserve byte-for-byte:** everything else — especially `errors/` files
  and existing `glossary.md` entries (human-curated).
- Update stamps only in regenerated files. Add a new build-state block
  (`update-<repo>-<date>`) to `meta/generation.md`.

## 8. Per-job cost logging and the pilot gate

Copilot billing is usage-based — cost is extrapolated from measurement,
never guessed.

- Log per job in `meta/generation.md`: prompts sent (count), approximate
  tokens if the surface shows them (else "n/a"), wall-clock minutes, date.
- **Pilot procedure (before the first full build):** pick ONE representative
  repo → build it fully → sum its per-job costs → extrapolate: mean cost per
  job × total jobs in the seed across the estate → present the estimate to
  the user next to the budget cap → proceed only on explicit go-ahead.
- Every later session appends to the cost log, keeping the estimate honest.

## 9. Landing the change

- Branch names: `kb/full-<date>`, `kb/update-<repo>-<date>`,
  `kb/resume-<date>`.
- Commit at every checkpoint; the final commit finalizes
  `meta/generation.md`.
- Open a PR whose description is the build-session report (SKILL.md output
  template). If PRs are unavailable, stop after committing to the branch and
  hand the user the diff (`git diff <default-branch>...HEAD`).
- Never merge; never push to the default branch (bootstrap's first commit is
  the sole exception). The org's named reviewer(s) approve.
