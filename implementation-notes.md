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

- 2026-07-06 Tier 1 (21) + meta (2) authored by 10 parallel subagents; all
  sources web-verified at authoring time (results in VERIFICATION-LOG.md).
  Session-limit interruption mid-run: 4 agents resumed via their
  transcripts; resumes completed partial folders without re-verification.
- 2026-07-06 BUG FOUND by spec validator: 3 skills (cicd-pipeline-designer,
  postmortem-writer, release-manager) had unquoted `description:` values
  containing ": " — valid to our minimal parser, invalid YAML to real
  parsers. Fixed by quoting; validator hardened with a SPEC-YAML check so
  the library validator now catches this class itself.
- 2026-07-06 Notable verification findings: DORA is now a five-metric
  model (four keys historical); Mermaid C4 syntax is experimental (skills
  carry a flowchart fallback); istqb.org 403s bot fetches (noted in that
  skill's SOURCES.md).
- 2026-07-06 Consistency reviewer pass (read-only subagent) over all 23:
  library-wide PASS on constraints line, description formula, namespaces
  (REV-/SEC-/PERF-/SQL-/TM-), eval JSON, zero cross-skill trigger
  collisions. 6 findings, all fixed same session: 3 missing sibling
  call-outs (threat-modeler→api-designer, sql-optimizer→code-reviewer,
  adr-writer↔c4-diagrammer), literal <skill-name> placeholders in 3
  architecture READMEs, 3 descriptions with the boundary landing past char
  250 (trimmed), adr-writer sentence order. Post-fix: boundary ends ≤248
  on all edited skills; both validators green (23/23, 0 spec failures).

## Deviations

- 2026-07-06 [USER-DIRECTED] Phase 0 gate WAIVED — user declined to run the
  in-org go/no-go; kit (phase0/ + skills/phase0-canary) deleted. Risk
  accepted: in-org triggering/script execution remains unproven until the
  team first uses a skill (was risk R2's mitigation).
- 2026-07-06 [USER-DIRECTED] Distribution simplified to MANUAL COPY ONLY —
  all `gh skill install` documentation removed (README, PER-HARNESS-SETUP,
  COMPATIBILITY). Version pinning falls back to git tags + CHANGELOG only.
- 2026-07-06 [USER-DIRECTED] "Create the skills" ⇒ authoring full Tier 1
  (21) + meta (2) in one pass; the first-5 gate becomes a post-hoc user
  review of the authored set rather than a pre-production checkpoint.
- 2026-07-06 Consequence of no Phase 0: org Python version and pptx/docx
  permissibility unknown ⇒ Tier 1 skills ship with NO scripts at all
  (Markdown/HTML output only, which PLAN §2.3 already made primary).

## Open items raised with user

- 2026-07-06 Phase 0 status asked at session start; user chose "build kit +
  start Phase A prep". Phase 0 remains a hard gate before Phase B.
