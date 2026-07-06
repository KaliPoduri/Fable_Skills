# refactoring-expert

Improves existing code without changing its observable behavior: maps code
smells to named refactorings from Fowler's catalog and applies them as small,
test-protected mechanical steps with a commit per refactoring.

## Example prompts

- "Refactor this class — it's doing too much."
- "This function is 300 lines long; break it up without changing behavior."
- "Remove the duplication between these two modules safely."

## Install

Copy this folder into your project's skill directory (see
[docs/PER-HARNESS-SETUP.md](../../docs/PER-HARNESS-SETUP.md) for all
harnesses and current install methods):

| Harness | Path |
|---|---|
| GitHub Copilot (VS Code) | `.agents/skills/refactoring-expert/` |
| Copilot cloud agent | `.github/skills/refactoring-expert/` |
| Claude Code | `.claude/skills/refactoring-expert/` (also reads `.agents/skills/`) |
| Cursor | `.cursor/skills/refactoring-expert/` |
| Codex | `.agents/skills/refactoring-expert/` |

## Notes

- Adding NEW behavior (features, bug fixes) is NOT this skill's job — that
  belongs to `tdd-developer`. Bugs discovered while refactoring are reported
  and routed, never silently fixed.
- Performance-motivated changes belong to `performance-optimizer` (future
  tier): they need measurement, not smell-driven transformation.
- Style-only lint fixes (formatting, quote style, import order) are not
  refactoring; the skill says so and points to the project's formatter.
- No scripts. Fully offline: the smell catalog and mechanics are distilled
  into `references/`; URLs in `references/SOURCES.md` are for
  re-verification only.
