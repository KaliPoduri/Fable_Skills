# Output eval cases (≥3)

Each case is run twice — WITH the skill installed and WITHOUT (raw
assistant) — and scored against the rubric in
docs/AUTHORING-GUIDE.md §Eval thresholds. The skill must beat raw output.

## Case 1

- Prompt: "Write a postmortem. Yesterday 14:02-15:37 UTC checkout
  returned 500s for ~40% of requests after a config deploy. On-call
  rolled back at 15:20; full recovery 15:37. Alert fired at 14:31."
- Input artifacts (if any): incident channel excerpt with timestamps,
  deploy record, error-rate graph description.
- Rubric focus: template compliance, completeness.
- Expected qualities: all template headings; impact table with sources;
  timeline with TZ and DETECTED (14:31) / MITIGATED (15:20) / RESOLVED
  (15:37) marked; time-to-detect 29m computed and flagged as a
  detection gap; causes split into trigger (config deploy), enabling
  conditions, failed defenses (no canary/validation); action items
  each with owner, ticket, priority, deadline.

## Case 2

- Prompt: "Rewrite this postmortem draft — it currently says the outage
  happened because Priya skipped the checklist and 'carelessly' pushed
  on a Friday."
- Input artifacts (if any): short blameful draft naming an engineer.
- Rubric focus: source accuracy (blameless principles), actionability.
- Expected qualities: no person named as cause; asks why the system
  allowed a single unchecked push to take down production (missing
  enforcement, no gate, checklist not automated); neutral language
  replaces "carelessly"; action items target automating the checklist
  or gating the deploy, not retraining/punishing the individual; the
  engineer appears at most as "the deploying engineer" in the timeline.

## Case 3

- Prompt: "Incident is closed: a cron job silently failed for 12 days
  before anyone noticed billing exports were missing. Write the RCA
  with action items."
- Input artifacts (if any): brief description; no clean timeline exists.
- Rubric focus: completeness (multi-cause analysis, lucky section),
  actionability.
- Expected qualities: does not invent timestamps — flags timeline gaps
  explicitly; identifies the monitoring failure (manual discovery) as
  itself a trigger for the postmortem per SRE criteria; contributing
  causes include the silent-failure mode AND the alerting gap AND the
  absent data-completeness check (no single root cause); "where we got
  lucky" (e.g., data recoverable) items map to action items; deadlines
  scaled to severity; measurable done-conditions ("alert fires within
  1h of missed export"), no "improve monitoring" vagueness.
