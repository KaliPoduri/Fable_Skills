# next_session.md

Task: IMPLEMENT PLAN.md v5 — Spark ETL Assistant Suite (3 Copilot skills + etl-knowledge/ KB spec). Plan is FINAL. Obey its implementing-agent block: [CANDIDATE] = verify before use + log; [OPEN] = ask the user, never guess; log deviations in implementation-notes.md ("Spark suite" section).

Status: **M0 kit BUILT (session 1, 2026-07-10).** Milestone order is gated (PLAN §8): M0 (BLOCKING, runs in USER's org Copilot) → M1 Skill C → M2 KB + Skill A → M3 Skill B. Nothing downstream starts until the USER runs M0 in-org and it passes.

What exists now — `m0/` (throwaway kit; delete after gate):
- `M0-CHECKLIST.md` — in-org spike: agent/skills policy (A5), .agents/skills load incl. multi-root secondary root (A6), ask-mode load, file-write+git, session depth (U8) + results template.
- `m0-canary/` — pure-markdown canary skill (validates green via `agentskills validate`). Proofs: trigger → ref-load → file-write → git.
- `FACT-LOCK.md` — billing+HARD budget, Spark minor ver (U1), scheduler (U9), history-server access+retention (U5), config-change scope (A10), policies, KB home, names. U1/U5/A10 = M1 gates.
- `BASELINE.md`, `ADOPTION-ONE-PAGER.md`, `PLAYBOOK-GOVERNANCE.md` — templates.
- Deviation logged: rebuilt canary because `skills/phase0-canary` was deleted (Phase-0 waiver); no-scripts policy → pure markdown.

Verified this session: `agentskills validate m0/m0-canary` → Valid (exit 0); `python tools/validate_skills.py` → 23/23 PASS, m0/ not scanned.

NEXT (blocked on USER): USER runs M0-CHECKLIST in org Copilot, fills FACT-LOCK/BASELINE/ADOPTION/GOVERNANCE. **Do not start M1 authoring until U1, U5, A10 are LOCKED.** Then M1 = author `spark-performance-advisor` per library conventions (template/, AUTHORING-GUIDE, both validators, SOURCES.md; every Spark config verified vs Apache Spark docs for the LOCKED minor version — AQE default-on only ≥3.2).

Conventions: skills in skills/<name>/; no scripts inside Spark skills; names fixed: etl-knowledge-builder, etl-assistant, spark-performance-advisor; quote YAML-risky descriptions.
Key files: PLAN.md, UNKNOWNS.md, m0/, implementation-notes.md, progress.md (Spark section at top), council/LOG.md.
Prior project (23-skill library): archived plan at archive/2026-06-skills-library-plan/; its eval execution still pending — separate track.

### git status --short --branch
```
## master...origin/master
```

Resume from this handoff unless the user's first message says otherwise.
