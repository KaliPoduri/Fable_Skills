# implementation-notes.md — Fable Skills

Log kept per PLAN.md implementing-agent instructions. Decisions as made; every
deviation under "Deviations" with a one-line reason.

---

# Spark suite (PROJECT 2)

## Decisions

- 2026-07-10 M0 kit built under a throwaway `m0/` directory (NOT `skills/`) —
  keeps the 23 real library skills and both validators untouched; cleanup is
  `rm -r m0/` after the M0 gate. Kit = README, M0-CHECKLIST, m0-canary skill,
  FACT-LOCK, BASELINE, ADOPTION-ONE-PAGER, PLAYBOOK-GOVERNANCE (PLAN §8 M0).
- 2026-07-10 Canary named `m0-canary`, pure markdown (no script) — Spark-suite
  library policy is no-scripts, and M0 needs no Python. Proofs: trigger →
  reference-load → file-write → git; ask mode expected to block write/git.
- 2026-07-10 Continuing on `master` (standing repo decision, solo private repo);
  M0 kit is documentation/templates only.
- 2026-07-10 [OPEN] items (U1, U5, U9, A5-A11, KB home, names, owners) left as
  blanks in the templates for the USER to resolve during the in-org spike —
  not guessed. M1 entry gates (U1/U5/A10) flagged in FACT-LOCK.md.

## Verifications

- 2026-07-10 `agentskills validate m0/m0-canary` → "Valid skill" (exit 0) —
  the canary will actually load in the in-org test.
- 2026-07-10 `python tools/validate_skills.py` → 23/23 PASS, 0 errors; grep
  confirms `m0/` is NOT scanned — the throwaway kit stays out of CI.
- 2026-07-10 Retrieved the deleted `phase0-canary` from git `66fc68f` as the
  reference pattern (it was removed in `b630598` when Phase 0 was waived).

## Deviations

- 2026-07-10 [DEVIATION] Handoff said "adapt skills/phase0-canary"; that skill
  no longer exists (deleted with the Phase-0 waiver, commit b630598). Rebuilt
  as a new pure-markdown `m0-canary` with file-write + git proofs. Reason: M0
  verifies skill loading + agent-mode file/git + ask-mode + session depth, not
  script execution or `gh skill install` (distribution is manual-copy-only,
  already locked). Old canary's gh-install/Python-script proofs are obsolete.

---

# Skills library (PROJECT 1)

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
