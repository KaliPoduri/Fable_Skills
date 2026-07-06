# systematic-debugger

Diagnoses bugs with a hypothesis-driven method: reproduce reliably first,
gather evidence before touching code, test one hypothesis at a time,
binary-search inputs/commits/code paths, and verify the fix kills the
original repro.

## Example prompts

- "Debug this — the export job crashes with a NullPointerException."
- "Why is this test failing on CI but passing locally? Works on my machine."
- "We have an intermittent 500 in checkout, maybe 1 in 20 requests. Help me track it down."

## Install

Copy this folder into your project's skill directory (see
[docs/PER-HARNESS-SETUP.md](../../docs/PER-HARNESS-SETUP.md) for all
harnesses and current install methods):

| Harness | Path |
|---|---|
| GitHub Copilot (VS Code) | `.agents/skills/systematic-debugger/` |
| Copilot cloud agent | `.github/skills/systematic-debugger/` |
| Claude Code | `.claude/skills/systematic-debugger/` (also reads `.agents/skills/`) |
| Cursor | `.cursor/skills/systematic-debugger/` |
| Codex | `.agents/skills/systematic-debugger/` |

## Notes

- This skill stops at a confirmed root cause plus a verified fix. Pinning
  the bug with a failing automated test and building the durable fix is
  owned by `tdd-developer`.
- Reviewing code for general quality, style, or maintainability is owned
  by `code-reviewer` — this skill only chases a concrete failure.
- No scripts; the skill is instructions plus offline references only.
