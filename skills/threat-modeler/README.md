# threat-modeler

Builds design-stage threat models: system decomposition (assets, entry
points, trust boundaries), STRIDE-per-element threat enumeration, risk
ranking, and mitigations delivered as a threat model document with a
numbered threat register (TM-1, TM-2, ...).

## Example prompts

- "Threat model this design: a public API gateway in front of three internal services and a shared Postgres."
- "Run a STRIDE analysis on the new file-upload feature."
- "What are the security threats in this architecture before we build it?"

## Install

Copy this folder into your project's skill directory (see
[docs/PER-HARNESS-SETUP.md](../../docs/PER-HARNESS-SETUP.md) for all
harnesses and current install methods):

| Harness | Path |
|---|---|
| GitHub Copilot (VS Code) | `.agents/skills/threat-modeler/` |
| Copilot cloud agent | `.github/skills/threat-modeler/` |
| Claude Code | `.claude/skills/threat-modeler/` (also reads `.agents/skills/`) |
| Cursor | `.cursor/skills/threat-modeler/` |
| Codex | `.agents/skills/threat-modeler/` |

## Notes

- Analyzes DESIGNS, before or independent of code. Reviewing written code
  for vulnerabilities belongs to `security-code-reviewer`; general code
  review belongs to `code-reviewer`; turning threats into testable security
  requirements belongs to `security-requirements-writer` (some are
  future-tier skills).
- No scripts. Fully offline: STRIDE tables, the risk matrix, and process
  guidance are distilled into `references/` from the sources listed in
  `references/SOURCES.md`.
