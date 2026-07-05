# next_session.md

Task: IMPLEMENT PLAN.md (final v3) — Fable Skills library, 67 skills (65 lifecycle + 2 meta), Agent Skills/SKILL.md format, Copilot-first.
Status: Planning complete (PlanGenie + 2 council rounds, committed). Implementation NOT started.
Current phase: Phase 0 — USER must run in-org go/no-go (PLAN.md §5): (1) manual-copy a throwaway skill → triggers in org VS Code Copilot Chat? (2) gh skill install works (gh ≥2.90)? (3) Python script runs; pptx/docx libs allowed?
If Phase 0 passed → Phase A: scaffold repo per PLAN.md §2.2 tree; write AUTHORING-GUIDE, PER-HARNESS-SETUP, COMPATIBILITY matrix, template/, CI validator, eval harness; set provisional eval thresholds; finalize packs with user; build skill-creator + library-maintainer. Then FIRST-5 GATE (user review) before mass generation.
Key decisions (details in PLAN.md):
- skills/<name>/ source tree; consumers install to .agents/skills/ (manual copy default until gh skill proven).
- Description ≤500 chars, triggers+negative boundary in first 250; body <500 lines; imperative body / third-person description.
- Every skill: README (per-harness usage), references/SOURCES.md (version+URL+last-verified), evals/, one-line constraints; scripts stdlib-only, no network, Windows-tested.
- Security gate: no allowed-tools pre-approval; user reviews every script-bearing skill.
- Privacy: build/evals on this personal machine, library content only; org side offline.
Rules for implementer: keep implementation-notes.md (decisions + Deviations); verify [CANDIDATE] before use; raise [OPEN] with user, never guess; [CONFIRMED] (user approved) tool/version claims still need verification.
Known issues: [OPEN] list in PLAN.md §7; repo not yet pushed to GitHub (private repo pending).
Handoff artifacts: PLAN.md (authoritative), UNKNOWNS.md, progress.md, council/LOG.md.
