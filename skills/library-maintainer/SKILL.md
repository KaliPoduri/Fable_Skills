---
name: library-maintainer
description: Maintains existing skills in the Fable Skills library. Use this skill when asked to re-verify sources, check for stale skills, bump a skill version, or deprecate a skill. Do not use for creating a new skill; use skill-creator instead. Covers staleness sweeps, SOURCES.md re-verification with VERIFICATION-LOG.md entries, SemVer bumps with CHANGELOG entries, deprecation flow, full-library validation, and consistency checks. Build-machine meta skill for the library repo itself.
metadata:
  version: "1.0.0"
  last-verified: "2026-07-06"
---

# Library Maintainer

Keep the released Fable Skills library correct, current, and consistent.
Work inside the library repo on the build machine. Every maintenance run
is one or more of six jobs: staleness sweep, source re-verification,
version bump, deprecation, full-library validation, consistency check.
Ask which jobs are wanted if the request is vague; a routine quarterly
pass runs all six. Creating a brand-new skill is never your job — hand
that to skill-creator.

## Constraints

Assume no external internet access, no paid tools, and English output.
Never send project code or data to external services.
Exception: this meta skill runs on the library build machine, where
internet access IS available and REQUIRED for source re-verification
(SOURCES.md rows are re-checked on the web, never from model memory).
Never delete a skill folder; deprecation marks and redirects, removal is
a human decision.
Do not weaken any AUTHORING-GUIDE rule while editing a skill; if a rule
itself seems wrong, flag it to the user instead of silently deviating.
Never add `allowed-tools` or shell pre-approval while touching a skill.

## Workflow

Read docs/AUTHORING-GUIDE.md before editing any skill — edits must leave
each skill compliant with it.

### Job 1 — Staleness sweep

1. Run `python tools/validate_skills.py` from the repo root. It warns per
   skill when `metadata.last-verified` is older than 90 days.
2. Cross-check by listing dates directly (grep `last-verified` across
   skills/*/SKILL.md) so warnings are not the only signal.
3. Report the stale list, oldest first, and propose re-verification
   (Job 2) for each. Do not change any date without doing Job 2.

### Job 2 — Source re-verification

For each skill in scope:

1. Open references/SOURCES.md. For every row, fetch the official URL on
   the web NOW and confirm: source still exists, version still current.
2. Outcomes per row:
   - UNCHANGED — update the row's last-verified date to today.
   - CHANGED (new version/moved URL) — update the row, re-distill the
     affected references/*.md content, and queue a version bump (Job 3:
     minor for content updates, major if the skill's guidance changes
     meaning).
   - GONE — mark the row `[Unverified — source unreachable <date>]`,
     keep the offline fallback authoritative, flag to the user.
3. Update the skill's `metadata.last-verified` to today ONLY when every
   row was actually re-checked.
4. Append one row to VERIFICATION-LOG.md PER verification event, matching
   its table: `| Date | Source / claim | Result | Verified by | Notes |`.
   The same source reappears each time it is re-checked; never rewrite
   old rows.

### Job 3 — Version bump (SemVer on metadata.version)

1. Decide the bump from the change, per SemVer 2.0.0:
   - PATCH — typo, wording, date refresh, eval-only additions.
   - MINOR — new content, new reference file, expanded workflow,
     backward-compatible description tweaks.
   - MAJOR — changed scope/boundary, renamed outputs, altered output
     template, or any change that breaks how consumers use the skill.
2. Edit `metadata.version` (keep it a quoted string).
3. Add a CHANGELOG.md line under `## [Unreleased]` in the matching Keep a
   Changelog category (`### Added` / `### Changed` / `### Deprecated` /
   `### Fixed`), naming the skill and new version.
4. Re-run both validators on the touched skill (see Job 5 commands).

### Job 4 — Deprecation flow

1. Confirm with the user: which skill, why, and what replaces it.
2. Prepend the description with `Deprecated: use <replacement> instead.`
   while keeping the rest of the description intact and ≤500 chars total.
3. Add a deprecation note at the top of the skill's README.md naming the
   replacement (or "no replacement").
4. Update the catalog in the repo-root README.md: mark the skill
   deprecated where it is listed; remove it from any pack table.
5. If a replacement exists, check the replacement's description boundary
   still makes sense (it may have named the deprecated skill).
6. MAJOR version bump + CHANGELOG entry under `### Deprecated` (Job 3).
7. Do not delete the folder; removal is a later human decision.

### Job 5 — Full-library validation

From the repo root:

1. `python tools/validate_skills.py --run-scripts` → every skill must
   print PASS; report each ERROR verbatim with its skill name.
2. Agent Skills CLI per skill folder:
   - Windows: `.venv/Scripts/agentskills.exe validate skills/<name>`
   - POSIX: `.venv/bin/agentskills validate skills/<name>`
3. Fix failures per the AUTHORING-GUIDE rule the message cites; rerun
   until clean. Two failed fix attempts on the same error → stop and ask.

### Job 6 — Consistency checks

1. Sibling boundaries both ways: for every `use <sibling> instead` in a
   description, confirm the sibling exists and (where the overlap is
   two-directional) names this skill back; confirm each named sibling has
   a near-miss case in the naming skill's evals/triggers.json.
2. Install-table drift: compare every skill README's install table
   against docs/PER-HARNESS-SETUP.md (that file is the master). Fix the
   README, never the master, unless the user says the master moved.
3. Catalog drift: every folder under skills/ appears in the repo-root
   README catalog and vice versa (template/ and throwaways excluded).
4. Metadata hygiene: version and last-verified present and quoted in
   every skill (the validator errors on these — Job 5 covers the check).

## Output template

End every maintenance run with this report:

```
## Library maintenance report — <date>

- Jobs run: <sweep | re-verify | bump | deprecate | validate | consistency>
- Skills touched: <name (old-version -> new-version)> per skill, or none
- Staleness: <N> stale skill(s): <names + last-verified dates> | none
- Re-verification: <N> rows checked; <U> unchanged / <C> changed / <G> gone
- VERIFICATION-LOG.md: <N> row(s) appended
- CHANGELOG.md: <entries added> | none
- Validation: validate_skills.py <PASS all / failures>; agentskills <valid / failures>
- Consistency: <findings> | clean
- Follow-ups for a human: <list> | none
```

## References (load on demand)

- `references/SOURCES.md` — source manifest for this skill (always
  present).
- `references/maintenance-runbook.md` — per-job runbook with decision
  tables (SemVer triage, re-verification outcomes, deprecation steps);
  load at the start of any maintenance run. It summarizes repo docs —
  read the live docs/AUTHORING-GUIDE.md as the authority.
- docs/AUTHORING-GUIDE.md (repo) — read before editing any skill.
- VERIFICATION-LOG.md (repo) — read before appending, to match the table
  format and see what is still-unverified.
- docs/PER-HARNESS-SETUP.md (repo) — load for Job 6 install-table checks.

## Checklist

- [ ] Jobs in scope agreed with the user (or full quarterly pass).
- [ ] No new skill created (that is skill-creator's job — redirect if
      asked).
- [ ] Every changed last-verified date backed by an actual web re-check
      this session.
- [ ] One VERIFICATION-LOG.md row appended per verification event.
- [ ] Every content change carries a SemVer bump + CHANGELOG entry.
- [ ] Deprecations: description marker, README note, catalog update,
      MAJOR bump — folder NOT deleted.
- [ ] Both validators pass on every touched skill (full library if Job 5).
- [ ] Report emitted in the Output template format, follow-ups listed.
