# progress.md — Fable Skills

## PROJECT 2: Spark ETL Assistant Suite (active)

### Milestones
- 2026-07-10 Planning: PlanGenie full run — 15-question interview, draft plan, 3 council rounds (Claude + Codex; round 3 unanimous: 10/10 majors CLOSED, no new majors), 19 refinements arbitrated (18 accepted, R10 native-context trial rejected). PLAN.md FINAL v5 committed with implementing-agent block. Old library plan archived to archive/2026-06-skills-library-plan/.

### Phase tracker (gates in PLAN.md §8)
| Milestone | Gate | Status |
|---|---|---|
| M0 spike + fact lock (BLOCKING) | all checks pass in org Copilot; fact-lock table filled; adoption owner named; M1 entry = U1/U5/A10 resolved | pending — M0 kit to be built locally, then USER runs in org |
| M1 spark-performance-advisor | slow-job experiment per §6 protocol, threshold recorded BEFORE runs | pending (blocked on M0) |
| M2 KB format + etl-knowledge-builder pilot | owner sample ≥20%/≥10 jobs incl. negative checks; cost extrapolation green-light | pending |
| M3 etl-assistant | ≥10 known incidents, zero high-confidence wrong, traps answered "insufficient evidence" | pending |
| Ops triage | — | deferred by user |

### Architectural decisions (full detail in PLAN.md v5)
- Copilot-only harness (org has no Claude Code); Skill A needs agent mode; skills from .agents/skills/.
- 3 skills join THIS library (names fixed): etl-knowledge-builder, etl-assistant, spark-performance-advisor.
- Sharded etl-knowledge/ KB: thin root index, per-repo indexes, lineage by domain, error-pattern index + dated files; pointers-not-copies; staleness stamps (code-only scope, caveat at point-of-use); dedicated repo preferred.
- Authoritative job seed + build-time grep cross-checks; regen = reviewable diff; content-based redaction; playbook via PR.
- Usage-based Copilot billing (since 2026-06-01): HARD-stop budget covering builds AND eval runs (M0).

### Blockers
- M0 is user-side (org Copilot) — everything downstream waits on its fact-lock results.

---

# PROJECT 1: Fable Skills library (23 skills — done, pilot pending)

## Milestones
- 2026-07-06 Planning: PlanGenie interview (all topics answered), 3 research subagents (Copilot mechanics, 67-skill SDLC inventory, authoring best practices), draft plan, 2 council rounds (Claude + Codex — zero unresolved disputes, 17 refinements accepted), PLAN.md FINAL v3 committed.
- 2026-07-06 Implementation session 1: Phase 0 test kit built (skills/phase0-canary + phase0/PHASE0-CHECKLIST.md — ready for user to run in-org). Phase-0-independent Phase A done: repo scaffold, template/, AUTHORING-GUIDE (incl. provisional eval thresholds), COMPATIBILITY, PER-HARNESS-SETUP, root README catalog, LICENSE/CHANGELOG/VERIFICATION-LOG, tools/validate_skills.py. skills-ref 0.1.1 PROVEN (agentskills CLI validates canary). implementation-notes.md started.

## Phase tracker
| Phase | Gate | Status |
|---|---|---|
| 0 In-org go/no-go (3 flows) | USER runs in org | WAIVED by user 2026-07-06 |
| A Foundation + meta skills | provisional thresholds set first | DONE (packs finalization + effort estimate n/a after waiver) |
| First-5 gate | user reviews generator output | superseded — user review of authored set, at leisure |
| B Tier 1 (21 skills) | — | DONE — authored, source-verified, both validators green |
| Pilot gate | usage + maintenance burden, 2–4 wks | pending |
| C Tier 2 (30 skills) | conditional on pilot | pending |
| Tier 3 (14) | named backlog, authored on demand | pending |

## Architectural decisions (see PLAN.md for full detail)
- Agent Skills open standard (SKILL.md folders) — one artifact for Copilot/Claude/Cursor/Codex/Antigravity.
- Library source: skills/<name>/; consumer default .agents/skills/; manual copy until gh skill proven.
- Install packs 4–6, ≤15 skills/project (trigger-budget mitigation).
- Eval: Claude Code headless = automated proxy; manual VS Code Copilot Chat smoke test = authoritative.
- Governance: user = script reviewer + source re-verifier + VERIFICATION-LOG.md owner (launch).

## Blockers
- (none) Phase 0 waived by user; note: in-org triggering remains unproven until first team use.

## Repo
- 2026-07-06 pushed to https://github.com/KaliPoduri/Fable_Skills (master). Visibility: private intended — user to confirm in browser (gh CLI not authenticated locally).

## Testing results
- 2026-07-06 `python tools/validate_skills.py --run-scripts` → PASS (phase0-canary, 0 errors; includes Windows script --self-test).
- 2026-07-06 `agentskills validate skills/phase0-canary` (skills-ref 0.1.1 in .venv) → "Valid skill".
- 2026-07-06 canary.py on build machine: Python 3.13.7; python-pptx AND python-docx importable (build machine only — org check is Phase 0).
- 2026-07-06 Tier 1 + meta (23 skills): `python tools/validate_skills.py` → 23/23 PASS, 0 errors; `agentskills validate` → 0 failures across all 23 (after quoting 3 YAML-unsafe descriptions; validator hardened). Consistency reviewer: 6 findings, all fixed. Trigger/output evals authored per skill but NOT yet executed (proxy runner still to be stood up).
