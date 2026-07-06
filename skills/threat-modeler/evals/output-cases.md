# Output eval cases (≥3)

Each case is run twice — WITH the skill installed and WITHOUT (raw
assistant) — and scored against the rubric in
docs/AUTHORING-GUIDE.md §Eval thresholds. The skill must beat raw output.

## Case 1

- Prompt: "Threat model this design: a public web app where users upload
  CSV files, a worker parses them into a shared Postgres, and an admin
  dashboard reads the results. Web app and worker run in the same VPC;
  admins log in over the internet."
- Input artifacts (if any): the description above.
- Rubric focus: template compliance, completeness.
- Expected qualities: follows the Output template headings exactly;
  elements classified into external entities, processes, data stores, data
  flows; at least three trust boundaries identified (internet→web app,
  internet→admin plane, services→DB); Mermaid diagram or structured text
  decomposition; STRIDE applied per element type (all six on processes;
  only T/I/D on flows and stores; S/R on external entities); threat
  register with contiguous TM-<n> IDs, likelihood/impact/risk, and a
  response for every threat; upload parsing (malicious CSV, resource
  exhaustion) and admin spoofing covered.

## Case 2

- Prompt: "Run a STRIDE analysis focused on what changes when we add a
  third-party payment provider callback (webhook) to our existing order
  service."
- Input artifacts (if any): brief existing-system summary provided in the
  prompt.
- Rubric focus: source accuracy (STRIDE-per-element), actionability.
- Expected qualities: models the webhook endpoint as a new entry point and
  the provider as an external entity with a new trust boundary; concrete
  threat statements (actor, action, target, consequence) including webhook
  spoofing/forgery, replay, and DoS on the callback endpoint; mitigations
  named as concrete controls (signature verification, anti-replay
  nonce/timestamp, rate limiting) mapped to the violated property; no
  vague "tampering may occur" entries.

## Case 3

- Prompt: "Here is our architecture description. Give me the threat
  register only, ranked, and tell me which risks you'd accept."
- Input artifacts (if any): a 10-line architecture description with an
  internet-facing API, an internal queue, and a logs bucket.
- Rubric focus: completeness, actionability (risk ranking and response
  discipline).
- Expected qualities: register ordered highest risk first using the
  likelihood x impact matrix; every threat has exactly one primary
  response; Accept appears only on Low-risk rows with a written
  justification; log store tampering modeled as T on the data store;
  assumptions and open questions still listed even though only the
  register was requested.
