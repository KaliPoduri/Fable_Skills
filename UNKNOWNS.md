# UNKNOWNS.md — Four-Quadrant Register

## Known knowns
- [USER] The project: a complete, exhaustive set of AI-agent skills covering software engineering artifacts (PPTs, design docs, PRDs, features, stories) and roles (developer, code reviewer, OWASP security scanner, code optimizer, SQL optimizer, design architect, and more).
- [USER] The named examples are a starting point; research determines the exhaustive inventory needed to complete a software engineering project end to end, and skill files are built for the full researched list.
- [USER] Skills must encode current, globally-followed best practices and standards.
- [USER] Primary target harness: GitHub Copilot; specifically VS Code Copilot Chat is the surface the user uses.
- [CONFIRMED] (user approved) Skills should be harness/platform-agnostic in design, Copilot priority.
- [USER] Must include a "skill creator" skill that converts user requirements into a new skill in this library's format.
- [CONFIRMED] (user approved) Skill depth: concise core instructions + reference files (checklists, templates, examples) loaded on demand.
- [CONFIRMED] (user approved) Skills include executable helper scripts where needed (e.g., PPTX generation); Python assumed available.
- [CONFIRMED] (user approved) Technology-agnostic guidance with language-specific notes where it matters.
- [USER] Audience: a team (not just the user; not public).
- [USER] Success = skills trigger correctly in VS Code Copilot + output quality beats raw Copilot + team adoption + full lifecycle coverage.
- [CONFIRMED] (user approved) Process skills assume Scrum-based Agile, noting Kanban variations.
- [CONFIRMED] (user approved) Staleness handled via a library-maintainer/refresh skill + documented review cadence.
- [USER] GitHub repo will be private.
- [CONFIRMED] (user approved) Each skill cites authoritative sources + last-verified date.
- [CONFIRMED] (user approved) Hard constraint: skills must never instruct the agent to browse/download from/send data to the external internet (org policy); no paid tools/services beyond Copilot; respect company data privacy; English only. Refresh-with-web-research runs outside the org environment.
- [CONFIRMED] (user approved) F:\AI_Projects\Fable_Skills itself is the single git repo, pushed to GitHub; each skill is a plain subfolder.
- [CONFIRMED] (user approved) Every skill folder gets its own README.md with detailed setup + usage instructions per harness (GitHub Copilot in VS Code, Cursor, Antigravity, Claude Code, and similar).
- [USER] User experience: "I code a little"; somewhat familiar with skill authoring.
- [CONFIRMED] (verified via web search, research subagent, July 2026) GitHub Copilot supports Agent Skills (SKILL.md directories, agentskills.io open standard) — GA since Dec 2025/Jan 2026 across VS Code, Copilot CLI, Copilot coding agent, Copilot code review; auto-detects .github/skills/, .claude/skills/, .agents/skills/. Frontmatter: name (≤64 chars, lowercase-hyphen, matches dir name), description (≤1024 chars); body best practice <500 lines with references/ one level deep. Distribution via `gh skill install <owner>/<repo>` (GitHub CLI ≥2.90.0, public preview Apr 2026).
- [CONFIRMED] (verified via web search, research subagent) Custom chat modes (.chatmode.md) are deprecated → renamed to custom agents (.agent.md). Prompt files are IDE-only. Skills are the only mechanism spanning all Copilot agent surfaces.

## Known unknowns
- RESOLVED: skill inventory researched — 50 skills (48 lifecycle + 2 meta), tiered; user approved building all in tier order.
- [CONFIRMED] (user approved) Teammates share the user's setup (VS Code + Copilot + skills + Python). Still [OPEN]: user to smoke-test that Agent Skills actually load in the org's VS Code before Phase B completes.
- [CONFIRMED] (user approved) AI coding agents execute the build phase by phase.
- [OPEN] Whether Copilot CLI honors ~/.claude/skills/ (documented for VS Code only) — low impact.
- [OPEN] GA-vs-preview status of Agent Skills in Visual Studio/JetBrains (user doesn't use them; low impact).
- [OPEN] Review cadence length (quarterly proposed, not yet confirmed).
- [OPEN] python-pptx/python-docx permitted offline in org — folded into Phase 0 gate.
- RESOLVED (round 1): License = internal-use notice, non-blocking.
- RESOLVED (round 1): subsets question → install packs (4–6, ≤15/project) are first-class.
- RESOLVED (round 1): gh skill install auto-discovers skills/*/SKILL.md — verified via gh manual by council Claude seat.
- [OPEN] Copilot-side skill listing/count limits (none documented).
- [OPEN] Cursor compat-scan + Antigravity paths community-sourced only — labeled [CANDIDATE] in COMPATIBILITY.md.
- [OPEN] Whether Copilot cloud agent honors user-invocable/argument-hint (VS Code yes; cloud-agent docs silent).
- [OPEN] Exact eval pass-threshold numbers (set in Phase A).
- [OPEN] Pack composition (finalized in Phase A with user).
- [OPEN] Unverified standard versions (Conventional Commits 1.0.0, SemVer 2.0.0, Keep a Changelog 1.1.0, ISO 25010:2023, PMBOK 7, OpenSLO, CWE Top 25 2025 edition, DORA capabilities state, book editions) — verify during authoring.

## Phase 1 blindspots (taught, now tracked)
- B1: RESOLVED — Copilot supports SKILL.md natively (see Known knowns).
- B2: [OPEN] Triggering quality — mitigated by description-writing standards + a triggering test plan; still needs real-world validation.
- B3: RESOLVED as design decision — progressive disclosure (name+description ~100 tokens always in context; body on activation; references on demand) is native to the skills standard.
- B4: RESOLVED as design decision — refresh skill + cadence doc (user approved).
- B5: [OPEN] Overlap boundaries between reviewer/security/optimizer skills — to be addressed by inventory design; council should scrutinize.
- B6: RESOLVED — SKILL.md is the cross-harness open standard.

## Unknown knowns (assumptions dug out)
- User assumed Copilot could run Claude-style skills — turned out TRUE (verified).
- [OPEN] User may assume teammates' Copilot setups match theirs (VS Code version, skills feature enabled, Python present).

## Unknown unknowns
- (Phase 4 council to surface)

## Topic checklist
| Topic | Status |
|---|---|
| Users | ANSWERED (team, private repo) |
| Features (skill inventory) | ANSWERED (research-driven exhaustive list + skill-creator + refresh skill) |
| Data (content sources) | ANSWERED (cited authoritative sources, last-verified dates) |
| Integrations (Copilot mechanics) | ANSWERED (SKILL.md verified) |
| Constraints | ANSWERED (offline, no paid tools, privacy, English) |
| Success criteria | ANSWERED (triggering, quality, adoption, coverage) |
| Risks | to be drafted in PLAN.md |
