# Output eval cases (≥3)

Each case is run twice — WITH the skill installed and WITHOUT (raw
assistant) — and scored against the rubric in
docs/AUTHORING-GUIDE.md §Eval thresholds. The skill must beat raw output.

## Case 1

- Prompt: "Set up etl-knowledge for our pipelines and build it for the
  billing-etl repo — here's the scheduler export." The repo contains
  Airflow DAG files, PySpark modules, SQL files, and a params file; the
  export lists 6 jobs, one of which has no artifact in the repo.
- Input artifacts (if any): the billing-etl repo (workspace), a CSV
  scheduler export (6 jobs), no existing KB.
- Rubric focus: template compliance (sharded layout per kb-format.md,
  stamped headers with the code-only scope note, root INDEX.md written
  last), source accuracy (every read/write claim carries a repo:path:line
  pointer and a passing grep cross-check).
- Expected qualities: confirms a HARD-stop budget cap and treats this repo
  as the costed pilot BEFORE generating; uses the export as the inventory
  of record; the UI-only job is recorded as a coverage gap, not invented;
  any claim whose grep fails appears as [unverified: reason]; lands on a
  KB branch with a PR whose description is the build-session report
  (cross-check accuracy, gaps, per-job cost, next resume point);
  meta/generation.md has the ticked build-state checklist and cost log.

## Case 2

- Prompt: "warehouse-load changed a lot last sprint — update the KB for
  just that repo." An existing KB is present with stamps from the previous
  build; two of the repo's five jobs actually changed.
- Input artifacts (if any): the existing etl-knowledge repo, the changed
  warehouse-load repo, the old stamp hash in meta/generation.md.
- Rubric focus: completeness of the MINIMAL regeneration set (changed
  repo's affected jobs/ chunks, its per-repo index, affected lineage
  files, root INDEX.md — nothing else), honesty (untouched files preserved
  byte-for-byte, stamps updated only in regenerated files).
- Expected qualities: scopes the job list via git diff between the old
  stamp hash and HEAD mapped through the per-repo index; errors/ files and
  existing glossary entries untouched; a new build-state block
  (update-warehouse-load-<date>) in meta/generation.md; PR diff touches
  only the permitted file set; cross-checks re-run for regenerated chunks
  only.

## Case 3

- Prompt: "Generate the KB for the ingest-scripts repo — we have no job
  list anywhere." The repo has shell wrapper scripts and a crontab-style
  file, no scheduler export, no wiki inventory.
- Input artifacts (if any): the ingest-scripts repo only.
- Rubric focus: honesty and interaction (no invented inventory; the seed
  rule survives the missing-seed case), template compliance (provenance
  line, human-confirmed marker).
- Expected qualities: detects cron-style entries and wrapper scripts as
  hypotheses and presents them for confirmation instead of asserting an
  inventory; builds the job list interactively with the user; writes
  "inventory: human-confirmed <date> by <user>" into the per-repo index;
  jobs the user could not confirm are coverage gaps; only then traces,
  cross-checks, and writes chunks; without the skill, the assistant
  typically invents a job list from filenames and writes no provenance.
