# epic-story-breakdown

Decomposes a PRD, feature description, or oversized epic into an epic list
and a backlog of one-liner story candidates, using SPIDR and other proven
splitting patterns, with dependency notes and relative sizing hints.

## Example prompts

- "Break this PRD into epics and stories."
- "This epic is way too big — split it into something we can put in a sprint."
- "Create a backlog from the attached feature description."

## Install

Copy this folder into your project's skill directory (see
[docs/PER-HARNESS-SETUP.md](../../docs/PER-HARNESS-SETUP.md) for all
harnesses and current install methods):

| Harness | Path |
|---|---|
| GitHub Copilot (VS Code) | `.agents/skills/epic-story-breakdown/` |
| Copilot cloud agent | `.github/skills/epic-story-breakdown/` |
| Claude Code | `.claude/skills/epic-story-breakdown/` (also reads `.agents/skills/`) |
| Cursor | `.cursor/skills/epic-story-breakdown/` |
| Codex | `.agents/skills/epic-story-breakdown/` |

## Notes

- Produces story candidates as one-liners only. Writing or refining an
  individual story — narrative, INVEST check, Gherkin acceptance criteria —
  is owned by the sibling skill `user-story-writer`; this skill's Handoff
  section points there.
- Authoring the upstream requirements document is owned by `prd-writer`;
  this skill consumes that document, it does not write it.
- No scripts.
