# Output eval cases (≥3)

Each case is run twice — WITH the skill installed and WITHOUT (raw
assistant) — and scored against the rubric in
docs/AUTHORING-GUIDE.md §Eval thresholds. The skill must beat raw output.

## Case 1

- Prompt: "Break this PRD into epics and stories." plus a one-page PRD for
  a customer support ticketing feature (submit ticket, agent queue,
  canned replies, SLA timers, CSAT survey).
- Input artifacts (if any): the one-page ticketing PRD.
- Rubric focus: template compliance; completeness (all PRD outcomes
  covered by an epic); source accuracy (patterns named correctly).
- Expected qualities: 3–9 outcome-phrased epics; every story candidate a
  one-liner in a table with split pattern and S/M/L hint; no narratives or
  acceptance criteria; Dependencies and Open questions sections present;
  Handoff section pointing to user-story-writer.

## Case 2

- Prompt: "This epic is too big: 'Admins can manage organization members
  (invite, deactivate, change roles, bulk import via CSV, audit history).'
  Split it."
- Input artifacts (if any): none beyond the epic text.
- Rubric focus: actionability (patterns applied correctly); source
  accuracy (CRUD, SPIDR-Data, workflow steps used and labeled).
- Expected qualities: CRUD split for member operations; CSV bulk import
  isolated as a data/interface variation; audit history separate; each
  candidate plausibly Sprint-sized; no horizontal front-end/back-end
  layer split.

## Case 3

- Prompt: "Create a backlog from this feature: multi-currency pricing.
  We don't yet know how FX rates will be sourced."
- Input artifacts (if any): a short feature paragraph noting the FX-rate
  unknown.
- Rubric focus: completeness (uncertainty handled explicitly);
  actionability (spike used as fallback, not default).
- Expected qualities: a timeboxed spike candidate for FX-rate sourcing;
  data-variation split (single currency first); the FX unknown surfaced
  under Open questions rather than silently assumed; sizing hints kept
  relative with a note that Developers own sizing.
