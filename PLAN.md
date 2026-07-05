# PLAN.md — Fable Skills: End-to-End Software Engineering Skill Library

FINAL (v3, after 2 council rounds — Claude + Codex seats, zero unresolved disputes; user exited at round 2 of 5). Tags: `[USER]` said in interview · `[CONFIRMED]` user-approved or tool-verified (basis noted) · `[CANDIDATE]` unverified suggestion — verify before use · `[OPEN]` unresolved.

## 1. Project summary

- [USER] Build a complete library of AI-agent skills covering everything needed to complete a software engineering project end to end — artifact skills (PRD, design docs, stories, slide decks…) and expert-role skills (code reviewer, OWASP security scanner, SQL optimizer, architect…).
- [USER] Primary harness: GitHub Copilot — specifically Copilot Chat in VS Code (the user's and team's only Copilot surface); design must be harness/platform-agnostic.
- [USER] Audience: the user's team. Repo will be private.
- [USER] Success criteria: (1) right skill triggers at the right time, (2) output quality beats raw Copilot, (3) team adoption, (4) full lifecycle coverage.
- [CONFIRMED] (user approved, round 2) Non-goals — deliberately out of scope, listed as future candidates: frontend implementation specifics, mobile development, cloud-provider-specific guidance, support operations, procurement/change management. "Exhaustive" means the bounded 67-skill inventory in §3, not universal coverage.
- [CONFIRMED] (user approved, round 2) Privacy boundary: all authoring, research, evals, and source re-verification happen on the user's personal machine using library content only; org code/data never enters the build/eval pipeline or prompts; inside the org, skills run fully offline via Copilot only.

## 2. Foundational decisions (hardest to change later)

### 2.1 Format: Agent Skills open standard
- [CONFIRMED] (verified: agentskills.io/specification, July 2026) Each skill is a folder with `SKILL.md` (frontmatter: `name` ≤64 chars lowercase-hyphen matching folder name; `description` ≤1024 chars — Codex counts bytes).
- [CONFIRMED] (verified: github.blog changelog 2025-12-18; code.visualstudio.com docs; wording corrected in council) GitHub Copilot supports Agent Skills since Dec 2025 (VS Code stable ~Jan 2026 — exact date unpinned; `gh skill` CLI is public preview, Apr 2026). Same format read by Claude Code, Codex, Cursor (official docs), Antigravity (community-sourced). Treat as a fast-moving preview-era surface (R2).
- [CONFIRMED] (verified: VS Code docs list `argument-hint`/`user-invocable`/`disable-model-invocation`; GitHub cloud-agent docs do not; spec: unknown fields ignored) Frontmatter recipe: spec fields + those three; per-surface support recorded in COMPATIBILITY.md — including the VS Code `context` (forked execution, experimental) field as its own matrix row. No blanket portability claims.
- [CONFIRMED] (user approved) `metadata: {version: "1.0.0", last-verified: "2026-07-06"}` — all values strings.

### 2.2 Repo layout and distribution
- [CONFIRMED] (user approved) `F:\AI_Projects\Fable_Skills` is the single git repo, private on GitHub; each skill a plain subfolder under `skills/` (library source of truth).
- [CONFIRMED] (verified: gh manual — `gh skill install` auto-discovers `skills/*/SKILL.md` and installs to `.agents/skills/` by default; user approved, round 2) Consumer path: **`.agents/skills/`** is the documented default install location (shared by Copilot, Cursor, Codex, Antigravity, and others), with `.github/skills/` noted for Copilot cloud agent. **Manual copy is the default documented install method** until Phase 0 proves `gh skill` (preview, needs gh ≥2.90.0 — one council seat's gh 2.80.0 lacked it).
- [CONFIRMED] (verified: gh manual, syntax corrected in round 2) Version pinning attaches to the skill: `gh skill install <owner>/Fable_Skills <skill>@v1.2.0`. Release discipline: git tags + CHANGELOG.md.
- [CONFIRMED] (user approved) LICENSE = internal-use notice; non-blocking.

```
Fable_Skills/
├── README.md                  # catalog: all 67 skills, packs, non-goals, install (manual first, gh skill when proven)
├── LICENSE                    # internal-use notice
├── CHANGELOG.md               # + git tags per release
├── VERIFICATION-LOG.md        # source re-verification results (governance)
├── docs/
│   ├── PER-HARNESS-SETUP.md   # master setup guide + pinned known-good versions
│   ├── COMPATIBILITY.md       # matrix: official URL / command transcript, paths, invocation, frontmatter per surface, verified date
│   └── AUTHORING-GUIDE.md     # standards, voice split, thresholds, security gate, shared constraints section
├── skills/
│   └── <skill-name>/
│       ├── SKILL.md
│       ├── README.md          # skill usage + quick install; links to docs/ for common steps; CI-checked links/boilerplate
│       ├── references/        # one level deep; incl. SOURCES.md manifest
│       ├── assets/            # templates
│       ├── scripts/           # Python, only where needed
│       └── evals/             # trigger + output cases
└── template/                  # blank scaffold used by skill-creator
```

### 2.3 Authoring standards (every skill)
- [CONFIRMED] (verified: agentskills.io + Anthropic engineering, 2026) Description: third-person what-it-does + "Use this skill when…" triggers; keywords AND negative boundary in FIRST 250 chars; total ≤500 chars/bytes (library policy — CI message distinguishes it from the 1024 spec limit). Body <500 lines, imperative voice (AUTHORING-GUIDE states the voice split explicitly); references one level deep with load conditions; output templates; checklists for workflows.
- [CONFIRMED] (user approved) Depth: concise SKILL.md + reference files loaded on demand.
- [CONFIRMED] (user approved) Source manifest per skill (`references/SOURCES.md`): standard, exact version, official URL, last-verified date, offline-fallback note. Twice-verified URLs recorded up front: OWASP Top 10:2025 (owasp.org/Top10/2025), ASVS 5.0.0, OWASP LLM Top 10 2025. ISTQB v4.0.1 cited as a copyright-only update of v4.0.
- [CONFIRMED] (user approved, round 2) Document/slide generation: Markdown/HTML output is PRIMARY; `python-pptx`/`python-docx` optional secondary if Phase 0 permits.
- [CONFIRMED] (verified + user approved) Script rules: stdlib-only preferred; non-interactive; forward slashes; cross-platform invocation (`python` vs `python3` documented); actionable errors; bounded output; `--dry-run` for destructive ops; CI tests invocation on Windows.
- [CONFIRMED] (user approved) Library security gate: no `allowed-tools`/shell pre-approval by default; stdlib-only unless approved; no network calls in scripts; manual review of every script-bearing skill before rollout (reviewer named in §5 governance). AUTHORING-GUIDE cites GitHub's own warning that skills may contain prompt injection/malicious scripts.
- [CONFIRMED] (user approved) Hard constraints (no external internet in-org, no paid tools, privacy, English) = one line per skill + shared AUTHORING-GUIDE section.
- [CONFIRMED] (user approved) Technology-agnostic; Scrum assumed for process skills (Kanban noted). `compliance-privacy-reviewer` carries a non-legal-advice boundary + jurisdiction-assumptions note.

### 2.4 Per-skill README (user requirement)
- [CONFIRMED] (user approved) Every skill folder has README.md: what it does, example prompts, setup + usage per harness (Copilot VS Code, Cursor, Antigravity, Claude Code, and similar); quick-install inline; common steps centralized in docs/PER-HARNESS-SETUP.md; CI checks links/boilerplate drift.
- Harness verification status: Copilot VS Code, Claude Code, Codex, **Cursor** (upgraded round 2 — official cursor.com/docs/skills: `.cursor/skills/` primary, `.claude/skills/` legacy-compat) = [CONFIRMED] official docs. Antigravity = [CANDIDATE] community-sourced (project `.agents/skills/`; global `~/.gemini/config/skills/`; `~/.agents/skills/` NOT read) — labeled with last-verified dates.

### 2.5 Install packs (trigger-budget mitigation)
- [CONFIRMED] (user approved; budgets verified: Codex 2%-of-context/8k fallback per developers.openai.com; Claude Code configurable per-description cap + ~1% listing budget dropping least-used first — corrected from stale "250-char" figure in round 2; Copilot undocumented) 4–6 curated packs (e.g., `discovery`, `agile-delivery`, `build`, `quality-security`, `data`, `ops-docs`); recommend ≤15 skills installed per project. All 67 at once would be silently truncated on every known harness.

## 3. Skill inventory — 67 total (65 lifecycle + 2 meta; count corrected in round 2)

[USER] Examples were a starting point; research determined the list.
[CONFIRMED] (user approved, round 2) Tier 1 (21) authored first; Tier 2 (30) authored only if the pilot supports it; Tier 3 (14) = NAMED BACKLOG — cataloged with name/description but full content authored on pilot demand. Meta (2) built in Phase A, outside tier counts.
[CANDIDATE] Individual skill definitions remain candidates until authored against verified sources.

### Meta (Phase A)
`skill-creator` [USER-required] · `library-maintainer` [CONFIRMED] (user approved)

### Product & Discovery (6)
T1: `prd-writer` · T2: `product-vision-writer`, `product-roadmap-writer`, `user-story-mapper`, `ux-design-reviewer` · T3: `persona-writer`

### Agile Process — Scrum (7)
T1: `epic-story-breakdown`, `user-story-writer` (owns INVEST+Gherkin) · T2: `agile-estimator`, `backlog-refiner`, `sprint-facilitator`*, `retrospective-facilitator`* · T3: `definition-of-done-writer`
(* = pilot-conditional: kept only if pilot shows they beat raw Copilot — council round 2)

### Architecture & Design (10)
T1: `architecture-doc-writer` (arc42 v9 + C4), `c4-diagrammer`, `adr-writer` (MADR 4.0.0), `api-designer` (OpenAPI 3.2.0 + RFC 9457), `threat-modeler` (STRIDE) · T2: `rfc-writer`, `data-modeler`, `design-reviewer` · T3: `tech-spike-planner`, `legacy-migration-planner`

### Implementation (6)
T1: `tdd-developer`, `refactoring-expert`, `systematic-debugger`, `git-workflow-expert` (Conventional Commits) · T3: `coding-standards-writer`, `code-documenter`

### Quality & Testing (7)
T1: `code-reviewer` (Google eng-practices; routes findings), `test-strategist` (ISTQB v4.0.1), `test-automation-engineer` · T2: `performance-tester`, `performance-optimizer`, `accessibility-auditor` (WCAG 2.2) · T3: `ai-evals-designer`

### Security & Compliance (6)
T1: `security-code-reviewer` (OWASP Top 10:2025 + ASVS 5.0.0 + CWE Top 25 primaries; 2017 Code Review Guide demoted to historical) · T2: `security-requirements-writer` (ASVS 5.0.0), `dependency-auditor` (offline — CANNOT confirm live CVEs, stated in description), `secrets-hygiene-auditor`, `compliance-privacy-reviewer` (non-legal-advice boundary) · T3: `llm-app-security-reviewer` (OWASP LLM Top 10 2025)

### Data & Databases (4)
T1: `sql-optimizer` · T2: `db-schema-designer`, `db-migration-planner` (expand-contract) · T3: `data-governance-advisor`

### Delivery & Operations (10)
T1: `cicd-pipeline-designer` (DORA), `release-manager` (SemVer + Keep a Changelog), `postmortem-writer` · T2: `deployment-strategist`, `observability-engineer` (OpenTelemetry), `slo-designer` (SRE Workbook), `incident-responder`, `runbook-writer` · T3: `iac-reviewer`, `dora-metrics-analyst`

### Management & Communication (5)
T2: `project-status-reporter`, `slide-deck-builder` (content structure; Markdown/HTML primary output), `risk-register-writer` · T3: `meeting-notes-writer`*, `estimation-doc-writer`

### Documentation (4)
T1: `readme-writer` · T2: `user-guide-writer` (Diátaxis), `tech-writer` (editing role, owns no templates) · T3: `onboarding-guide-writer`

Tier check: T1 = 21, T2 = 30, T3 = 14 → 65 lifecycle + 2 meta = 67. ✓

### Overlap boundary rules (in descriptions and bodies)
- [CANDIDATE] `code-reviewer` routes, never duplicates: security → `security-code-reviewer`, perf → `performance-optimizer`, SQL → `sql-optimizer`; namespaces REV-/SEC-/PERF-/SQL-.
- [CANDIDATE] Security triad: threat-modeler (design) · security-requirements-writer (gate) · security-code-reviewer (code).
- [CANDIDATE] Data triad: data-modeler (logical) → db-schema-designer (physical) → sql-optimizer (queries); migrations only in db-migration-planner.
- [CANDIDATE] Story chain: prd-writer → user-story-mapper → epic-story-breakdown → user-story-writer (only the last defines Gherkin/INVEST).
- [CANDIDATE] Sibling descriptions name neighbors; evals include sibling prompts as should-NOT-trigger.

## 4. Quality & testing plan

- [CONFIRMED] (verified: skills-ref exists on PyPI — official spec reference implementation; must be pip-installed and proven in Phase A, else a local validator script replaces it) Format validation per skill.
- [CONFIRMED] (user approved) Per skill: ~20 labeled trigger queries (varied should-trigger + near-miss should-NOT-trigger) + ≥3 output eval cases (with vs without skill).
- [CONFIRMED] (user approved via delegated decision, round 2) Eval runner: Claude Code headless on the build machine as the automated PROXY (its selector differs from Copilot's — labeled as such); the AUTHORITATIVE check is the manual per-skill smoke test in the org's VS Code Copilot Chat; Copilot CLI upgrades to primary runner if it ever becomes available to the user. Eval runtime budgeted in Phase A (~1,300+ invocations per full regression).
- [CONFIRMED] (user approved, round 2) Provisional pass thresholds (trigger TPR, near-miss FPR, output rubric) are set BEFORE the first-5 gate; finalized in Phase A.
- [CANDIDATE] CI (local): frontmatter name/dir match; description ≤500 (library policy) vs ≤1024 (spec) distinguished in errors; forward-slash paths; README/SOURCES/last-verified present; README link/boilerplate check; Windows script-invocation test.

## 5. Build phases & governance

- [CONFIRMED] (user approved; expanded round 2) **Phase 0 — In-org go/no-go gate.** Prove three flows with one throwaway skill: (1) manual copy into a test repo's skill directory triggers in the team's VS Code Copilot Chat; (2) a `gh skill install` flow (or record it as unavailable → manual-only distribution); (3) one Python script invocation (confirm version; check python-pptx/docx permissibility). Hard gate.
- [CANDIDATE] **Phase A — Foundation.** Repo scaffold; AUTHORING-GUIDE (thresholds, voice split, security gate, constraints); PER-HARNESS-SETUP (pinned versions); COMPATIBILITY matrix (URLs/transcripts); template/; root README (catalog, packs, non-goals); CI script; eval harness proven (skills-ref or local validator); rough per-skill effort estimate to reality-test Phase B; pack composition finalized with user; build `skill-creator` + `library-maintainer`.
- [CONFIRMED] (user approved) Governance at launch: the user fills all three roles — script reviewer, source re-verifier, and owner of VERIFICATION-LOG.md (where re-verification results live); revisited at pilot.
- [CONFIRMED] (user approved) **First-5 gate:** skill-creator generates 5 skills; user reviews against the provisional thresholds before mass production.
- [CANDIDATE] **Phase B — Tier 1 (21 skills):** distilled content, SKILL.md, README, references+SOURCES, assets, scripts where needed, evals; validate.
- [CONFIRMED] (user approved; expanded round 2) **Pilot gate:** 2–4 week team pilot measuring usage AND maintenance burden (skills gone stale/broken during pilot). Results decide: Tier 2 authored as planned / re-scoped / trimmed; pilot-conditional Scrum skills kept or cut.
- [CANDIDATE] **Phase C — Tier 2 (30 skills):** conditional on pilot.
- [CONFIRMED] (user approved, round 2) **Tier 3 (14) = named backlog:** catalog entries only; authored on demand.
- [CANDIDATE] Build agents work in parallel subagents per category with a consistency reviewer pass.

## 6. Challenges & Risks

- [CONFIRMED] (both seats, budgets verified) R1 Trigger dilution → packs ≤15/project + description discipline.
- [CONFIRMED] (council) R2 Preview-surface churn (Copilot skills, gh skill preview; org policy) → Phase 0 gate, pinned versions, expect breakage, library-maintainer.
- [CANDIDATE] R3 Staleness → SOURCES manifests + re-verification cadence [OPEN: quarterly proposed] + VERIFICATION-LOG.md.
- [CANDIDATE] R4 Overlap confusion → boundary sentences + near-miss evals.
- [CANDIDATE] R5 Windows/POSIX drift → standards + Windows CI invocation test.
- [CANDIDATE] R6 Content quality → distill from named sources with citations, never model memory alone.
- [CANDIDATE] R7 Scale/consistency (67 skills) → tiers, backlogged Tier 3, first-5 + pilot gates, effort estimate in Phase A, template-driven generation, consistency pass.
- [CONFIRMED] (council; corroborated by GitHub's own warning) R8 Library-as-attack-surface → security gate, pinned installs, named script reviewer.
- [CANDIDATE] R9 Proxy-eval mismatch: descriptions tuned on Claude Code's selector may not transfer perfectly to Copilot's → authoritative manual Copilot smoke tests; revisit if Copilot CLI becomes available.

## 7. Remaining Unknowns

- [OPEN] Phase 0 results: org skills enabled? gh skill works? Python version? pptx/docx libs?
- [OPEN] Re-verification cadence length (quarterly proposed).
- [OPEN] Final eval threshold numbers (provisional before first-5 gate; final in Phase A).
- [OPEN] Copilot-side listing/count limits (undocumented).
- [OPEN] Antigravity paths (community-sourced only).
- [OPEN] Whether Copilot cloud agent honors `user-invocable`/`argument-hint` (VS Code yes; cloud-agent docs silent).
- [OPEN] Exact VS Code stable release date for skills (~Jan 2026, unpinned) — matters only for COMPATIBILITY.md footnote.
- [OPEN] Per-skill effort estimate (produced in Phase A).
- [OPEN] Pack composition (finalized in Phase A).
- [OPEN] Standards versions still unverified: Conventional Commits 1.0.0, SemVer 2.0.0, Keep a Changelog 1.1.0, ISO 25010:2023, PMBOK 7, OpenSLO, CWE Top 25 2025 edition, DORA capabilities state, book editions — verify during authoring of affected skills.

## 8. Assumptions register

- [CONFIRMED] (user approved) Teammates' setups match the user's (VS Code + Copilot Chat; Phase 0 verifies skills actually load in-org).
- [CONFIRMED] (user approved) Scope = the 67-skill inventory with tier gates and Tier-3 backlog as defined in §3/§5.
- [CONFIRMED] (user approved) AI coding agents execute the build phase by phase, with user review at the gates.

---

> **Instructions for the implementing agent:**
> - Keep a file called `implementation-notes.md`. Log decisions as you make them.
> - Log EVERY deviation from this plan under a "Deviations" heading, with a
>   one-line reason.
> - Where the plan is silent and you must improvise, choose the most
>   conservative option and log it.
> - Items tagged `[CANDIDATE]` must be verified before use — log the
>   verification result in `implementation-notes.md`. Items tagged `[OPEN]`
>   must be raised with the user, never guessed.
> - Items tagged `[CONFIRMED] (user approved)` that name a concrete tool,
>   library, API, version, price, product capability, or legal/compliance
>   claim were approved, not verified — verify them before use, like
>   `[CANDIDATE]` items.
