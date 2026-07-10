# next_session.md

Task: IMPLEMENT PLAN.md v5 — Spark ETL Assistant Suite (3 Copilot skills + etl-knowledge/ KB spec). Plan is FINAL (PlanGenie + 3 council rounds, unanimous closure). Read PLAN.md in full first; obey its implementing-agent block: [CANDIDATE] = verify before use and log it; [OPEN] = ask the user, never guess; log every deviation in implementation-notes.md ("Spark suite" section, Deviations heading).
Status: Implementation NOT started. Milestone order is gated (PLAN §8): M0 (BLOCKING, runs in the user's org Copilot) → M1 Skill C → M2 KB + Skill A pilot → M3 Skill B.
Session 1 goal — build the M0 kit locally so the user can run the spike in-org:
1. M0 checklist: agent-skills policy, .agents/skills load (incl. multi-root secondary root), ask-mode load test, file-write + git test, session-depth observation. Adapt skills/phase0-canary (existing test skill) for these checks.
2. Fact-lock table template: billing plan + HARD-stop budget (must cover eval runs too), exact Apache Spark minor version, scheduler type, org policies, history-server access + event-log retention, dev config-change scope.
3. Baseline sheet (3–5 recent incidents' time-to-RCA) + adoption one-pager skeleton + playbook governance template (reviewer role, approval criteria, disputed-cause handling, security owner).
4. USER runs M0 in org; record results in the fact-lock table; M1 entry criteria = U1, U5, A10 resolved.
Only after M0: author spark-performance-advisor (M1) per library conventions — template/, docs/AUTHORING-GUIDE.md, both validators green (tools/validate_skills.py + .venv agentskills CLI), SOURCES.md; every Spark config verified against Apache Spark docs for the LOCKED minor version (AQE default-on only since 3.2).
Conventions: skills in skills/<name>/; library policy = no scripts inside skills; names fixed: etl-knowledge-builder, etl-assistant, spark-performance-advisor; quote YAML-risky descriptions.
Key files: PLAN.md, UNKNOWNS.md, council/LOG.md, progress.md (Spark suite section at top), implementation-notes.md.
Prior project (23-skill library): plan archived at archive/2026-06-skills-library-plan/; its eval execution is still pending — separate track, don't mix.
