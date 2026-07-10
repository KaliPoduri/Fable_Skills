# Changelog

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions
are git tags per release (see PLAN.md §2.2). Nothing released yet.

## [Unreleased]

### Added
- Repo scaffold: docs/, skills/, template/, tools/ (Phase A foundation).
- CI validator `tools/validate_skills.py` (library policy; spec validation
  via the `agentskills` CLI from skills-ref 0.1.1).
- All 21 Tier 1 skills, authored and source-verified: prd-writer,
  readme-writer, epic-story-breakdown, user-story-writer,
  architecture-doc-writer, c4-diagrammer, adr-writer, api-designer,
  threat-modeler, tdd-developer, refactoring-expert, systematic-debugger,
  git-workflow-expert, code-reviewer, test-strategist,
  test-automation-engineer, security-code-reviewer, sql-optimizer,
  cicd-pipeline-designer, release-manager, postmortem-writer.
- Both meta skills: skill-creator, library-maintainer.
- Spark ETL assistant suite (PLAN.md v5, M1–M3 authoring):
  etl-knowledge-builder, etl-assistant, spark-performance-advisor —
  authored version-adaptive (Spark 3.0–3.5, exact minor version required
  at intake); in-org acceptance gates (M0 spike, M1 experiment, M2 owner
  sampling, M3 incident set) remain pending.

### Changed
- Distribution simplified to manual folder copy only (user decision);
  `gh skill install` documentation removed.
- Routing hardening for the Spark suite (PLAN v5 §2/R9): sql-optimizer and
  systematic-debugger descriptions gained Spark-suite boundary lines and a
  cross-trigger near-miss eval case each.

### Removed
- Phase 0 in-org test kit (gate waived by user).
