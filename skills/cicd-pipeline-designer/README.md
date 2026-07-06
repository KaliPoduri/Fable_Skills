# cicd-pipeline-designer

Designs CI/CD pipelines end to end: stage layout (build, test tiers,
security checks, artifact, deploy), quality gates with failure policy,
caching, artifact versioning, and a DORA capabilities/metrics alignment
check. Output is a design document plus a platform-agnostic YAML sketch
with GitHub Actions, GitLab CI, and Jenkins notes.

## Example prompts

- "Design our CI/CD pipeline for this repo."
- "What pipeline stages and quality gates should we have for CI?"
- "Our builds are slow and deploys are flaky — propose a better pipeline
  with caching and gates."

## Install

Copy this folder into your project's skill directory (see
[docs/PER-HARNESS-SETUP.md](../../docs/PER-HARNESS-SETUP.md) for all
harnesses and current install methods):

| Harness | Path |
|---|---|
| GitHub Copilot (VS Code) | `.agents/skills/cicd-pipeline-designer/` |
| Copilot cloud agent | `.github/skills/cicd-pipeline-designer/` |
| Claude Code | `.claude/skills/cicd-pipeline-designer/` (also reads `.agents/skills/`) |
| Cursor | `.cursor/skills/cicd-pipeline-designer/` |
| Codex | `.agents/skills/cicd-pipeline-designer/` |

## Notes

- Does NOT design progressive rollout mechanics (canary, blue-green,
  feature-flag ramps) — that is owned by `deployment-strategist` (future).
- Does NOT cut or version releases (changelog, tags, release notes) —
  that is owned by `release-manager`.
- Does NOT choose a branching model — that is owned by
  `git-workflow-expert` (future).
- No scripts; the skill is instructions plus references only.
