# architecture-doc-writer

Writes a complete software architecture document structured by the arc42
template v9, with C4 model views (context, container, dynamic, deployment)
embedded in the matching sections as offline-rendering Mermaid diagrams.

## Example prompts

- "Write an architecture document for this repository."
- "Document our system architecture using arc42."
- "We're onboarding new devs — create an arc42 doc with diagrams for this service."

## Install

Copy this folder into your project's skill directory (see
[docs/PER-HARNESS-SETUP.md](../../docs/PER-HARNESS-SETUP.md) for all
harnesses and current install methods):

| Harness | Path |
|---|---|
| GitHub Copilot (VS Code) | `.agents/skills/architecture-doc-writer/` |
| Copilot cloud agent | `.github/skills/architecture-doc-writer/` |
| Claude Code | `.claude/skills/architecture-doc-writer/` (also reads `.agents/skills/`) |
| Cursor | `.cursor/skills/architecture-doc-writer/` |
| Codex | `.agents/skills/architecture-doc-writer/` |

## Notes

- A standalone diagram request ("draw a container diagram") is owned by
  **c4-diagrammer** — this skill only embeds diagrams inside a full arc42
  document.
- Recording a single architecture decision is owned by **adr-writer**;
  section 9 of the document links to ADRs, it does not write them.
- No scripts; the skill is pure instructions plus references.
