# adr-writer

Writes Architecture Decision Records in MADR 4.0.0 format — one numbered
Markdown file per decision, with context, honestly compared options,
decision outcome, consequences, and the proposed/accepted/deprecated/
superseded status lifecycle.

## Example prompts

- "Write an ADR for choosing PostgreSQL over MongoDB."
- "Record this decision: we're standardizing on Kafka for events."
- "Our caching ADR is obsolete — supersede it with the new approach."

## Install

Copy this folder into your project's skill directory (see
[docs/PER-HARNESS-SETUP.md](../../docs/PER-HARNESS-SETUP.md) for all
harnesses and current install methods):

| Harness | Path |
|---|---|
| GitHub Copilot (VS Code) | `.agents/skills/adr-writer/` |
| Copilot cloud agent | `.github/skills/adr-writer/` |
| Claude Code | `.claude/skills/adr-writer/` (also reads `.agents/skills/`) |
| Cursor | `.cursor/skills/adr-writer/` |
| Codex | `.agents/skills/adr-writer/` |

## Notes

- Documenting the whole architecture (context, building blocks, runtime,
  deployment) is owned by **architecture-doc-writer**; its section 9
  links to the ADRs this skill writes.
- Long-form design proposals meant for discussion and iteration are owned
  by **rfc-writer** (future tier); an ADR records a decision, it does not
  host the debate.
- No scripts; the skill is pure instructions plus references.
