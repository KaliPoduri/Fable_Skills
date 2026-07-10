# Fable Skills

A private library of AI-agent skills covering the software engineering
lifecycle end to end — artifact skills (PRDs, design docs, stories, decks)
and expert-role skills (code reviewer, security scanner, SQL optimizer,
architect). Agent Skills open standard (`SKILL.md` folders); primary
harness: GitHub Copilot Chat in VS Code; also works in Claude Code, Codex,
Cursor (and, community-verified, Antigravity).

**Status: Tier 1 authored.** All 21 Tier 1 skills plus the 2 meta skills
are authored, source-verified, and validator-clean under `skills/`
(everything marked T1 or Meta below). Tier 2 (30) and the Tier 3 backlog
(14) are catalog-only for now. The Spark ETL suite (3 skills, PLAN.md v5)
is authored version-adaptive; its in-org acceptance gates (M0–M3) are
pending.

## Install

Copy a whole skill folder into your project's skill directory
(Copilot VS Code: `.agents/skills/<name>/`) and reload the editor. That is
the entire mechanism. Full steps + all harnesses:
[docs/PER-HARNESS-SETUP.md](docs/PER-HARNESS-SETUP.md).

**Install a pack, not the whole library** — keep ≤15 skills per project;
more dilutes skill triggering on every known harness.

## Packs (draft — [OPEN] composition to be finalized)

| Pack | For | Skills (draft) |
|---|---|---|
| `discovery` | product shaping | prd-writer, product-vision-writer, product-roadmap-writer, user-story-mapper, persona-writer |
| `agile-delivery` | sprint work | epic-story-breakdown, user-story-writer, agile-estimator, backlog-refiner, project-status-reporter |
| `build` | design + implementation | architecture-doc-writer, adr-writer, api-designer, tdd-developer, refactoring-expert, systematic-debugger, git-workflow-expert |
| `quality-security` | review gates | code-reviewer, security-code-reviewer, threat-modeler, test-strategist, test-automation-engineer, dependency-auditor |
| `data` | data work | data-modeler, db-schema-designer, sql-optimizer, db-migration-planner |
| `ops-docs` | ship + run + document | cicd-pipeline-designer, release-manager, postmortem-writer, runbook-writer, readme-writer, tech-writer |
| `spark-etl` | Spark/ETL dev teams | etl-knowledge-builder, etl-assistant, spark-performance-advisor, sql-optimizer, systematic-debugger |

## Catalog — 70 skills (65 lifecycle + 2 meta + 3 Spark ETL)

Tier 1 (21) authored first · Tier 2 (30) after the pilot gate · Tier 3
(14) named backlog, authored on demand · `*` = pilot-conditional.

### Meta (2)
`skill-creator` · `library-maintainer`

### Spark ETL suite (3 — authored, in-org gates pending)
`etl-knowledge-builder` (KB generation, agent mode) ·
`etl-assistant` (failed-job RCA, explain-flow, static improvements) ·
`spark-performance-advisor` (slow-job tuning from runtime evidence)

### Product & Discovery (6)
T1: `prd-writer` · T2: `product-vision-writer`, `product-roadmap-writer`, `user-story-mapper`, `ux-design-reviewer` · T3: `persona-writer`

### Agile Process — Scrum (7)
T1: `epic-story-breakdown`, `user-story-writer` · T2: `agile-estimator`, `backlog-refiner`, `sprint-facilitator`*, `retrospective-facilitator`* · T3: `definition-of-done-writer`

### Architecture & Design (10)
T1: `architecture-doc-writer`, `c4-diagrammer`, `adr-writer`, `api-designer`, `threat-modeler` · T2: `rfc-writer`, `data-modeler`, `design-reviewer` · T3: `tech-spike-planner`, `legacy-migration-planner`

### Implementation (6)
T1: `tdd-developer`, `refactoring-expert`, `systematic-debugger`, `git-workflow-expert` · T3: `coding-standards-writer`, `code-documenter`

### Quality & Testing (7)
T1: `code-reviewer`, `test-strategist`, `test-automation-engineer` · T2: `performance-tester`, `performance-optimizer`, `accessibility-auditor` · T3: `ai-evals-designer`

### Security & Compliance (6)
T1: `security-code-reviewer` · T2: `security-requirements-writer`, `dependency-auditor`, `secrets-hygiene-auditor`, `compliance-privacy-reviewer` · T3: `llm-app-security-reviewer`

### Data & Databases (4)
T1: `sql-optimizer` · T2: `db-schema-designer`, `db-migration-planner` · T3: `data-governance-advisor`

### Delivery & Operations (10)
T1: `cicd-pipeline-designer`, `release-manager`, `postmortem-writer` · T2: `deployment-strategist`, `observability-engineer`, `slo-designer`, `incident-responder`, `runbook-writer` · T3: `iac-reviewer`, `dora-metrics-analyst`

### Management & Communication (5)
T2: `project-status-reporter`, `slide-deck-builder`, `risk-register-writer` · T3: `meeting-notes-writer`*, `estimation-doc-writer`

### Documentation (4)
T1: `readme-writer` · T2: `user-guide-writer`, `tech-writer` · T3: `onboarding-guide-writer`

## Non-goals (deliberate, may become future candidates)

Frontend implementation specifics · mobile development ·
cloud-provider-specific guidance · support operations ·
procurement/change management.

## Repo guide

| Path | What |
|---|---|
| `PLAN.md` | authoritative plan — Spark ETL suite (v5); library plan archived at `archive/2026-06-skills-library-plan/` |
| `docs/AUTHORING-GUIDE.md` | binding standards for every skill |
| `docs/PER-HARNESS-SETUP.md` | install per harness |
| `docs/COMPATIBILITY.md` | support matrix + evidence |
| `template/` | blank scaffold for new skills |
| `tools/validate_skills.py` | library-policy CI validator |
| `VERIFICATION-LOG.md` | source re-verification governance |

Validation (build machine): `python tools/validate_skills.py --run-scripts`
plus `agentskills validate skills/<name>` (from `.venv`).
