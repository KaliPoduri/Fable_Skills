# user-story-writer

Writes and refines individual user stories: role–goal–benefit narrative,
INVEST quality check, Gherkin Given/When/Then acceptance criteria, and a
definition-of-ready sanity check.

## Example prompts

- "Write a user story for password reset with acceptance criteria."
- "Is this story INVEST? 'As an admin I want to export logs so that I can audit access.'"
- "Add Gherkin scenarios to the checkout story."

## Install

Copy this folder into your project's skill directory (see
[docs/PER-HARNESS-SETUP.md](../../docs/PER-HARNESS-SETUP.md) for all
harnesses and current install methods):

| Harness | Path |
|---|---|
| GitHub Copilot (VS Code) | `.agents/skills/user-story-writer/` |
| Copilot cloud agent | `.github/skills/user-story-writer/` |
| Claude Code | `.claude/skills/user-story-writer/` (also reads `.agents/skills/`) |
| Cursor | `.cursor/skills/user-story-writer/` |
| Codex | `.agents/skills/user-story-writer/` |

## Notes

- Works on ONE story at a time. Breaking a PRD, feature, or epic into many
  stories is owned by the sibling skill `epic-story-breakdown`; its
  one-liner story candidates are this skill's typical input.
- Authoring the upstream requirements document is owned by `prd-writer`.
- This skill owns INVEST and Gherkin for the library — other skills defer
  here rather than restating them.
- No scripts.
