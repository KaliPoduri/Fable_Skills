# git-workflow-expert

Guides day-to-day Git discipline: Conventional Commits v1.0.0 messages,
branch strategy selection (trunk-based vs feature vs release branches),
PR hygiene, rebase-vs-merge decisions, .gitignore discipline, and safe
undo recipes (revert over reset on shared history).

## Example prompts

- "Write a commit message for this change — it adds OAuth login and removes the old session endpoint."
- "What branching strategy should our 6-person team use? We deploy weekly."
- "I need to undo the last two commits but they're already pushed to main."

## Install

Copy this folder into your project's skill directory (see
[docs/PER-HARNESS-SETUP.md](../../docs/PER-HARNESS-SETUP.md) for all
harnesses and current install methods):

| Harness | Path |
|---|---|
| GitHub Copilot (VS Code) | `.agents/skills/git-workflow-expert/` |
| Copilot cloud agent | `.github/skills/git-workflow-expert/` |
| Claude Code | `.claude/skills/git-workflow-expert/` (also reads `.agents/skills/`) |
| Cursor | `.cursor/skills/git-workflow-expert/` |
| Codex | `.agents/skills/git-workflow-expert/` |

## Notes

- Version numbers, CHANGELOG entries, and release tagging are owned by
  `release-manager` — this skill stops at commit/branch/PR discipline.
- CI pipeline and workflow design is owned by `cicd-pipeline-designer`;
  this skill only assumes "CI must be green before merge".
- No scripts; the skill is instructions plus offline references only.
