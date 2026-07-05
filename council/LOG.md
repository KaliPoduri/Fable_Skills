# Council LOG

## Round 1 (packet: round-1-packet.md)
Seats: Claude (fresh Fable subagent, web-verified fact-hunt) + Codex (background task task-mr87jiol-pgkp65).

Merged into 9 refinements; user verdicts:
1. Phase 0 in-org smoke-test go/no-go gate — ACCEPTED
2. Install packs (4–6, ≤15/project) + description discipline (≤500 chars, triggers in first 250, CI) — ACCEPTED
3. Build gates: first-5 generator review + post-Tier-1 team pilot deciding Tiers 2–3 — ACCEPTED (both gates)
4. Claim hygiene: GA→"supported since Dec 2025/preview"; R2→preview-surface churn + version pinning; Cursor/Antigravity→[CANDIDATE] community-sourced; COMPATIBILITY.md matrix — ACCEPTED
5. Distribution: skills/ source of truth (gh skill install auto-discovery VERIFIED) + consumer install docs + git-tag releases — ACCEPTED
6. Security: anchor swap (Top10:2025 + ASVS 5.0 + CWE Top 25; 2017 Code Review Guide demoted) + library security gate — ACCEPTED (both)
7. Eval runner: Claude Code headless / Copilot CLI proxy + thresholds + manual Copilot smoke test; keep ~20+3 — ACCEPTED
8. Coverage gaps: add 5 skills (ux-design-reviewer, compliance-privacy-reviewer, data-governance-advisor, ai-evals-designer, legacy-migration-planner) → 55 total — ACCEPTED
9. Small fixes a–h (string metadata, voice rule, dependency-auditor rescope, python vs python3 + Windows CI, constraints boilerplate→1 line + shared section, SOURCES manifest, internal-use LICENSE, maintainer defines who/where of re-verification) — ACCEPTED (all)

Rejected: none. Disputed: none carried by user; cross-check items for round 2:
- To Codex: does the updated plan resolve M1 (layout/distribution), M3 (frontmatter portability — resolved via per-surface matrix), M4 (dilution), M5 (exhaustiveness), M6 (feasibility gates), M7 (offline vs staleness), M8 (security governance)?
- To Claude seat: do the applied fixes resolve its majors 1–7?

PLAN.md v2 written. Round 2 = cross-examination on the updated plan.
