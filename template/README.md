# <skill-name>

<What it does, 1–2 sentences. Same meaning as the SKILL.md description.>

## Example prompts

- "<direct trigger prompt>"
- "<indirect/natural prompt>"

## Install

Copy this folder into your project's skill directory (see
[docs/PER-HARNESS-SETUP.md](../../docs/PER-HARNESS-SETUP.md) for all
harnesses and current install methods):

| Harness | Path |
|---|---|
| GitHub Copilot (VS Code) | `.agents/skills/<skill-name>/` |
| Copilot cloud agent | `.github/skills/<skill-name>/` |
| Claude Code | `.claude/skills/<skill-name>/` (also reads `.agents/skills/`) |
| Cursor | `.cursor/skills/<skill-name>/` |
| Codex | `.agents/skills/<skill-name>/` |

## Notes

- <Scope boundary: what this skill deliberately does NOT do, and which
  sibling skill owns it.>
- <Script usage, if any: invocation line, what it needs, what it outputs.>
