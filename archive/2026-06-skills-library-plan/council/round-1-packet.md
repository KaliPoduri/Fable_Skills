BEGIN COUNCIL REVIEW PACKET
You are a critical reviewer of a software project plan. You have no other
context; everything you need is below.
Critique this plan on: (1) feasibility, (2) completeness — what unknowns did
the planner miss?, (3) risks, (4) simpler alternatives, (5) fact-hunt:
actively try to refute every named tool, library, API, version, price,
product capability, or legal/compliance claim — flag anything you cannot
verify or suspect is made up.
Reply as a numbered list of major concerns, then minor concerns, then
concrete refinements — most important first. Be specific and brief.

Context for tags used in the plan: [USER] = the project owner said it in an
interview; [CONFIRMED] = owner-approved or verified with a real tool (noted
which); [CANDIDATE] = unverified suggestion that must be checked before use;
[OPEN] = unresolved question.

--- PLAN BEGINS ---
# PLAN.md — Fable Skills: End-to-End Software Engineering Skill Library

Draft v1 (Phase 3). Tags: `[USER]` said in interview · `[CONFIRMED]` user-approved or tool-verified (noted which) · `[CANDIDATE]` unverified suggestion — verify before use · `[OPEN]` unresolved.

## 1. Project summary

- [USER] Build a complete, exhaustive library of AI-agent skills covering everything needed to complete a software engineering project end to end — artifact skills (PRD, design docs, stories, slide decks…) and expert-role skills (code reviewer, OWASP security scanner, SQL optimizer, architect…).
- [USER] Primary harness: GitHub Copilot (user's surface: VS Code Copilot Chat); design must be harness/platform-agnostic.
- [USER] Audience: the user's team. Repo will be private.
- [USER] Success criteria: (1) right skill triggers at the right time, (2) output quality beats raw Copilot, (3) team adoption, (4) full lifecycle coverage.

## 2. Foundational decisions (hardest to change later)

### 2.1 Format: Agent Skills open standard
- [CONFIRMED] (verified via web search, research subagent, July 2026) Each skill is a folder with `SKILL.md` (YAML frontmatter: `name` ≤64 chars lowercase-hyphen matching folder name; `description` ≤1024 chars) per the agentskills.io specification.
- [CONFIRMED] (verified via web search) GitHub Copilot supports Agent Skills GA since Dec 2025/Jan 2026 across VS Code, Copilot CLI, coding agent, and code review; the same format is read by Claude Code, Cursor, Codex, and Antigravity — this satisfies both "Copilot priority" and "platform-agnostic" with one artifact.
- [CONFIRMED] (verified via web search) Portable frontmatter recipe: spec fields (`name`, `description`, `license`, `metadata`, `compatibility`) plus `user-invocable` / `disable-model-invocation` / `argument-hint` (honored by Copilot + Claude Code; unknown fields are ignored by other harnesses).
- [CANDIDATE] Frontmatter `metadata: {version, last-verified}` used for per-skill versioning — verify harnesses tolerate the map before mass-applying.

### 2.2 Repo layout
- [CONFIRMED] (user approved) `F:\AI_Projects\Fable_Skills` is the single git repo, pushed to GitHub as a private repo; each skill is a plain subfolder.
- [CANDIDATE] Skills live under a `skills/` parent directory (`skills/<skill-name>/`), matching anthropics/skills and awesome-copilot conventions and enabling `gh skill install <owner>/Fable_Skills <skill>`:

```
Fable_Skills/
├── README.md                  # catalog: table of all skills, install instructions
├── LICENSE                    # [OPEN] license choice (private repo; still recommended)
├── CHANGELOG.md
├── docs/
│   ├── PER-HARNESS-SETUP.md   # master setup guide (Copilot VS Code, Cursor, Claude Code, Antigravity, Codex)
│   └── AUTHORING-GUIDE.md     # the standards below, for future skills
├── skills/
│   └── <skill-name>/
│       ├── SKILL.md
│       ├── README.md          # per-skill setup+usage per harness (user requirement)
│       ├── references/        # checklists, deep guidance (one level deep)
│       ├── assets/            # document templates
│       ├── scripts/           # Python helpers (only where needed)
│       └── evals/             # trigger + output test cases
└── template/                  # blank skill scaffold used by skill-creator
```

### 2.3 Authoring standards (applied to every skill)
- [CONFIRMED] (verified via web search — agentskills.io, Anthropic engineering, current 2026) Description = what it does + when to use + trigger keywords + negative boundary ("Not for X — use skill Y"), third person, key use case first; body <500 lines / <5k tokens, imperative voice; references one level deep with explicit load conditions ("Read references/x.md when …"); output templates over prose; checklists for multi-step workflows.
- [CONFIRMED] (user approved) Depth model: concise SKILL.md core + reference files (checklists, templates, examples) loaded only when needed.
- [CONFIRMED] (user approved) Each skill cites its authoritative sources + a last-verified date (in a Sources section of SKILL.md or references/).
- [CONFIRMED] (user approved) Helper scripts (Python) included where text alone can't do the job (e.g., PPTX generation).
- [CONFIRMED] (verified via web search) Script rules: stdlib-only Python preferred; non-interactive; forward slashes in all paths; invoked as `python3 scripts/x.py`; actionable error messages; bounded output; `--dry-run` for anything destructive.
- [CONFIRMED] (user approved) Hard constraint baked into every skill: never instruct the agent to browse/download from/send data to the external internet; no paid tools/services; company-data privacy respected; English only.
- [CONFIRMED] (user approved) Technology-agnostic guidance with language-specific notes where it matters; Scrum-based Agile assumed for process skills (Kanban variations noted).
- [CANDIDATE] PPTX/DOCX generation scripts: if pure-stdlib is impractical, use `python-pptx`/`python-docx` as pre-installed offline dependencies — verify these libraries are permitted/installable inside the org before relying on them; fallback is generating Markdown/HTML content the user converts.

### 2.4 Per-skill README (user requirement)
- [CONFIRMED] (user approved) Every skill folder contains README.md: what the skill does, example prompts, and setup + usage for each harness (GitHub Copilot in VS Code, Cursor, Antigravity, Claude Code, and similar).
- [CONFIRMED] (verified via web search) Verified per-harness install paths to document: Copilot VS Code (`.github/skills/`, `.claude/skills/`, `.agents/skills/`; personal `~/.copilot/skills/`), Claude Code (`.claude/skills/`, `~/.claude/skills/`), Cursor (`.cursor/skills/`, `.agents/skills/` + compat scan of `.claude/skills/`), Codex (`.agents/skills/`, `~/.agents/skills/`), Antigravity (`.agents/skills/`; global `~/.gemini/config/skills/` — verified via community article, not official docs), plus `gh skill install` (gh ≥2.90.0) for any of them.
- [CANDIDATE] To avoid 50 near-identical READMEs drifting: per-skill README covers skill-specific usage and links to `docs/PER-HARNESS-SETUP.md` for the common install steps, while still including a short quick-install section inline so it works standalone.

## 3. Skill inventory (research-derived)

[USER] The user's examples were a starting point; research determines the exhaustive end-to-end list, and skill files are built for all of it.
[CANDIDATE] The full inventory below came from subagent research (July 2026) with source-version verification; individual skills await user/council review. 50 skills = 48 lifecycle skills + 2 meta skills. [CONFIRMED] (user approved) Building all 50 in tier order (Tier 1 → 2 → 3).

### Meta (build first — they build the rest)
| Skill | Kind | Purpose |
|---|---|---|
| `skill-creator` | Role | [USER-required] Takes user requirements → produces a new skill folder (SKILL.md, README, references, evals) conforming to this library's standards |
| `library-maintainer` | Role | [CONFIRMED] (user approved) Re-verifies sources, updates stale content, runs validation; documents review cadence. Web re-verification runs outside the org environment |

### Product & Discovery (5)
`prd-writer` (Tier 1) · `product-vision-writer` (2) · `product-roadmap-writer` (2) · `persona-writer` (3) · `user-story-mapper` (2)

### Agile Process — Scrum (7)
`epic-story-breakdown` (1) · `user-story-writer` (1, owns INVEST + Gherkin rules) · `agile-estimator` (2) · `sprint-facilitator` (2) · `retrospective-facilitator` (2) · `backlog-refiner` (2) · `definition-of-done-writer` (3)

### Architecture & Design (9)
`architecture-doc-writer` (1, arc42 v9 + C4) · `c4-diagrammer` (1, Mermaid/PlantUML) · `adr-writer` (1, MADR 4.0.0) · `rfc-writer` (2) · `api-designer` (1, OpenAPI 3.2.0 + RFC 9457) · `data-modeler` (2) · `threat-modeler` (1, STRIDE) · `design-reviewer` (2) · `tech-spike-planner` (3)

### Implementation (6)
`tdd-developer` (1) · `refactoring-expert` (1) · `systematic-debugger` (1) · `coding-standards-writer` (3) · `git-workflow-expert` (1, Conventional Commits) · `code-documenter` (3)

### Quality & Testing (6)
`code-reviewer` (1, Google eng-practices; routes security/perf/SQL findings to sibling skills) · `test-strategist` (1, ISTQB v4.0.1) · `test-automation-engineer` (1) · `performance-tester` (2) · `performance-optimizer` (2) · `accessibility-auditor` (2, WCAG 2.2)

### Security (5)
`security-code-reviewer` (1, OWASP Top 10:2025 + Code Review Guide 2.0 + CWE) · `security-requirements-writer` (2, OWASP ASVS 5.0.0) · `dependency-auditor` (2, offline: reasons over lockfiles/SBOMs — no live CVE lookup, limitation stated in skill) · `secrets-hygiene-auditor` (2) · `llm-app-security-reviewer` (3, OWASP LLM Top 10 2025)

### Data & Databases (3)
`db-schema-designer` (2) · `sql-optimizer` (1) · `db-migration-planner` (2, expand-contract)

### Delivery & Operations (10)
`cicd-pipeline-designer` (1, DORA capabilities) · `deployment-strategist` (2) · `release-manager` (1, SemVer + Keep a Changelog) · `iac-reviewer` (3) · `observability-engineer` (2, OpenTelemetry concepts) · `slo-designer` (2, SRE Workbook) · `incident-responder` (2) · `postmortem-writer` (1) · `runbook-writer` (2) · `dora-metrics-analyst` (3)

### Management & Communication (5)
`project-status-reporter` (2) · `slide-deck-builder` (2, owns deck content structure + PPTX script) · `meeting-notes-writer` (3) · `risk-register-writer` (2) · `estimation-doc-writer` (3)

### Documentation (4)
`readme-writer` (1) · `user-guide-writer` (2, Diátaxis) · `onboarding-guide-writer` (3) · `tech-writer` (2, editing role, owns no templates)

### Overlap boundary rules (written into descriptions and bodies)
- [CANDIDATE] `code-reviewer` routes, never duplicates: security → `security-code-reviewer`, performance → `performance-optimizer`, SQL → `sql-optimizer`; distinct finding-tag namespaces (REV-/SEC-/PERF-/SQL-).
- [CANDIDATE] Security triad: `threat-modeler` = design-time · `security-requirements-writer` = gate checklist · `security-code-reviewer` = code-time findings.
- [CANDIDATE] Data triad: `data-modeler` (logical) → `db-schema-designer` (physical) → `sql-optimizer` (queries); migrations only in `db-migration-planner`.
- [CANDIDATE] Story chain: `prd-writer` → `user-story-mapper` → `epic-story-breakdown` → `user-story-writer`; only the last defines Gherkin/INVEST rules.
- [CANDIDATE] Each sibling skill's description names its neighbors ("Not for X — use skill Y") and its evals include the sibling's prompts as should-NOT-trigger cases.

## 4. Quality & testing plan

- [CONFIRMED] (verified via web search — agentskills.io) Per skill: `skills-ref validate` format check; ~20 labeled trigger queries (should-trigger with varied phrasing + near-miss should-NOT-trigger); ≥3 output eval cases in `evals/evals.json` compared with-skill vs without-skill.
- [CANDIDATE] CI (local script, no external services): validate frontmatter name/dir match, description length, forward-slash paths, presence of README/Sources/last-verified in every skill.
- [CANDIDATE] Manual acceptance: user smoke-tests Tier-1 skills in VS Code Copilot Chat in the org environment before mass rollout to the team.
- [OPEN] Whether the org's VS Code/Copilot policy enables Agent Skills, and which VS Code version the team runs (Stable-channel skill-loading bugs were reported early 2026).
- [OPEN] Whether Python 3.11+ is available in the org environment for helper scripts.

## 5. Build phases

- [CANDIDATE] Phase A — Foundation: repo scaffold, git init + private GitHub repo, `docs/AUTHORING-GUIDE.md`, `docs/PER-HARNESS-SETUP.md`, `template/`, root README skeleton, CI validation script, then build `skill-creator` first and use it to generate the rest.
- [CANDIDATE] Phase B — Tier 1 (18 skills incl. meta): each skill gets research-distilled content (from sources already gathered; any new web research happens outside the org), SKILL.md, README, references, assets, scripts where needed, evals; validate.
- [CANDIDATE] Phase C — Tier 2 (22 skills), same recipe.
- [CANDIDATE] Phase D — Tier 3 (10 skills) + `library-maintainer` cadence doc + final catalog polish + team rollout instructions.
- [CANDIDATE] Build agent uses parallel subagents per category to draft skills, with a single reviewer pass for cross-skill consistency (terminology, boundary lines, tag namespaces).

## 6. Challenges & Risks

- [CANDIDATE] R1 Trigger dilution: 50 skills' descriptions all load into the agent's context list; Claude Code budgets ~1% of context and drops/truncates long listings; Codex caps at 8,000 chars; Copilot limits undocumented. Mitigation: tight descriptions, key use case first; consider advising teams to install per-project subsets rather than all 50.
- [CANDIDATE] R2 Org policy blocks: Copilot Agent Skills could be disabled by org admin settings; Python may be unavailable. Mitigation: [OPEN] items verified by user in-org before Phase B completes.
- [CANDIDATE] R3 Staleness: standards drift (OWASP, DORA, spec changes). Mitigation: last-verified dates + `library-maintainer` + [OPEN] cadence (quarterly proposed).
- [CANDIDATE] R4 Overlap confusion: adjacent skills fire wrongly. Mitigation: boundary sentences in descriptions + near-miss evals.
- [CANDIDATE] R5 Windows/POSIX drift: team members on different OSes; scripts must avoid backslash paths and exec-bit assumptions. Mitigation: authoring standards + CI check.
- [CANDIDATE] R6 Content quality risk: LLM-generated skills without domain grounding produce generic advice. Mitigation: every skill distilled from the named authoritative sources, not from model memory alone; citations required.
- [CANDIDATE] R7 Scale of effort: 50 deep skills (guides + templates + scripts + evals + READMEs) is a large build; risk of inconsistency and fatigue. Mitigation: phased tiers, template-driven generation via `skill-creator`, consistency reviewer pass.

## 7. Remaining Unknowns

- [OPEN] Org enables Copilot Agent Skills in VS Code? (user verifies in-org)
- [OPEN] Python 3.11+ available in org? (user verifies)
- [OPEN] `python-pptx`/`python-docx` permitted offline in org, or Markdown/HTML fallback needed?
- [OPEN] License choice for the private repo.
- [OPEN] Review cadence length (quarterly proposed, not confirmed).
- [OPEN] Whether to advise per-project skill subsets vs installing all 50 (trigger-dilution tradeoff).
- [OPEN] Exact `gh skill install` requirements for repo layout (skills/ folder convention inferred, not verified against gh docs).
- [OPEN] Copilot-side listing/count limits for skills (none documented; absence unverified).
- [OPEN] Antigravity setup steps rest on a community article, not official docs.
- [OPEN] Standards versions not verified this session: Conventional Commits 1.0.0, SemVer 2.0.0, Keep a Changelog 1.1.0, ISO 25010:2023, PMBOK 7, OpenSLO version, CWE Top 25 2025, book editions — verify during authoring of the affected skills.

## 8. Assumptions register

- [CONFIRMED] (user approved) Teammates' setups match the user's: VS Code with Copilot, Agent Skills available, Python installed.
- [CONFIRMED] (user approved) "Exhaustive" = the 50-skill inventory above, built in tier order (1 → 2 → 3).
- [CONFIRMED] (user approved) The build is executed by AI coding agents following this plan phase by phase, with user review.
--- PLAN ENDS ---
END COUNCIL REVIEW PACKET
