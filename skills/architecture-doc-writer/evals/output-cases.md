# Output eval cases (≥3)

Each case is run twice — WITH the skill installed and WITHOUT (raw
assistant) — and scored against the rubric in
docs/AUTHORING-GUIDE.md §Eval thresholds. The skill must beat raw output.

## Case 1

- Prompt: "Write an architecture document for this repository." (run in a
  small web app repo: frontend + API + database, docker-compose deploy)
- Input artifacts (if any): the repository itself; no existing docs.
- Rubric focus: template compliance, completeness.
- Expected qualities: all 12 arc42 v9 sections present in order (including
  10.1/10.2 split); ranked quality-goals table with measurable scenarios;
  C4 context diagram in section 3 and container diagram in section 5 as
  Mermaid; every diagram block also described in a blackbox table;
  unknown business facts tagged `[assumption]`, not invented.

## Case 2

- Prompt: "Document our system architecture. Top quality goals are
  availability and auditability; we're constrained to on-prem Kubernetes
  and Java. Existing ADRs live in docs/decisions/."
- Input artifacts (if any): three MADR files in docs/decisions/.
- Rubric focus: source accuracy, actionability.
- Expected qualities: constraints correctly split technical vs
  organizational; section 4 maps availability and auditability to
  concrete approaches; section 9 links the three existing ADRs in a table
  with status instead of restating them; deployment view reflects
  on-prem Kubernetes, not invented cloud services.

## Case 3

- Prompt: "Our architecture doc must stay lightweight — cover the
  essentials for a 2-person team CLI tool."
- Input artifacts (if any): small CLI repo, no external systems except the
  filesystem and one HTTP API.
- Rubric focus: completeness vs tailoring judgment, template compliance.
- Expected qualities: keeps all 12 headings but stubs sections that do
  not apply with a one-line note instead of deleting them; context
  diagram shows the CLI as one box with the HTTP API as external; no
  padded textbook content in section 8; document stays short.
