# next_session.md

Task: IMPLEMENT PLAN.md (final v3) — Fable Skills, 67 skills, Agent Skills format, Copilot-first.
Status: Phase A ~70% done. Phase 0 kit READY — USER runs phase0/PHASE0-CHECKLIST.md in-org (canary at skills/phase0-canary, throwaway; delete both after gate).
Done this session: scaffold (docs/, template/, tools/), AUTHORING-GUIDE (provisional eval thresholds §10), COMPATIBILITY, PER-HARNESS-SETUP, root README catalog+draft packs, LICENSE/CHANGELOG/VERIFICATION-LOG/.gitignore, tools/validate_skills.py (library policy) — all validated.
Verified: skills-ref 0.1.1 PROVEN (.venv, `agentskills validate` → Valid skill); validator PASS incl. Windows --self-test; build machine Python 3.13.7, pptx/docx importable.
Next steps (Phase A remainder):
1. Build meta skills: skill-creator (uses template/, enforces AUTHORING-GUIDE) + library-maintainer.
2. Per-skill effort estimate to reality-test Phase B (PLAN §5).
3. Finalize pack composition with USER (draft in README, marked [OPEN]).
4. When user brings Phase 0 results → log in implementation-notes + VERIFICATION-LOG, flip PER-HARNESS-SETUP install line, decide gh-vs-manual + pptx/docx, delete phase0/ + canary.
Then FIRST-5 GATE (user review vs provisional thresholds) before mass generation.
Rules: implementation-notes.md has Decisions/Deviations — keep logging; verify [CANDIDATE]+[CONFIRMED-tool-claims] before use; raise [OPEN] with user.
Convention: work on master; agentskills validates spec, tools/validate_skills.py validates library policy; template/ excluded from CI.
