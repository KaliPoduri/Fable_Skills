# test-strategist

Produces test strategies and test plans in ISTQB CTFL v4.0.1 vocabulary:
test levels, test types, risk-based prioritization, entry/exit criteria,
environment and test data needs, and an explicit "what we will NOT test"
section with reasons.

## Example prompts

- "Write a test strategy for our payment service."
- "I need a test plan for the v2.0 release."
- "What should we test before shipping this feature, and what can we skip?"

## Install

Copy this folder into your project's skill directory (see
[docs/PER-HARNESS-SETUP.md](../../docs/PER-HARNESS-SETUP.md) for all
harnesses and current install methods):

| Harness | Path |
|---|---|
| GitHub Copilot (VS Code) | `.agents/skills/test-strategist/` |
| Copilot cloud agent | `.github/skills/test-strategist/` |
| Claude Code | `.claude/skills/test-strategist/` (also reads `.agents/skills/`) |
| Cursor | `.cursor/skills/test-strategist/` |
| Codex | `.agents/skills/test-strategist/` |

## Notes

- Planning documents only. Writing the automated test code itself is owned
  by `test-automation-engineer`; the developer red-green loop is owned by
  `tdd-developer` (future skill).
- Deliverables cite ISTQB CTFL Syllabus v4.0.1 (a copyright-only update of
  v4.0 — examinable content unchanged).
- No scripts. Text-only skill; works fully offline.
