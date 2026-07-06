# security-code-reviewer

Reviews written code for security vulnerabilities against OWASP Top
10:2025, OWASP ASVS 5.0.0, and the 2025 CWE Top 25, producing SEC-numbered
findings with severity, CWE ID, the vulnerable pattern, and a concrete fix.

## Example prompts

- "Do a security review of src/api/auth before we merge."
- "Check this handler for SQL injection and XSS."
- "I think we have hardcoded secrets in the config loader — find and fix
  anything security-relevant in that module."

## Install

Copy this folder into your project's skill directory (see
[docs/PER-HARNESS-SETUP.md](../../docs/PER-HARNESS-SETUP.md) for all
harnesses and current install methods):

| Harness | Path |
|---|---|
| GitHub Copilot (VS Code) | `.agents/skills/security-code-reviewer/` |
| Copilot cloud agent | `.github/skills/security-code-reviewer/` |
| Claude Code | `.claude/skills/security-code-reviewer/` (also reads `.agents/skills/`) |
| Cursor | `.cursor/skills/security-code-reviewer/` |
| Codex | `.agents/skills/security-code-reviewer/` |

## Notes

- Design-stage threat analysis (STRIDE, data-flow diagrams, "what could go
  wrong before code exists") is owned by **threat-modeler**.
- General, non-security code review (readability, correctness, style) is
  owned by **code-reviewer**.
- Third-party dependency CVEs are owned by **dependency-auditor** (future
  tier). This skill runs offline and CANNOT confirm live CVEs.
- LLM-application-specific issues (prompt injection, model output
  handling) are owned by **llm-app-security-reviewer** (future tier).
- The OWASP Code Review Guide (2017) is treated as historical context
  only and is never cited as current guidance.
- No scripts; the skill is instructions + offline reference files only.
