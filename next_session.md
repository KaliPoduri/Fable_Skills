# next_session.md

Task: PlanGenie run for Spark ETL Assistant Suite — COMPLETE. PLAN.md v5 is FINAL (ends with implementing-agent instructions block). UNKNOWNS.md final; full council record in council/ (3 rounds, unanimous closure, 18/19 refinements accepted; R10 native-context trial rejected by user).
Status: All committed on master. Nothing in flight.
The plan delivers: 3 Copilot Agent Skills (etl-knowledge-builder, etl-assistant, spark-performance-advisor) + sharded etl-knowledge/ KB, for the user's org (GitHub Copilot VS Code only — no Claude Code there). Milestones M0 (feasibility spike + fact lock, blocking) → M1 (Skill C) → M2 (KB + Skill A pilot) → M3 (Skill B).
Next steps (user-driven):
1. Implementation starts with M0 — but M0 runs in the ORG's Copilot (agent mode, .agents/skills load test, fact-lock table, baseline capture) — mostly user-side actions, not this machine.
2. When implementing skills here: follow the Fable Skills library conventions (AUTHORING-GUIDE, validators: tools/validate_skills.py + .venv agentskills CLI); all [CANDIDATE] Spark configs verified against Apache Spark docs for the org's exact minor version (locked at M0).
3. Older context: skills-library plan archived at archive/2026-06-skills-library-plan/ (23 skills authored/validated/pushed; eval execution still pending — separate track).
Conventions: master branch; PlanGenie tags stay in PLAN.md ([USER]/[CONFIRMED]/[CANDIDATE]/[OPEN]); [OPEN] items must be raised with the user, never guessed.
