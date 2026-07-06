# tdd-developer

Implements features and bugfixes with strict test-driven development: a test
list, one failing test at a time, the smallest change to green, and a
mandatory refactor step — following Kent Beck's red-green-refactor loop.

## Example prompts

- "Implement the discount calculator with TDD."
- "Write the failing test first, then make it pass."
- "We found the off-by-one in the pager — pin it with a regression test and fix it test-first."

## Install

Copy this folder into your project's skill directory (see
[docs/PER-HARNESS-SETUP.md](../../docs/PER-HARNESS-SETUP.md) for all
harnesses and current install methods):

| Harness | Path |
|---|---|
| GitHub Copilot (VS Code) | `.agents/skills/tdd-developer/` |
| Copilot cloud agent | `.github/skills/tdd-developer/` |
| Claude Code | `.claude/skills/tdd-developer/` (also reads `.agents/skills/`) |
| Cursor | `.cursor/skills/tdd-developer/` |
| Codex | `.agents/skills/tdd-developer/` |

## Notes

- Behavior-preserving cleanup with no new behavior is NOT this skill's job —
  that belongs to `refactoring-expert` (this skill hands off catalog-scale
  restructurings mid-session too).
- Diagnosing a bug whose cause is unknown belongs to `systematic-debugger`;
  this skill takes over once the cause is known, pinning it with a failing
  test before the fix.
- No scripts. Fully offline: the method is distilled into `references/`;
  URLs in `references/SOURCES.md` are for re-verification only.
