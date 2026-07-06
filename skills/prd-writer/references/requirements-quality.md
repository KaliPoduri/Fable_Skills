# Requirements quality — writing FRs, NFRs, and release criteria

Distilled from: Marty Cagan (Silicon Valley Product Group), "How To Write a
Good PRD", 2005
(https://www.svpg.com/wp-content/uploads/2024/07/How-To-Write-a-Good-PRD.pdf;
text verified 2026-07-06 via https://archive.org/details/goodprd). Cagan
marks the paper historical; the principles below are the durable parts,
applied inside the lightweight agile structure of prd-structure.md.

## Cagan's four PRD components (orientation)

1. Product purpose — problem statement, target users, big picture,
   scenarios.
2. Features — described at the level of user interaction and use cases,
   each traceable to an objective.
3. Release criteria — the non-functional bar the release must clear.
4. Schedule — context and target timeframe (in this library: the header's
   target release plus links to plans; detailed scheduling belongs to
   delivery tooling, not the PRD).

## Rules for functional requirements

- Problem, not solution. State WHAT the user must be able to accomplish
  and under what conditions — never HOW the system implements it.
  Requirements are not design (Cagan). If design intent matters, link a
  mockup; do not encode it as a requirement.
- Testable. A requirement someone cannot write a pass/fail check for is a
  wish. Force numbers, enumerations, or observable behavior.
- One requirement per statement. "And" joining two capabilities means two
  IDs.
- Traceable. Every FR names the goal it serves. A requirement serving no
  goal is scope creep with an ID.
- Prioritized. Must / Should / Could per requirement. If everything is
  Must, nothing is.
- Scenario-grounded. Cagan: describe features via use cases and
  interaction, not feature-list bullets. Anchor each FR group in a short
  scenario ("A returning customer wants to …").

## Release criteria — the NFR checklist (Cagan)

Cover each category with a measurable requirement or an explicit waiver
("not a constraint for this release", with reason):

| Category | What to pin down |
|---|---|
| Performance | Response/latency targets for the key tasks, under stated load |
| Scalability | Expected volume now and at 12 months; what must not degrade |
| Reliability | Availability target, data-loss tolerance, recovery expectations |
| Usability | Who must succeed at what task without training/help |
| Supportability | Diagnosability, logging, upgrade path, ops handover |
| Localizability | Which locales/languages/formats the release must handle |
| Security & privacy | Access control expectations, data classification, retention (modern addition — Cagan's list predates it; keep it anyway) |

## Assumptions discipline

Cagan step 6: identify and QUESTION your assumptions. For each assumption
ask: if this is false, does the product still make sense? If no, it is a
risk needing validation before or during the release — record it in the
Risks section with a validation action.

## Principles that keep PRDs honest (Cagan)

- Do your homework first: customers, competitors, team capabilities.
  A PRD written without that study is fiction with headings. When the
  homework has not been done, say so in Open questions — do not simulate it.
- Less is more: every added feature costs complexity, support, and focus.
  Prefer cutting a Could over diluting a Must.
- You are not your customer: personal preference is not evidence. Claims
  about users need a source (research, support data, interviews) or an
  Assumptions entry.
- Avoid specials: one-customer features undermine product coherence.
  If a requirement exists only for a single stakeholder, flag it.
- Test completeness (Cagan step 9): walk each user type through each of
  their key tasks using only the requirements. Any step you cannot
  complete reveals a missing FR.
- Prioritize ruthlessly (Cagan step 8): the PRD should make cutting scope
  easy — that is what the priority column is for.

## Cagan's ten-step process (reference)

1. Do your homework. 2. Define the product's purpose. 3. Define user
profiles, goals, tasks. 4. Define product principles. 5. Prototype and
test the concept. 6. Identify and question assumptions. 7. Write it down.
8. Prioritize. 9. Test completeness. 10. Manage the product (keep the PRD
current as decisions land).

Steps 1–6 are the thinking the Workflow's steps 1–6 compress; steps 7–10
map to Workflow 7–12. Steps 5 (prototyping) and 10 (ongoing management)
happen outside this skill — note them as next steps where relevant.
