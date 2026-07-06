# COMPATIBILITY.md — Agent Skills support matrix

Status legend: **[CONFIRMED]** = official docs or command transcript (basis
noted) · **[CANDIDATE]** = community-sourced, verify before relying on it ·
**[OPEN]** = unknown. All of this is a preview-era surface (risk R2):
expect churn, re-verify on breakage, pin versions in PER-HARNESS-SETUP.md.

Verified dates are when the source was last checked, not release dates.

## Skill discovery paths (project-level)

| Surface | Path | Status | Basis | Verified |
|---|---|---|---|---|
| GitHub Copilot — VS Code Chat | `.agents/skills/` | [CONFIRMED] | gh manual (install default); github.blog 2025-12-18 | 2026-07-06 |
| GitHub Copilot — cloud agent | `.github/skills/` | [CONFIRMED] | GitHub cloud-agent docs | 2026-07-06 |
| Claude Code | `.claude/skills/`; also reads `.agents/skills/` | [CONFIRMED] | Anthropic docs | 2026-07-06 |
| Codex | `.agents/skills/` | [CONFIRMED] | developers.openai.com | 2026-07-06 |
| Cursor | `.cursor/skills/` primary; `.claude/skills/` legacy-compat | [CONFIRMED] | cursor.com/docs/skills | 2026-07-06 |
| Antigravity | project `.agents/skills/`; global `~/.gemini/config/skills/`; `~/.agents/skills/` NOT read | [CANDIDATE] | community-sourced only | 2026-07-06 |

## Frontmatter field support

Spec rule: unknown fields are ignored — extra fields are safe everywhere
but only WORK where listed. (Spec: agentskills.io/specification.)

| Field | Copilot VS Code | Copilot cloud agent | Claude Code | Codex | Cursor | Status |
|---|---|---|---|---|---|---|
| `name`, `description` | yes | yes | yes | yes | yes | [CONFIRMED] spec core |
| `metadata` (string map) | ignored-safe | ignored-safe | yes | ignored-safe | ignored-safe | [CONFIRMED] spec |
| `argument-hint` | yes (VS Code docs) | [OPEN] docs silent | yes | [OPEN] | [OPEN] | mixed |
| `user-invocable` | yes (VS Code docs) | [OPEN] docs silent | yes | [OPEN] | [OPEN] | mixed |
| `disable-model-invocation` | yes (VS Code docs) | [OPEN] docs silent | yes | [OPEN] | [OPEN] | mixed |
| `context` (forked execution) | experimental (VS Code docs) | [OPEN] | n/a | n/a | n/a | [CANDIDATE] — do not depend on it |

## Limits that shape our authoring rules

| Surface | Limit | Status | Basis |
|---|---|---|---|
| Spec | description ≤1024 (Codex counts BYTES); name ≤64 lowercase-hyphen | [CONFIRMED] | agentskills.io spec |
| Codex | skill listing budget: 2% of context, 8k-token fallback | [CONFIRMED] | developers.openai.com |
| Claude Code | configurable per-description cap; ~1% listing budget, least-used dropped first | [CONFIRMED] | Anthropic docs (corrected in council round 2) |
| Copilot | listing/count limits UNDOCUMENTED | [OPEN] | — hence packs ≤15 skills/project |

## Distribution

| Mechanism | Status | Notes |
|---|---|---|
| Manual folder copy | [CONFIRMED] default | works everywhere; documented per skill |
| `gh skill install <owner>/Fable_Skills <skill>[@tag]` | [CONFIRMED] syntax (gh manual); [OPEN] in-org availability | public preview, needs gh ≥2.90.0; auto-discovers `skills/*/SKILL.md`; installs to `.agents/skills/`; **pending Phase 0** |

## Timeline footnotes

- Copilot Agent Skills GA'd in waves: github.blog changelog 2025-12-18;
  VS Code stable ~Jan 2026 — exact date unpinned [OPEN].
- `gh skill` CLI public preview since Apr 2026.
