# implementation-notes.md — Fable Skills

Log kept per PLAN.md implementing-agent instructions. Decisions as made; every
deviation under "Deviations" with a one-line reason.

## Decisions

- 2026-07-06 Work continues on `master` — matches repo convention (all planning
  commits are on master; solo-user private repo). No feature branch created.
- 2026-07-06 Phase 0 not yet run (user-only, in-org). Per user direction this
  session: build the Phase 0 test kit AND start Phase-0-independent Phase A
  work. Everything depending on Phase 0 results stays open and is marked
  "pending Phase 0" in the affected docs (gh skill vs manual-only install,
  python-pptx/docx, org Python version).
- 2026-07-06 Phase 0 kit split: checklist in `phase0/` (throwaway, deleted
  after the gate); the canary skill itself at `skills/phase0-canary/` because
  flow 2 (`gh skill install`) only auto-discovers `skills/*/SKILL.md` — it
  could not be tested from any other path. Canary is marked THROWAWAY in its
  own files and is deleted together with `phase0/` once the gate closes.
- 2026-07-06 CI validator placed at `tools/validate_skills.py`. PLAN.md tree is
  silent on the CI script's location; `tools/` is the conservative choice (does
  not pollute `skills/` or `docs/`).
- 2026-07-06 skills-ref installed into `.venv/` (gitignored) — build-machine
  only; consumers never need it.

## Verifications

- 2026-07-06 `skills-ref` EXISTS on PyPI: versions 0.1.0, 0.1.1
  (`pip index versions skills-ref`). PLAN §4 [CONFIRMED] upheld.
- 2026-07-06 `skills-ref` 0.1.1 PROVEN functionally: installed into `.venv`,
  ships an `agentskills` CLI (author: Anthropic / agentskills.io);
  `agentskills validate skills/phase0-canary` → "Valid skill". Division of
  labor: `agentskills` = spec validator; `tools/validate_skills.py` = library
  policy (500-char description, README/SOURCES/evals presence, body lines,
  script --self-test). CI = run both. Template folder correctly fails
  spec validation (placeholder name) — template/ is excluded from CI scans.
- 2026-07-06 `tools/validate_skills.py --run-scripts` PASS on phase0-canary,
  including Windows script invocation (canary.py --self-test, exit 0).
- 2026-07-06 Build machine: Python 3.13.7, pip 26.0.1 (command output this
  session).

## Deviations

- (none yet)

## Open items raised with user

- 2026-07-06 Phase 0 status asked at session start; user chose "build kit +
  start Phase A prep". Phase 0 remains a hard gate before Phase B.
