# next_session.md

Task: IMPLEMENT PLAN.md v5 — Spark ETL Assistant Suite (3 Copilot skills + etl-knowledge/ KB). Obey PLAN's implementing-agent block: [CANDIDATE] verify+log; [OPEN] ask, never guess; log deviations in implementation-notes.md ("Spark suite" section).

Status: **M0 kit BUILT (session 1, 2026-07-10); committed, unpushed.** Gate order (PLAN §8): M0 (BLOCKING, runs in USER's org Copilot) → M1 Skill C → M2 KB+Skill A → M3 Skill B. Everything downstream is blocked on the USER running M0 in-org.

Built — `m0/` (throwaway; delete after gate): `M0-CHECKLIST.md` (spike: policy A5, .agents/skills load incl. multi-root A6, ask-mode, file-write+git, session depth U8 + results template) · `m0-canary/` (pure-markdown canary, validates green) · `FACT-LOCK.md` (billing+HARD budget, Spark minor ver U1, scheduler U9, history-server access+retention U5, config-change scope A10 — U1/U5/A10 = M1 gates) · `BASELINE.md` · `ADOPTION-ONE-PAGER.md` · `PLAYBOOK-GOVERNANCE.md`. Deviation logged: canary rebuilt (phase0-canary was deleted).

Verified: `agentskills validate m0/m0-canary` → Valid; `validate_skills.py` → 23/23 PASS, m0/ not scanned.

NEXT (blocked on USER): USER runs `m0/M0-CHECKLIST.md` in org Copilot, fills the four sheets. **Do not start M1 until U1, U5, A10 are LOCKED in FACT-LOCK.md.** Then M1 = author `spark-performance-advisor` per library conventions (template/, AUTHORING-GUIDE, both validators, SOURCES.md); every Spark config verified vs Apache Spark docs for the LOCKED minor version (AQE default-on only ≥3.2).

Conventions: skills in skills/<name>/; no scripts in Spark skills; names fixed (etl-knowledge-builder, etl-assistant, spark-performance-advisor); quote YAML-risky descriptions.
Key files: PLAN.md, UNKNOWNS.md, m0/, implementation-notes.md, progress.md, council/LOG.md. Prior 23-skill library: archived at archive/2026-06-skills-library-plan/ (eval execution still pending — separate track).

### git
```
master, ahead of origin — unpushed (gh not authenticated locally; USER pushes)
```

Resume from this handoff unless the user's first message says otherwise.
