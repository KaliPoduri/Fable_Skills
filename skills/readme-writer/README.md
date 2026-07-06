# readme-writer

Writes or overhauls a repository README — project summary, quick start,
installation, usage examples, configuration, contributing pointer, and
license note — grounded in what actually exists in the repo.

## Example prompts

- "Write a README for this repository."
- "Our README is out of date — bring it in line with the current code."
- "Improve our README so a new developer can get the app running in five minutes."

## Install

Copy this folder into your project's skill directory (see
[docs/PER-HARNESS-SETUP.md](../../docs/PER-HARNESS-SETUP.md) for all
harnesses and current install methods):

| Harness | Path |
|---|---|
| GitHub Copilot (VS Code) | `.agents/skills/readme-writer/` |
| Copilot cloud agent | `.github/skills/readme-writer/` |
| Claude Code | `.claude/skills/readme-writer/` (also reads `.agents/skills/`) |
| Cursor | `.cursor/skills/readme-writer/` |
| Codex | `.agents/skills/readme-writer/` |

## Notes

- Does NOT write full user guides, tutorials, or how-tos — that is owned
  by `user-guide-writer` (future skill). The README links to those; it
  does not contain them.
- Does NOT edit arbitrary prose or documentation for clarity — that is
  owned by `tech-writer` (future skill).
- No scripts; the skill is instructions + references only.
