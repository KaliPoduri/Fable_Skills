# Maintenance runbook

Working reference for the six maintenance jobs. Summarizes repo docs —
READ THE LIVE docs/AUTHORING-GUIDE.md AS THE AUTHORITY; if this file and
the guide disagree, the guide wins and this file needs a fix.

## Job order for a full quarterly pass

1. Staleness sweep → 2. Re-verify stale skills → 3. Bumps for anything
changed → 4. (deprecations only if requested) → 5. Full validation →
6. Consistency checks → report.

## Re-verification decision table (per SOURCES.md row)

| Web check result | Row action | Skill action | Log |
|---|---|---|---|
| Same version, URL alive | update Last verified date | none | VERIFICATION-LOG row: OK |
| New version published | update version + date | re-distill references/*.md; MINOR bump (MAJOR if guidance changes meaning) | row: CHANGED + what |
| URL moved (redirect) | update URL + date | none unless content changed | row: OK, note new URL |
| Source unreachable | mark `[Unverified — source unreachable <date>]`, keep old data | offline fallback stays authoritative; flag to user | row: GONE/unreachable |

`metadata.last-verified` moves to today only when EVERY row in that
skill was re-checked this session.

## VERIFICATION-LOG.md row format (append-only)

`| YYYY-MM-DD | <source / claim> | OK / CHANGED / unreachable | <who> | <notes> |`

One row per verification EVENT — the same source reappears each time it
is re-checked. Never rewrite or delete old rows. Check the file's
"still-unverified" list while there; remove an item from that list only
when it has been verified and logged.

## SemVer triage (SemVer 2.0.0, verified 2026-07-06)

| Change to a skill | Bump |
|---|---|
| Typo, wording, formatting, last-verified date refresh | PATCH |
| Eval cases added/refined, README clarifications | PATCH |
| New reference file, expanded workflow, new optional output section | MINOR |
| Re-distilled sources after upstream version change (same guidance) | MINOR |
| Changed scope/boundary or description triggers | MAJOR |
| Changed output template headings/format consumers rely on | MAJOR |
| Deprecation | MAJOR |

Keep `version` a quoted string in frontmatter.

## CHANGELOG categories (Keep a Changelog 1.1.0, verified 2026-07-06)

Under `## [Unreleased]`: `### Added`, `### Changed`, `### Deprecated`,
`### Removed`, `### Fixed`, `### Security`. One line per skill change,
naming the skill and its new version.

## Deprecation checklist

1. User confirms skill + reason + replacement (or none).
2. Description gets `Deprecated: use <replacement> instead.` prefix;
   total stays ≤500 chars.
3. README top note names the replacement.
4. Root README catalog marked; skill pulled from pack tables.
5. Replacement's own boundary re-checked.
6. MAJOR bump + `### Deprecated` CHANGELOG line.
7. Folder stays; deletion is a human decision.

## Validation commands (repo root)

- Library validator: `python tools/validate_skills.py --run-scripts`
  (or with skill names to scope). PASS + 0 errors required; the 90-day
  staleness warning is the sweep signal, not a failure.
- Spec validator, per skill:
  - Windows: `.venv/Scripts/agentskills.exe validate skills/<name>`
  - POSIX: `.venv/bin/agentskills validate skills/<name>`

## Consistency sweep queries

- Boundary mentions: grep `instead` across skills/*/SKILL.md
  descriptions; each named sibling must exist; check reciprocity where
  overlap runs both ways; each named sibling needs a near-miss case in
  the naming skill's evals/triggers.json.
- Install tables: diff each skill README table against
  docs/PER-HARNESS-SETUP.md (master). Fix READMEs toward the master.
- Catalog: skills/ folders vs root README catalog, both directions.
