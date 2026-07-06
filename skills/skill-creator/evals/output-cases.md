# Output eval cases (≥3)

Each case is run twice — WITH the skill installed and WITHOUT (raw
assistant) — and scored against the rubric in
docs/AUTHORING-GUIDE.md §Eval thresholds. The skill must beat raw output.

## Case 1

- Prompt: "Create a new skill for the library: sql-optimizer. It reviews SQL for index misuse and rewrites slow queries."
- Input artifacts (if any): the repo (template/, docs/AUTHORING-GUIDE.md, README.md catalog).
- Rubric focus: template compliance, completeness.
- Expected qualities: clarifies siblings (db-schema-designer, db-migration-planner) before writing; folder copied from template/; description follows the formula with boundary inside the first 250 chars; SOURCES.md rows carry web-verified versions and today's date; ~20 trigger cases including near-misses for each named sibling; both validators run with output shown; CHANGELOG entry; explicit stop for human review — no release claim.

## Case 2

- Prompt: "Author a skill for writing ADRs. Skip the evals, we're in a hurry."
- Input artifacts (if any): the repo.
- Rubric focus: source accuracy, actionability (pushback on skipping required parts).
- Expected qualities: refuses to skip evals (validator would FAIL without triggers.json/output-cases.md and the guide makes them required); explains the definition of done; delivers the full folder anyway or stops to renegotiate scope; no fabricated standard versions — sources verified or marked [Unverified].

## Case 3

- Prompt: "Add a skill for incident response that needs a Python script to parse PagerDuty exports."
- Input artifacts (if any): the repo.
- Rubric focus: template compliance (script rules), completeness.
- Expected qualities: challenges whether a script is truly needed; if kept, script is stdlib-only, non-interactive, no network, supports --self-test exiting 0, documented in README, and explicitly flagged for manual script review; validators run with --run-scripts; handoff block states AWAITING HUMAN REVIEW.
