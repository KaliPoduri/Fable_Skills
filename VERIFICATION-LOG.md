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
| 2026-07-06 | skills-ref on PyPI (spec reference implementation) | OK — 0.1.1 installed; `agentskills validate` proven against all authored skills | implementation session | |
| 2026-07-06 | agentskills.io/specification | OK (re-fetch) | authoring subagents | |
| 2026-07-06 | OpenAPI Specification | OK — v3.2.0 current (published 2025-09-19), spec.openapis.org | authoring subagents | |
| 2026-07-06 | RFC 9457 (+ RFC 9110, RFC 5789) | OK — rfc-editor.org | authoring subagents | 9457 obsoletes 7807 |
| 2026-07-06 | arc42 template | OK — v9.0 (July 2025), arc42.org | authoring subagents | |
| 2026-07-06 | MADR | OK — 4.0.0 (2024-09-17), adr.github.io/madr | authoring subagents | |
| 2026-07-06 | Mermaid C4 syntax | OK but EXPERIMENTAL per mermaid.js.org — skills carry flowchart fallback | authoring subagents | |
| 2026-07-06 | Conventional Commits | OK — v1.0.0, conventionalcommits.org | authoring subagents | was on unverified list |
| 2026-07-06 | SemVer | OK — 2.0.0, semver.org | authoring subagents | was on unverified list |
| 2026-07-06 | Keep a Changelog | OK — 1.1.0, keepachangelog.com | authoring subagents | was on unverified list |
| 2026-07-06 | CWE Top 25 | OK — 2025 edition (released 2025-12-11 with CISA), cwe.mitre.org | authoring subagents | was on unverified list |
| 2026-07-06 | ISTQB CTFL syllabus | OK — v4.0.1 (2024-09-15; copyright-only update of v4.0) | authoring subagents | istqb.org 403s direct fetch; verified via indexed URL |
| 2026-07-06 | OWASP Top 10:2025 + ASVS 5.0.0 (re-check) | OK — owasp.org/Top10/2025; ASVS tag v5.0.0 | authoring subagents | third verification |
| 2026-07-06 | DORA (dora.dev) | OK — 34 capabilities; metrics now a FIVE-metric model (four keys = historical name) | authoring subagents | was on unverified list |
| 2026-07-06 | Scrum Guide (Nov 2020), INVEST (Wake 2003), Gherkin reference | OK — scrumguides.org, xp123.com, cucumber.io | authoring subagents | |
| 2026-07-06 | Google eng-practices | OK — living doc, google.github.io/eng-practices | authoring subagents | |
| 2026-07-06 | Book editions: Beck TDD (2002, 978-0321146533), Fowler Refactoring 2nd ed (2018, 978-0134757599), Agans 9 Rules, Zeller Why Programs Fail 2nd ed (2009) | OK — publisher pages | authoring subagents | was on unverified list |
| 2026-07-06 | Google SRE Book ch.15 + SRE Workbook ch.10 (postmortems) | OK — sre.google | authoring subagents | |

Still-unverified standards (verify during authoring of the affected skill —
PLAN.md §7): ISO 25010:2023, PMBOK 7, OpenSLO (all Tier 2/3 skills).
