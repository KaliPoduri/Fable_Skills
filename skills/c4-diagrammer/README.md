# c4-diagrammer

Produces C4 model diagrams (system context, container, component, dynamic,
and system landscape) as Mermaid text blocks that render offline in VS Code
and GitHub, with C4 notation discipline enforced.

## Example prompts

- "Draw a C4 container diagram of our system."
- "Give me a context diagram for the order service."
- "Diagram this architecture — who talks to what?"

## Install

Copy this folder into your project's skill directory (see
[docs/PER-HARNESS-SETUP.md](../../docs/PER-HARNESS-SETUP.md) for all
harnesses and current install methods):

| Harness | Path |
|---|---|
| GitHub Copilot (VS Code) | `.agents/skills/c4-diagrammer/` |
| Copilot cloud agent | `.github/skills/c4-diagrammer/` |
| Claude Code | `.claude/skills/c4-diagrammer/` (also reads `.agents/skills/`) |
| Cursor | `.cursor/skills/c4-diagrammer/` |
| Codex | `.agents/skills/c4-diagrammer/` |

## Notes

- A full architecture document (arc42, all sections) is owned by
  **architecture-doc-writer** — this skill delivers diagrams only.
- Data/ER diagrams and schema modeling are owned by **data-modeler**
  (future tier); this skill draws structure and interactions, not
  entities and relations.
- Mermaid's C4 syntax is experimental upstream; the skill always offers a
  stable flowchart-based fallback with the same conventions.
- No scripts; the skill is pure instructions plus references.
