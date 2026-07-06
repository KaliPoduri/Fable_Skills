---
name: postmortem-writer
description: "Writes blameless incident postmortems: impact, timeline, causes, action items with owners. Use this skill when asked to write a postmortem, incident retrospective, or RCA document. Do not use for live incident response; use incident-responder. Not for runbooks (runbook-writer) or sprint retros (retrospective-facilitator)."
metadata:
  version: "1.0.0"
  last-verified: "2026-07-06"
---

# Postmortem Writer

Write a blameless postmortem for an incident that is already resolved:
quantify the impact, reconstruct a precise detection-to-resolution
timeline, analyze contributing causes without stopping at a single root
cause, capture what went well/badly/where the team got lucky, and turn
findings into owned, deadlined action items. Grounded in the Google SRE
Book (Chapter 15) and SRE Workbook (Chapter 10) postmortem-culture
chapters.

## Constraints

Assume no external internet access, no paid tools, and English output.
Never send project code or data to external services.
Blameless is non-negotiable: never name a person as a cause; write about
systems, tooling, and process. People appear only as neutral role
actors in the timeline (e.g., "the on-call engineer").
Use factual, neutral language — no sarcasm, no "obviously", no
"ridiculous", no speculation presented as fact. Label anything
unconfirmed as such.
The incident is over. Live incident command belongs to
incident-responder; turning findings into operational procedures
belongs to runbook-writer; team process retros belong to
retrospective-facilitator.

## Workflow

1. **Confirm a postmortem is warranted and collect inputs.** Typical
   triggers: user-visible downtime or degradation beyond threshold, any
   data loss, on-call intervention (rollback, traffic rerouting),
   resolution time over threshold, monitoring gap discovered manually —
   or any stakeholder asked for one. Gather: incident channel/ticket
   logs, alert timestamps, deploy/change records, dashboards or metric
   snapshots, and the names of systems (not people) involved.
2. **Quantify impact.** Numbers, not adjectives: duration, users or
   percentage of traffic affected, failed requests, data lost or
   delayed, revenue or SLO/error-budget consumption if measurable, and
   support ticket volume. State the measurement source for each figure;
   mark estimates as estimates.
3. **Reconstruct the timeline.** Ordered timestamped entries (with
   timezone) from first causal event through detection, escalation,
   mitigation, and full resolution. Every entry: timestamp, factual
   event, source (alert, log, chat, deploy record). Mark the three
   pivots explicitly: DETECTED, MITIGATED, RESOLVED. Compute
   time-to-detect and time-to-mitigate. Flag gaps where nothing is
   known rather than smoothing over them.
4. **Analyze contributing causes.** Avoid single-root-cause thinking:
   real incidents come from multiple interacting causes. Work through
   trigger (what set it off), enabling conditions (what allowed it to
   propagate — missing validation, absent alerts, config drift), and
   defenses that failed or were absent (tests, canaries, rate limits,
   review). For each cause, ask why the system made the action
   reasonable — everyone involved had good intentions and acted on the
   information they had. Load `references/postmortem-culture.md` for
   blameless framing and the good-vs-bad worked contrast.
5. **Capture lessons.** Three lists: what went well (defenses and
   responses that worked — keep them funded), what went badly (gaps
   this incident proved), where we got lucky (harm avoided by chance —
   treat each as a near-miss defect to fix, not a comfort).
6. **Write action items.** Each: concrete verb-first description, a
   single named owner (a person or team accepting it — ownership is not
   blame), a tracking ticket, priority, and a deadline scaled to
   severity — as a default: critical ≤ 2 weeks, high ≤ 1 month,
   medium ≤ 1 quarter (adjust to org policy and say so). Balance
   prevention, detection, and mitigation items; include a measurable
   done-condition per item. "Make X better" is not an action item.
7. **Assemble the document** with the output template below. Include a
   glossary if it will be shared beyond the owning team.
8. **Share and review.** Route the draft through senior-engineer review
   (completeness, cause depth, actionable items) before broad sharing;
   then share widely — postmortems only pay for themselves when others
   can learn from them. Aim to publish within days, not months. Add a
   review-status line to the doc header.
9. **Hand off boundaries.** Live incident being managed right now →
   incident-responder. "Turn this into an operational procedure" →
   runbook-writer. "Run our sprint retro" → retrospective-facilitator.

## Output template

```markdown
# Postmortem: <incident title> (<incident id/date>)

Status: <draft | in review | reviewed & published>
Owners: <postmortem authors (role/team)>
Reviewed by: <reviewer roles> | Date published: <YYYY-MM-DD>

## Summary
<3-5 sentences: what broke, blast radius, duration, how it was
resolved. Readable by someone outside the team.>

## Impact
| Measure | Value | Source |
|---|---|---|
| Duration | | |
| Users/traffic affected | | |
| Requests failed / data affected | | |
| SLO / error budget consumed | | |

## Timeline (all times <TZ>)
| Time | Event | Source |
|---|---|---|
| | <first causal event> | |
| | **DETECTED** — <how> | |
| | **MITIGATED** — <how> | |
| | **RESOLVED** — <how> | |

Time to detect: <N> · Time to mitigate: <N> · Time to resolve: <N>

## Contributing causes
### Trigger
### Enabling conditions
### Failed or missing defenses

## What went well
## What went badly
## Where we got lucky

## Action items
| # | Action | Type (prevent/detect/mitigate) | Owner | Ticket | Priority | Due |
|---|---|---|---|---|---|---|

## Glossary
<only if shared beyond the owning team>
```

## References (load on demand)

- `references/SOURCES.md` — source manifest (always present).
- `references/postmortem-culture.md` — load when analyzing causes,
  wording anything that could read as blame (steps 4–6), or when the
  user questions why the doc is blameless; contains the SRE good-vs-bad
  postmortem contrast and review/sharing practices.

## Checklist

- [ ] No person named or implied as a cause anywhere; roles only in the
      timeline; language neutral and factual throughout.
- [ ] Impact is quantified with sources; estimates labeled.
- [ ] Timeline timestamps carry a timezone; DETECTED/MITIGATED/RESOLVED
      marked; time-to-detect and time-to-mitigate computed.
- [ ] More than one contributing cause examined (trigger, enabling
      conditions, failed defenses) — no single-root-cause story.
- [ ] "Where we got lucky" items each map to an action item or an
      explicit accepted risk.
- [ ] Every action item has owner, ticket, priority, deadline, and a
      measurable done-condition.
- [ ] Review step and sharing plan stated; publish target within days.
- [ ] Output follows the template above.
