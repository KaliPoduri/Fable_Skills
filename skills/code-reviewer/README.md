# code-reviewer

General code review of a diff, PR, or file per Google's engineering
practices: correctness, design, readability, naming, comments, tests, and
consistency, with severity-tagged findings (REV-n). Routes security,
performance, and SQL findings to their specialist sibling skills instead
of duplicating them.

## Example prompts

- "Review this code."
- "Can you do a code review of my PR diff before I merge?"
- "Look over these changes and tell me what would block merge."

## Install

Copy this folder into your project's skill directory (see
[docs/PER-HARNESS-SETUP.md](../../docs/PER-HARNESS-SETUP.md) for all
harnesses and current install methods):

| Harness | Path |
|---|---|
| GitHub Copilot (VS Code) | `.agents/skills/code-reviewer/` |
| Copilot cloud agent | `.github/skills/code-reviewer/` |
| Claude Code | `.claude/skills/code-reviewer/` (also reads `.agents/skills/`) |
| Cursor | `.cursor/skills/code-reviewer/` |
| Codex | `.agents/skills/code-reviewer/` |

## Notes

- This skill deliberately does NOT deep-dive specialist areas. It notes
  the observation in one line and hands off: security issues are owned by
  `security-code-reviewer` (SEC- findings), performance issues by
  `performance-optimizer` (future skill, PERF- findings), SQL/query issues
  by `sql-optimizer` (SQL- findings).
- No scripts. Text-only skill; works fully offline.
