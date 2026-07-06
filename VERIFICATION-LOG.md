# VERIFICATION-LOG.md

Governance record of source re-verification (PLAN.md §5; owner: Kali
Poduri). One row per verification EVENT — the same source reappears each
time it is re-checked. Cadence: [OPEN] quarterly proposed, not yet decided.

| Date | Source / claim | Result | Verified by | Notes |
|---|---|---|---|---|
| 2026-07-06 | agentskills.io/specification (SKILL.md format, frontmatter limits) | OK | planning session | name ≤64 lowercase-hyphen; description ≤1024 (Codex counts bytes); unknown fields ignored |
| 2026-07-06 | github.blog changelog 2025-12-18 + VS Code docs (Copilot Agent Skills support) | OK | planning session | VS Code stable rollout ~Jan 2026, exact date unpinned [OPEN] |
| 2026-07-06 | gh manual — `gh skill install` (preview, gh ≥2.90.0; auto-discovers skills/*/SKILL.md; installs to .agents/skills/) | OK | planning session | one council seat's gh 2.80.0 lacked the command |
| 2026-07-06 | cursor.com/docs/skills (.cursor/skills/ primary, .claude/skills/ legacy-compat) | OK | planning session | upgraded Cursor to officially-documented in round 2 |
| 2026-07-06 | OWASP Top 10:2025 — owasp.org/Top10/2025 | OK (twice) | planning session | |
| 2026-07-06 | OWASP ASVS 5.0.0 | OK (twice) | planning session | |
| 2026-07-06 | OWASP LLM Top 10 2025 | OK (twice) | planning session | |
| 2026-07-06 | ISTQB v4.0.1 = copyright-only update of v4.0 | OK | planning session | |
| 2026-07-06 | skills-ref on PyPI (spec reference implementation) | OK — versions 0.1.0, 0.1.1 exist (`pip index versions skills-ref`) | implementation session | functional proof pending this session |

Still-unverified standards (verify during authoring of the affected skill —
PLAN.md §7): Conventional Commits 1.0.0, SemVer 2.0.0, Keep a Changelog
1.1.0, ISO 25010:2023, PMBOK 7, OpenSLO, CWE Top 25 2025 edition, DORA
capabilities state, book editions.
