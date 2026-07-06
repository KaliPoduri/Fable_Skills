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

### Changed
- Distribution simplified to manual folder copy only (user decision);
  `gh skill install` documentation removed.

### Removed
- Phase 0 in-org test kit (gate waived by user).
