BEGIN COUNCIL REVIEW PACKET (ROUND 2 — CROSS-EXAMINATION)
You are a critical reviewer of a software project plan. You have no other
context; everything you need is below.

The plan below is REVISED (v2) after a first review round; nine refinements
were accepted by the project owner and applied.

Critique this plan on: (1) feasibility, (2) completeness — what unknowns did
the planner miss?, (3) risks, (4) simpler alternatives, (5) fact-hunt:
actively try to refute every named tool, library, API, version, price,
product capability, or legal/compliance claim — flag anything you cannot
verify or suspect is made up.

ADDITIONALLY: a previous reviewer raised the numbered points listed AFTER the
plan. Answer EVERY numbered point with a verdict: AGREE (the updated plan
handles it), AGREE WITH CHANGE (concern accepted, different fix — say which),
or REBUT (reason). Then list any NEW major concerns, minor concerns, and
concrete refinements — most important first. Be specific and brief.

Context for tags: [USER] = owner said it in interview; [CONFIRMED] =
owner-approved or verified with a real tool (noted which); [CANDIDATE] =
unverified suggestion, must be checked before use; [OPEN] = unresolved.

--- PLAN BEGINS ---
# PLAN.md — Fable Skills: End-to-End Software Engineering Skill Library

Draft v2 (after council round 1). Tags: `[USER]` said in interview · `[CONFIRMED]` user-approved or tool-verified (noted which) · `[CANDIDATE]` unverified suggestion — verify before use · `[OPEN]` unresolved.

## 1. Project summary

- [USER] Build a complete, exhaustive library of AI-agent skills covering everything needed to complete a software engineering project end to end — artifact skills (PRD, design docs, stories, slide decks…) and expert-role skills (code reviewer, OWASP security scanner, SQL optimizer, architect…).
- [USER] Primary harness: GitHub Copilot (user's surface: VS Code Copilot Chat); design must be harness/platform-agnostic.
- [USER] Audience: the user's team. Repo will be private.
- [USER] Success criteria: (1) right skill triggers at the right time, (2) output quality beats raw Copilot, (3) team adoption, (4) full lifecycle coverage.

## 2. Foundational decisions (hardest to change later)

### 2.1 Format: Agent Skills open standard
- [CONFIRMED] (verified via web search, research subagent + council fact-hunt, July 2026) Each skill is a folder with `SKILL.md` (YAML frontmatter: `name` ≤64 chars lowercase-hyphen matching folder name; `description` ≤1024 chars — Codex counts bytes) per the agentskills.io specification.
- [CONFIRMED] (verified via web search; wording corrected by council) GitHub Copilot supports Agent Skills since Dec 2025 (VS Code stable early Jan 2026; `gh skill` CLI is public preview, Apr 2026). The same format is read by Claude Code, Codex, Cursor, and Antigravity — one artifact satisfies "Copilot priority" and "platform-agnostic". Treat all of this as a fast-moving preview-era surface, not settled GA (see R2).
- [CONFIRMED] (council accepted) Frontmatter recipe: spec fields (`name`, `description`, `license`, `metadata`, `compatibility`) plus `user-invocable` / `disable-model-invocation` / `argument-hint`. Per-surface support differs (VS Code docs list these fields; GitHub cloud-agent docs do not) — the harness compatibility matrix (§2.5) records field support per surface instead of blanket claims. Unknown fields are ignored by other harnesses.
- [CONFIRMED] (council accepted) `metadata: {version: "1.0.0", last-verified: "2026-07-06"}` — all values written as strings (spec: string key-value map; non-string values may break validators).

### 2.2 Repo layout and distribution
- [CONFIRMED] (user approved) `F:\AI_Projects\Fable_Skills` is the single git repo, pushed to GitHub as a private repo; each skill is a plain subfolder.
- [CONFIRMED] (verified via web search — gh manual confirms `skills/*/SKILL.md` auto-discovery; council round 1) `skills/` is the library source of truth; consumers install into their projects via `gh skill install <owner>/Fable_Skills <skill>` (lands in the consuming project's skill directory) or manual copy into `.github/skills/`. Harnesses load skills from `.github/skills/`, `.claude/skills/`, or `.agents/skills/` inside the consuming project — never from a bare `skills/` folder — so the consumer path must be documented in every README.
- [CONFIRMED] (council accepted) Release discipline: git tags per library release (v1.0.0…) + CHANGELOG.md, so `gh skill install …@vX.Y.Z` pins versions instead of floating on default-branch HEAD.
- [CONFIRMED] (council accepted) LICENSE = simple internal-use notice for the private repo; must not block Phase A.

```
Fable_Skills/
├── README.md                  # catalog: table of all skills, install packs, install instructions
├── LICENSE                    # internal-use notice
├── CHANGELOG.md               # + git tags per release
├── docs/
│   ├── PER-HARNESS-SETUP.md   # master setup guide + pinned known-good versions
│   ├── COMPATIBILITY.md       # harness matrix: official source URL, paths, invocation, frontmatter support per surface, verified date
│   └── AUTHORING-GUIDE.md     # standards below, incl. shared constraints section
├── skills/
│   └── <skill-name>/
│       ├── SKILL.md
│       ├── README.md          # per-skill usage + quick install; links to docs/ for common steps
│       ├── references/        # checklists, deep guidance (one level deep) + SOURCES manifest
│       ├── assets/            # document templates
│       ├── scripts/           # Python helpers (only where needed)
│       └── evals/             # trigger + output test cases
└── template/                  # blank skill scaffold used by skill-creator
```

### 2.3 Authoring standards (applied to every skill)
- [CONFIRMED] (verified via web search — agentskills.io, Anthropic engineering, 2026) Description: third-person what-it-does + "Use this skill when…" trigger half; trigger keywords AND the negative boundary ("Not for X — use skill Y") within the FIRST 250 characters; total ≤500 chars (bytes); CI-enforced. Body <500 lines / <5k tokens, imperative voice; references one level deep with explicit load conditions; output templates over prose; checklists for multi-step workflows.
- [CONFIRMED] (user approved) Depth model: concise SKILL.md core + reference files (checklists, templates, examples) loaded only when needed.
- [CONFIRMED] (user approved + council refined) Source citations: each skill carries a source manifest (standard name, exact version, URL, last-verified date, offline-fallback note) in `references/SOURCES.md`.
- [CONFIRMED] (user approved) Helper scripts (Python) where text alone can't do the job (e.g., PPTX generation).
- [CONFIRMED] (verified via web search + council refined) Script rules: stdlib-only Python preferred; non-interactive; forward slashes in paths; cross-platform invocation documented (`python` vs `python3` on Windows); actionable errors; bounded output; `--dry-run` for anything destructive; CI tests script invocation on Windows, not just path lint.
- [CONFIRMED] (council accepted) Library security gate: no `allowed-tools`/shell pre-approval in any skill by default; stdlib-only scripts unless explicitly approved; no network calls in scripts; manual review of every script-bearing skill before team rollout.
- [CONFIRMED] (user approved + council refined) Hard constraints (never browse/download/send data to external internet; no paid tools; company-data privacy; English only) live as ONE line per skill + a shared AUTHORING-GUIDE section — not 50 copies of boilerplate.
- [CONFIRMED] (user approved) Technology-agnostic guidance with language-specific notes where it matters; Scrum-based Agile assumed for process skills (Kanban variations noted).
- [CANDIDATE] PPTX/DOCX scripts: `python-pptx`/`python-docx` as offline dependencies if stdlib impractical — verify org permits them (Phase 0); fallback: Markdown/HTML the user converts.

### 2.4 Per-skill README (user requirement)
- [CONFIRMED] (user approved) Every skill folder contains README.md: what the skill does, example prompts, and setup + usage per harness (Copilot VS Code, Cursor, Antigravity, Claude Code, and similar).
- [CONFIRMED] (council accepted) Per-skill README = skill-specific usage + short quick-install inline; common install steps live in `docs/PER-HARNESS-SETUP.md` (drift avoidance).
- Verification status of harness paths: Copilot VS Code + Claude Code + Codex [CONFIRMED] (official docs, July 2026); Cursor compat-scan of `.claude/skills/` and Antigravity paths (`.agents/skills/` project; `~/.gemini/config/skills/` global; `~/.agents/skills/` NOT read) [CANDIDATE] — community-sourced, labeled as such with last-verified dates in COMPATIBILITY.md.

### 2.5 Install packs (trigger-budget mitigation)
- [CONFIRMED] (council accepted, both seats) 4–6 curated install packs (e.g., `discovery`, `agile-delivery`, `build`, `quality-security`, `data`, `ops-docs`); recommend ≤15 skills installed per project. Rationale (verified): Claude Code truncates each listing description at ~250 chars and budgets ~1% of context (configurable); Codex caps the listing at 2% of context or 8,000 chars fallback; Copilot limits undocumented. All 55 at once would be silently truncated.

## 3. Skill inventory (research-derived)

[USER] The user's examples were a starting point; research determines the exhaustive end-to-end list, and skill files are built for the full list.
[CONFIRMED] (user approved) Inventory = 55 skills: 53 lifecycle + 2 meta, built in tier order. Council round 1 added 5 gap-fillers (UX, compliance, data governance, AI evals, migration).
[CANDIDATE] Individual skill definitions below remain candidates until each is authored against verified sources.

### Meta (build first — they build the rest)
| Skill | Purpose |
|---|---|
| `skill-creator` | [USER-required] Takes user requirements → produces a new skill folder (SKILL.md, README, references, evals) conforming to this library's standards |
| `library-maintainer` | [CONFIRMED] (user approved + council refined) Re-verifies sources, updates stale content, runs validation. Defines WHO re-verifies outside the org and WHERE results are recorded. Cadence: [OPEN] (quarterly proposed) |

### Product & Discovery (6)
`prd-writer` (1) · `product-vision-writer` (2) · `product-roadmap-writer` (2) · `persona-writer` (3) · `user-story-mapper` (2) · `ux-design-reviewer` (2, council addition)

### Agile Process — Scrum (7)
`epic-story-breakdown` (1) · `user-story-writer` (1, owns INVEST + Gherkin) · `agile-estimator` (2) · `sprint-facilitator` (2) · `retrospective-facilitator` (2) · `backlog-refiner` (2) · `definition-of-done-writer` (3)

### Architecture & Design (10)
`architecture-doc-writer` (1, arc42 v9 + C4) · `c4-diagrammer` (1, Mermaid/PlantUML) · `adr-writer` (1, MADR 4.0.0) · `rfc-writer` (2) · `api-designer` (1, OpenAPI 3.2.0 + RFC 9457) · `data-modeler` (2) · `threat-modeler` (1, STRIDE) · `design-reviewer` (2) · `tech-spike-planner` (3) · `legacy-migration-planner` (3, council addition)

### Implementation (6)
`tdd-developer` (1) · `refactoring-expert` (1) · `systematic-debugger` (1) · `coding-standards-writer` (3) · `git-workflow-expert` (1, Conventional Commits) · `code-documenter` (3)

### Quality & Testing (7)
`code-reviewer` (1, Google eng-practices; routes findings) · `test-strategist` (1, ISTQB v4.0.1) · `test-automation-engineer` (1) · `performance-tester` (2) · `performance-optimizer` (2) · `accessibility-auditor` (2, WCAG 2.2) · `ai-evals-designer` (3, council addition)

### Security & Compliance (6)
`security-code-reviewer` (1, OWASP Top 10:2025 [final text Jan 2026] + ASVS 5.0.0 + CWE Top 25 as primaries — Code Review Guide 2.0 (2017) demoted to historical reference per council) · `security-requirements-writer` (2, ASVS 5.0.0) · `dependency-auditor` (2, description explicitly states: offline — reasons over lockfiles/SBOMs, CANNOT confirm live CVEs) · `secrets-hygiene-auditor` (2) · `llm-app-security-reviewer` (3, OWASP LLM Top 10 2025) · `compliance-privacy-reviewer` (2, council addition — GDPR-style principles, privacy-by-design)

### Data & Databases (4)
`db-schema-designer` (2) · `sql-optimizer` (1) · `db-migration-planner` (2, expand-contract) · `data-governance-advisor` (3, council addition)

### Delivery & Operations (10)
`cicd-pipeline-designer` (1, DORA capabilities) · `deployment-strategist` (2) · `release-manager` (1, SemVer + Keep a Changelog) · `iac-reviewer` (3) · `observability-engineer` (2, OpenTelemetry concepts) · `slo-designer` (2, SRE Workbook) · `incident-responder` (2) · `postmortem-writer` (1) · `runbook-writer` (2) · `dora-metrics-analyst` (3)

### Management & Communication (5)
`project-status-reporter` (2) · `slide-deck-builder` (2, deck content structure + PPTX script) · `meeting-notes-writer` (3) · `risk-register-writer` (2) · `estimation-doc-writer` (3)

### Documentation (4)
`readme-writer` (1) · `user-guide-writer` (2, Diátaxis) · `onboarding-guide-writer` (3) · `tech-writer` (2, editing role, owns no templates)

### Overlap boundary rules (written into descriptions and bodies)
- [CANDIDATE] `code-reviewer` routes, never duplicates: security → `security-code-reviewer`, performance → `performance-optimizer`, SQL → `sql-optimizer`; finding-tag namespaces (REV-/SEC-/PERF-/SQL-).
- [CANDIDATE] Security triad: `threat-modeler` design-time · `security-requirements-writer` gate checklist · `security-code-reviewer` code-time findings.
- [CANDIDATE] Data triad: `data-modeler` (logical) → `db-schema-designer` (physical) → `sql-optimizer` (queries); migrations only in `db-migration-planner`.
- [CANDIDATE] Story chain: `prd-writer` → `user-story-mapper` → `epic-story-breakdown` → `user-story-writer`; only the last defines Gherkin/INVEST rules.
- [CANDIDATE] Sibling descriptions name their neighbors; evals include sibling prompts as should-NOT-trigger cases.

## 4. Quality & testing plan

- [CONFIRMED] (council accepted) Per skill: `skills-ref validate`; ~20 labeled trigger queries (varied should-trigger + near-miss should-NOT-trigger); ≥3 output eval cases (with-skill vs without-skill).
- [CONFIRMED] (council accepted) Eval runner: scripted via Claude Code headless (and/or Copilot CLI) as proxy harness — acknowledged proxy ≠ exact Copilot behavior — PLUS one manual VS Code Copilot smoke test per skill before team adoption.
- [CONFIRMED] (council accepted) Pass thresholds defined in AUTHORING-GUIDE: trigger true-positive rate, near-miss false-positive rate, output rubric score. [OPEN] exact threshold numbers set during Phase A.
- [CANDIDATE] CI (local, no external services): frontmatter name/dir match; description ≤500 chars with triggers in first 250; forward-slash paths; README/SOURCES/last-verified present; Windows script-invocation test.

## 5. Build phases

- [CONFIRMED] (council accepted) **Phase 0 — In-org go/no-go gate:** hand-write ONE trivial skill, install in `.github/skills/` of a test repo, verify it triggers in the team's actual VS Code Copilot Chat; confirm Python version and whether `python-pptx`/`python-docx` are permitted. Hard gate for everything below.
- [CANDIDATE] **Phase A — Foundation:** repo scaffold, private GitHub repo, AUTHORING-GUIDE.md (incl. thresholds, security gate, constraints section), PER-HARNESS-SETUP.md (pinned known-good versions), COMPATIBILITY.md matrix, template/, root README with packs, CI validation script, eval runner harness; then build `skill-creator`.
- [CONFIRMED] (council accepted) **First-5 gate:** `skill-creator` generates the first 5 skills; user reviews generator output quality before mass production.
- [CANDIDATE] **Phase B — Tier 1** (20 skills incl. meta): research-distilled content, SKILL.md, README, references+SOURCES, assets, scripts where needed, evals; validate.
- [CONFIRMED] (council accepted) **Pilot gate:** after Tier 1, team pilot (2–4 weeks) in real projects; usage data decides whether Tiers 2–3 proceed as planned, re-scoped, or trimmed.
- [CANDIDATE] **Phase C — Tier 2** (~24 skills), same recipe, conditional on pilot.
- [CANDIDATE] **Phase D — Tier 3** (~11 skills) + library-maintainer cadence doc + catalog polish + rollout instructions.
- [CANDIDATE] Build agents work in parallel subagents per category, with a consistency reviewer pass (terminology, boundaries, tag namespaces).

## 6. Challenges & Risks

- [CONFIRMED] (council, both seats) R1 Trigger dilution: 55 descriptions exceed every known listing budget (Claude ~1% + ~250-char/description truncation; Codex 2%/8k; Copilot undocumented). Mitigation: install packs ≤15/project (§2.5) + description discipline (§2.3).
- [CONFIRMED] (council reframed) R2 Preview-surface churn: Copilot Agent Skills + `gh skill` are preview-era and changing; org policy could also disable them. Mitigation: Phase 0 gate; pin known-good VS Code/Copilot versions in PER-HARNESS-SETUP.md; expect breaking changes; library-maintainer re-verifies.
- [CANDIDATE] R3 Staleness: standards drift. Mitigation: SOURCES manifests + library-maintainer + [OPEN] cadence.
- [CANDIDATE] R4 Overlap confusion: boundary sentences + near-miss evals.
- [CANDIDATE] R5 Windows/POSIX drift: authoring standards + Windows CI invocation test.
- [CANDIDATE] R6 Content quality: skills distilled from named authoritative sources with citations, never model memory alone.
- [CANDIDATE] R7 Scale/consistency: 55 deep skills. Mitigation: tiers, first-5 gate, pilot gate, template-driven generation, consistency pass.
- [CONFIRMED] (council, Codex seat) R8 Library-as-attack-surface: skills can carry prompt injection / malicious scripts. Mitigation: security gate (§2.3), pinned installs, script review before rollout.

## 7. Remaining Unknowns

- [OPEN] Phase 0 results: org enables Agent Skills? Python version? python-pptx/docx permitted?
- [OPEN] Review cadence length (quarterly proposed).
- [OPEN] Exact eval pass-threshold numbers (set in Phase A).
- [OPEN] Copilot-side listing/count limits (none documented; absence unverified).
- [OPEN] Cursor global-skills dir + compat scan; Antigravity paths — community-sourced only.
- [OPEN] Whether Copilot cloud agent honors `user-invocable`/`argument-hint` (VS Code does; cloud-agent docs silent).
- [OPEN] Standards versions not verified this session: Conventional Commits 1.0.0, SemVer 2.0.0, Keep a Changelog 1.1.0, ISO 25010:2023, PMBOK 7, OpenSLO version, CWE Top 25 2025 edition, DORA capabilities catalog state, book editions — verify during authoring of affected skills.
- [OPEN] Pack composition (which skills in which pack) — finalized in Phase A with user.

## 8. Assumptions register

- [CONFIRMED] (user approved) Teammates' setups match the user's: VS Code with Copilot, Agent Skills available, Python installed. (Phase 0 verifies the skills feature actually works in-org.)
- [CONFIRMED] (user approved) "Exhaustive" = the 55-skill inventory above, built in tier order with council-added gates.
- [CONFIRMED] (user approved) The build is executed by AI coding agents following this plan phase by phase, with user review at the gates.
--- PLAN ENDS ---

A previous reviewer said (answer every point with AGREE / AGREE WITH CHANGE / REBUT):

1. The repo layout is wrong for the primary target: Copilot loads project skills from .github/skills, .claude/skills, or .agents/skills, not from a bare skills/ folder; gh skill is public preview, not stable.
2. Several [CONFIRMED] portability claims were overstated: Cursor and Antigravity support/paths are unverified from official docs and should not sit beside officially-documented harnesses.
3. The frontmatter compatibility recipe is unsafe: user-invocable, disable-model-invocation, and argument-hint are not listed in GitHub's Copilot cloud-agent skill docs; treating them as universally honored is unverified.
4. Trigger dilution may invalidate "install all skills": Codex caps the skill list at 2% of context or 8,000 chars; Claude Code truncates listing text; the original "~1%" claim was outdated/imprecise.
5. "Exhaustive end-to-end" is not proven: the inventory misses or underweights UX/product design, frontend implementation, mobile, cloud-provider specifics, compliance/privacy, data governance, AI evals, support ops, procurement/change management, and migration strategy.
6. Feasibility is weak: 50+ deep skills is a large documentation/QA program; the plan lacked effort estimates, a quality bar, an owner/reviewer matrix, and stop/go gates after Tier 1.
7. The "no external internet" rule conflicts with source verification, dependency auditing, and staleness management; the plan did not define who re-verifies outside the org, where results are stored, or how offline skills avoid recommending stale standards.
8. Security governance is underdeveloped: skills can contain scripts and tool permissions; the plan needs trust review, pinning, provenance, allowed-tools policy, and script approval rules before team rollout.
9. metadata values must be strings; non-string dates may break validators.
10. "Third person description" conflicts with Agent Skills guidance recommending imperative "Use this skill when…" phrasing.
11. Per-skill READMEs will drift; centralizing common harness setup is better than repeating five setup sections per skill.
12. Scrum-as-default may overfit process skills to one operating model.
13. The eval plan lacked pass thresholds (precision/recall targets, smoke-test criteria).
14. dependency-auditor's offline limitation must be explicit: lockfile reasoning cannot confirm current CVEs.

END COUNCIL REVIEW PACKET
