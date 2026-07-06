# Output eval cases (≥3)

Each case is run twice — WITH the skill installed and WITHOUT (raw
assistant) — and scored against the rubric in
docs/AUTHORING-GUIDE.md §Eval thresholds. The skill must beat raw output.

## Case 1

- Prompt: "Security review this handler and fix what you find." with a
  small web handler containing (a) SQL built by f-string from a request
  parameter, (b) the query result rendered into HTML via string
  concatenation, (c) a hardcoded database password.
- Input artifacts (if any): one ~40-line handler file (any web framework).
- Rubric focus: source accuracy (correct CWE-89, CWE-79 IDs and OWASP
  A05:2025 mapping), template compliance (SEC-<n>, severity, location,
  before/after code), completeness (all three seeded flaws found).
- Expected qualities: three findings, each with severity, correct CWE ID,
  vulnerable snippet, and a working fix (parameterized query,
  context-aware encoding, secret moved out of source with the value
  redacted in the report); summary table present; residual-risk section
  names dependency-auditor for the driver library.

## Case 2

- Prompt: "Can users read each other's invoices? Review the authorization
  in this API module." with a module where GET /invoices/{id} fetches by
  id with no ownership check, and a JWT is decoded without signature
  verification.
- Input artifacts (if any): one API module (~60 lines) plus its auth
  middleware.
- Rubric focus: actionability (fix enforces object-level check in the
  right layer), source accuracy (CWE-639/CWE-862 distinction, CWE-347-type
  JWT issue assigned a correct CWE even though outside the Top 25).
- Expected qualities: IDOR finding traced source-to-sink (not a bare
  pattern match); JWT verification finding; fixes shown as corrected
  code; severities justified; no invented findings on the safe routes.

## Case 3

- Prompt: "We got flagged in an audit for logging and error handling.
  Review this service's logging security." with a service that logs full
  request bodies (containing passwords), returns stack traces to clients,
  and has an empty catch around an authorization check.
- Input artifacts (if any): one service file with logger config.
- Rubric focus: completeness (secrets-in-logs, verbose errors, fail-open
  catch all found; A09:2025 and A10:2025 both used), template compliance.
- Expected qualities: findings for CWE-200 exposure and fail-open error
  handling; fixes redact at the logging layer and fail closed; report
  states explicitly that no live-CVE claims are made; checklist honored
  (no secrets echoed back in the report).
