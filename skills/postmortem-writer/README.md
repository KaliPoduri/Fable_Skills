# postmortem-writer

Writes blameless incident postmortems: quantified impact, a precise
detection-to-mitigation-to-resolution timeline, contributing-causes
analysis (no single-root-cause stories), what went well/badly/lucky,
and action items with owners and severity-scaled deadlines. Based on
the Google SRE Book and SRE Workbook postmortem-culture chapters.

## Example prompts

- "Write a postmortem for yesterday's checkout outage."
- "Turn this incident channel log into an RCA document."
- "Draft the incident retrospective for INC-4211 — we need action items
  with owners."

## Install

Copy this folder into your project's skill directory (see
[docs/PER-HARNESS-SETUP.md](../../docs/PER-HARNESS-SETUP.md) for all
harnesses and current install methods):

| Harness | Path |
|---|---|
| GitHub Copilot (VS Code) | `.agents/skills/postmortem-writer/` |
| Copilot cloud agent | `.github/skills/postmortem-writer/` |
| Claude Code | `.claude/skills/postmortem-writer/` (also reads `.agents/skills/`) |
| Cursor | `.cursor/skills/postmortem-writer/` |
| Codex | `.agents/skills/postmortem-writer/` |

## Notes

- Does NOT manage a live, ongoing incident — that is owned by
  `incident-responder` (future).
- Does NOT write operational runbooks/procedures from the findings —
  that is owned by `runbook-writer` (future).
- Does NOT facilitate sprint/team retrospectives — that is owned by
  `retrospective-facilitator` (future).
- No scripts; the skill is instructions plus references only.
