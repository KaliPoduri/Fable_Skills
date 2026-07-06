# Postmortem culture — distilled from Google SRE

Sources: Google SRE Book, Ch. 15 "Postmortem Culture: Learning from
Failure" (https://sre.google/sre-book/postmortem-culture/) and The Site
Reliability Workbook, Ch. 10, same title
(https://sre.google/workbook/postmortem-culture/). Both verified
2026-07-06.

## When a postmortem is warranted (SRE Book)

Common trigger criteria — any one suffices:

- User-visible downtime or degradation beyond an agreed threshold
- Data loss of any kind
- On-call engineer intervention (rollback, traffic rerouting, etc.)
- Resolution time above an agreed threshold
- A monitoring failure — the incident was discovered manually

Plus: any stakeholder may request a postmortem for any event. Teams
should define these thresholds BEFORE incidents, not during.

## Blamelessness (SRE Book)

Core assumption: everyone involved had good intentions and did the
right thing with the information they had at the time. Therefore:

- Investigate why the system and context made the action reasonable —
  not who acted. Focus on systemic weaknesses.
- If a postmortem punishes, people stop surfacing issues; the
  organization loses its ability to learn. Blameless postmortems are a
  prerequisite for honest timelines.
- Blameless does not mean consequence-free vagueness: name the system
  gap precisely; never name a person as a cause.

## Good vs bad postmortem (SRE Workbook, worked contrast)

The Workbook contrasts two postmortems of the same incident (an
automation bug that erased machine setups globally). The failure modes
to avoid, and their fixes:

| Bad postmortem | Good postmortem |
|---|---|
| Blames an engineer by name for "ignoring" a step | Discusses the system-design gaps that made the mistake possible |
| No quantified impact | Specific numbers: queries lost, latency increase, revenue impact |
| Skips key technical details of the failure chain | Documents the full failure chain |
| Vague action items ("make automation better") | Measurable, ticketed action items with owners |
| Inflammatory language ("which is ridiculous") | Neutral, factual language throughout |
| Diffuse ownership, many owners | Clear accountable owner(s) for the document |
| Shared only within the immediate team | Shared company-wide, with a glossary for outsiders |
| Published four months late | Published within days of incident closure |

## Quality attributes of a good postmortem (SRE Workbook)

- **Clarity** — organized sections, glossary for technical terms, data
  shown with links to its source.
- **Concrete action items** — each with an owner, priority by severity,
  measurable success criteria, and a mix of preventative and mitigative
  work.
- **Blamelessness** — targets system weaknesses; conclusions follow
  from evidence; respectful, objective language.
- **Depth** — impact traced across teams and systems; cause analysis
  goes deep instead of stopping at the first plausible cause; every
  conclusion backed by verifiable data, not assumption.

## Against single-root-cause thinking

Complex systems fail through multiple interacting causes. Structure
cause analysis in three layers instead of hunting one "root cause":

1. **Trigger** — the proximate event (deploy, config change, traffic
   spike, expiry).
2. **Enabling conditions** — what let the trigger become an incident
   (missing validation, silent failure modes, stale runbook, config
   drift, alert gap).
3. **Failed or missing defenses** — each layer that should have caught
   it and did not (tests, canary, review, rate limit, rollback
   automation, monitoring).

A postmortem that fixes only the trigger leaves the enabling conditions
armed for the next, different trigger.

## Review, sharing, and incentives

- Draft collaboratively in a shared doc during/after the incident;
  real-time commenting speeds assembly (SRE Book).
- Formal review by senior engineers before publication, checking:
  completeness of the account, depth of cause analysis, impact
  captured, action plan appropriate (SRE Book).
- Publish within days; share widely (announcements, reading groups,
  postmortem repositories) so other teams learn (Workbook).
- Reward the work: visibly recognize well-written postmortems and
  completed action items; track action-item closeout — unclosed action
  items plus repeat incidents signal cultural breakdown (both).
- Reduce friction with templates and tooling so writing the postmortem
  is cheap (Workbook).
