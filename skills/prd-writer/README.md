# prd-writer

Writes a Product Requirements Document (PRD) for a feature or product:
problem statement, goals/non-goals, target users, scope, functional and
non-functional requirements, success metrics, risks, and open questions.

## Example prompts

- "Write a PRD for the new bulk-export feature."
- "We need a product requirements document for the SSO rollout — here are my notes."
- "Turn this feature brief into a proper requirements doc."

## Install

Copy this folder into your project's skill directory (see
[docs/PER-HARNESS-SETUP.md](../../docs/PER-HARNESS-SETUP.md) for all
harnesses and current install methods):

| Harness | Path |
|---|---|
| GitHub Copilot (VS Code) | `.agents/skills/prd-writer/` |
| Copilot cloud agent | `.github/skills/prd-writer/` |
| Claude Code | `.claude/skills/prd-writer/` (also reads `.agents/skills/`) |
| Cursor | `.cursor/skills/prd-writer/` |
| Codex | `.agents/skills/prd-writer/` |

## Notes

- Does NOT decompose requirements into epics or user stories — that is
  owned by `epic-story-breakdown` (with `user-story-mapper` and
  `user-story-writer` downstream).
- Does NOT write product vision or roadmap documents — those are owned by
  `product-vision-writer` and `product-roadmap-writer` (future skills).
- Top of the story chain: prd-writer → user-story-mapper →
  epic-story-breakdown → user-story-writer.
- No scripts; the skill is instructions + references only.
