# skill-creator

Creates a new skill for the Fable Skills library end to end: scope and
sibling boundaries, template copy, description per the authoring formula,
web-verified sources, distilled references, evals, both validators, a
CHANGELOG entry, and a hard stop for human review.

## Example prompts

- "Create a new skill for SQL query optimization"
- "Add a skill for postmortem writing to the library"
- "Author the adr-writer skill from the catalog"

## Install

Copy this folder into your project's skill directory (see
[docs/PER-HARNESS-SETUP.md](../../docs/PER-HARNESS-SETUP.md) for all
harnesses and current install methods):

| Harness | Path |
|---|---|
| GitHub Copilot (VS Code) | `.agents/skills/skill-creator/` |
| Copilot cloud agent | `.github/skills/skill-creator/` |
| Claude Code | `.claude/skills/skill-creator/` (also reads `.agents/skills/`) |
| Cursor | `.cursor/skills/skill-creator/` |
| Codex | `.agents/skills/skill-creator/` |

## Notes

- **This is a build-machine meta skill.** It is meant to run inside the
  Fable Skills library repo itself, not in consumer projects. The install
  table above exists for form's sake; installing this skill elsewhere is
  pointless — it references repo files (template/, docs/AUTHORING-GUIDE.md,
  tools/validate_skills.py) by repo-relative path and needs the build
  machine's internet access for source verification.
- Scope boundary: creating brand-new skills ONLY. Updating, re-verifying,
  version-bumping, or deprecating existing skills is owned by
  `library-maintainer`.
- No scripts ship with this skill; it instructs running the repo's
  existing `tools/validate_skills.py` and the `agentskills` CLI from the
  repo `.venv`.
- Every skill it produces stops at a human review gate before rollout
  (security policy R8).
