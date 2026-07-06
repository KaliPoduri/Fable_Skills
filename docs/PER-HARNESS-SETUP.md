# PER-HARNESS-SETUP.md — installing Fable skills

Master setup guide. Per-skill READMEs link here for the common steps and
only carry the quick-install table. See COMPATIBILITY.md for the full
support matrix and evidence.

**Install method: copy the skill folder into your project.** That is the
whole mechanism — no CLI tools, no package manager.

**Keep ≤15 skills installed per project.** Installing everything dilutes
skill selection on every known harness (Codex and Claude Code have hard
listing budgets; Copilot's is undocumented). Install a pack (see root
README) plus at most a few singles.

## Known-good versions (pinned at last verification, 2026-07-06)

| Tool | Version | Note |
|---|---|---|
| Python (build machine) | 3.13.7 | validation tooling only — skills ship no scripts |
| skills-ref / agentskills CLI | 0.1.1 | build machine only, format validation |

## Install (all harnesses)

1. Pick the skill folder from this repo's `skills/`.
2. Copy the WHOLE folder (SKILL.md alone is not enough — references,
   assets, scripts, evals travel with it) into your project's skill
   directory from the table below.
3. Reload the editor/agent (VS Code: `Developer: Reload Window`).
4. Smoke-test: ask the agent something the skill's description clearly
   covers; confirm it triggers.

| Harness | Project path | Notes |
|---|---|---|
| GitHub Copilot (VS Code Chat) | `.agents/skills/<name>/` | our primary surface |
| GitHub Copilot (cloud agent) | `.github/skills/<name>/` | for repo-level agents |
| Claude Code | `.claude/skills/<name>/` or `.agents/skills/<name>/` | |
| Cursor | `.cursor/skills/<name>/` | `.claude/skills/` legacy-compat |
| Codex | `.agents/skills/<name>/` | |
| Antigravity | `.agents/skills/<name>/` (project) | [CANDIDATE] community-sourced; global `~/.gemini/config/skills/`; verify locally |

## Updating / removing

- Update: re-copy the folder from a newer library version; check
  CHANGELOG.md for breaking changes.
- Remove: delete the skill folder from the project skill directory.

## Troubleshooting

- Skill never triggers: confirm the folder landed under the correct path
  for YOUR harness (table above), reload the window, then try the exact
  trigger phrasing from the skill's README example prompts.
- Triggers but ignores references/scripts: the folder was copied
  partially — re-copy the whole folder.
