# test-automation-engineer

Designs and writes automated tests: test pyramid balance (unit vs
integration vs end-to-end), Arrange-Act-Assert structure, behavior-based
naming, test data management, and determinism — including root-cause
diagnosis and repair of flaky tests.

## Example prompts

- "Write automated tests for this order-processing module."
- "Our tests are flaky — they pass locally and fail in CI. Fix them."
- "Help me set up integration tests for the repository layer."

## Install

Copy this folder into your project's skill directory (see
[docs/PER-HARNESS-SETUP.md](../../docs/PER-HARNESS-SETUP.md) for all
harnesses and current install methods):

| Harness | Path |
|---|---|
| GitHub Copilot (VS Code) | `.agents/skills/test-automation-engineer/` |
| Copilot cloud agent | `.github/skills/test-automation-engineer/` |
| Claude Code | `.claude/skills/test-automation-engineer/` (also reads `.agents/skills/`) |
| Cursor | `.cursor/skills/test-automation-engineer/` |
| Codex | `.agents/skills/test-automation-engineer/` |

## Notes

- Strategy and plan documents are owned by `test-strategist`; CI
  pipeline/stage design by `cicd-pipeline-designer`; test-first (red-green)
  feature development by `tdd-developer`. This skill writes and repairs
  the tests themselves.
- No scripts. Text-only skill; works fully offline.
