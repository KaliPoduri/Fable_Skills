# api-designer

Designs HTTP/REST APIs from a feature description or existing system:
resource model, methods and status codes, versioning, pagination, RFC 9457
error responses, idempotency rules, and an OpenAPI 3.2.0 skeleton.

## Example prompts

- "Design a REST API for our order management service."
- "Write an OpenAPI spec for the endpoints in this module."
- "What error format should our API return, and how should we paginate the list endpoints?"

## Install

Copy this folder into your project's skill directory (see
[docs/PER-HARNESS-SETUP.md](../../docs/PER-HARNESS-SETUP.md) for all
harnesses and current install methods):

| Harness | Path |
|---|---|
| GitHub Copilot (VS Code) | `.agents/skills/api-designer/` |
| Copilot cloud agent | `.github/skills/api-designer/` |
| Claude Code | `.claude/skills/api-designer/` (also reads `.agents/skills/`) |
| Cursor | `.cursor/skills/api-designer/` |
| Codex | `.agents/skills/api-designer/` |

## Notes

- Designs the API contract only. Database and logical data modeling belong
  to `data-modeler`; testable security requirements belong to
  `security-requirements-writer`; design-stage threat analysis belongs to
  `threat-modeler` (all may be future-tier skills).
- No scripts. Fully offline: all normative content is distilled into
  `references/` from the sources listed in `references/SOURCES.md`.
