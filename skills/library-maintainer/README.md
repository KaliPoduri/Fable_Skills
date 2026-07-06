# library-maintainer

Maintains the existing Fable Skills library: staleness sweeps, web
re-verification of every SOURCES.md row (logged in VERIFICATION-LOG.md),
SemVer version bumps with CHANGELOG entries, deprecation flow,
full-library validation runs, and consistency checks (sibling boundaries,
install-table drift, catalog drift).

## Example prompts

- "Re-verify the library sources"
- "Check for stale skills"
- "Bump the version of prd-writer"
- "Deprecate phase0-canary"

## Install

Copy this folder into your project's skill directory (see
[docs/PER-HARNESS-SETUP.md](../../docs/PER-HARNESS-SETUP.md) for all
harnesses and current install methods):

| Harness | Path |
|---|---|
| GitHub Copilot (VS Code) | `.agents/skills/library-maintainer/` |
| Copilot cloud agent | `.github/skills/library-maintainer/` |
| Claude Code | `.claude/skills/library-maintainer/` (also reads `.agents/skills/`) |
| Cursor | `.cursor/skills/library-maintainer/` |
| Codex | `.agents/skills/library-maintainer/` |

## Notes

- **This is a build-machine meta skill.** It is meant to run inside the
  Fable Skills library repo itself, not in consumer projects. The install
  table above exists for form's sake; the skill references repo files
  (VERIFICATION-LOG.md, CHANGELOG.md, tools/validate_skills.py, docs/) by
  repo-relative path and needs the build machine's internet access for
  source re-verification.
- Scope boundary: existing skills ONLY. Creating a brand-new skill is
  owned by `skill-creator`.
- No scripts ship with this skill; it instructs running the repo's
  existing `tools/validate_skills.py` and the `agentskills` CLI from the
  repo `.venv`.
- Deprecation never deletes a folder; removal stays a human decision.
