# release-manager

Runs the release process: SemVer 2.0.0 version decisions, CHANGELOG
updates per Keep a Changelog 1.1.0, annotated git tags, human-readable
release notes, a freeze-verify-tag-publish-announce checklist, and the
hotfix path.

## Example prompts

- "Cut the release — what version should this be and what goes in the
  changelog?"
- "We renamed a public API parameter and fixed two bugs since 1.4.2.
  What's the next version?"
- "Write the release notes for everything merged since the last tag."

## Install

Copy this folder into your project's skill directory (see
[docs/PER-HARNESS-SETUP.md](../../docs/PER-HARNESS-SETUP.md) for all
harnesses and current install methods):

| Harness | Path |
|---|---|
| GitHub Copilot (VS Code) | `.agents/skills/release-manager/` |
| Copilot cloud agent | `.github/skills/release-manager/` |
| Claude Code | `.claude/skills/release-manager/` (also reads `.agents/skills/`) |
| Cursor | `.cursor/skills/release-manager/` |
| Codex | `.agents/skills/release-manager/` |

## Notes

- Does NOT design CI/CD pipelines, stages, or quality gates — that is
  owned by `cicd-pipeline-designer`.
- Does NOT define commit message conventions or branching models — that
  is owned by `git-workflow-expert` (future).
- Never pushes tags or publishes packages on its own; it prepares
  commands and content, then asks for confirmation.
- No scripts; the skill is instructions plus references only.
