---
name: user-story-writer
description: "Writes and refines one user story: narrative, INVEST check, Gherkin acceptance criteria. Use this skill when writing a user story, adding acceptance criteria, or checking INVEST. Do not use to split an epic; use epic-story-breakdown instead. Covers role-goal-benefit format, Given/When/Then scenarios, and a definition-of-ready check. Do not use to write the upstream requirements doc; use prd-writer instead."
metadata:
  version: "1.0.0"
  last-verified: "2026-07-06"
---

# User Story Writer

Write or refine a single user story to the point where it is ready for
Sprint Planning: role–goal–benefit narrative, INVEST quality check, Gherkin
Given/When/Then acceptance criteria, and a definition-of-ready sanity
check. This skill owns INVEST and Gherkin for the library. It works on ONE
story at a time — breaking a feature, PRD, or epic into many stories is
owned by the sibling skill `epic-story-breakdown` (its one-liner candidates
are this skill's typical input); the upstream requirements document is
owned by `prd-writer`.

## Constraints

Assume no external internet access, no paid tools, and English output.
Never send project code or data to external services.
Scrum is assumed (story readiness targets Sprint Planning); where Kanban
differs, note it inline.
Stay technology-agnostic: express behavior from the user's point of view,
never as implementation tasks.
A story is a placeholder for a conversation — keep it negotiable; do not
gold-plate criteria beyond what the request states.

## Workflow

1. Ingest the input: a one-liner story candidate (typically from
   `epic-story-breakdown`), a rough story, or a plain-language request.
   If the input is a whole feature or epic that needs decomposing first,
   stop and point to `epic-story-breakdown`.
2. Identify role, goal, and benefit. The role is a concrete user type
   (not "user" if the input allows better; never the system). The benefit
   must answer "why would they want this?" — if it is missing from the
   input, propose one and flag it as an assumption.
3. Draft the narrative in the standard form:
   `As a <role>, I want <goal>, so that <benefit>.`
   Keep the goal solution-free: what the user needs, not how it is built.
4. Run the INVEST check. Load `references/invest.md` and evaluate all six
   letters — Independent, Negotiable, Valuable, Estimable, Small,
   Testable. For each letter record PASS or a one-line concern plus a
   concrete fix (reword, split suggestion, missing information).
5. If the Small check fails badly (story clearly exceeds one Sprint),
   recommend `epic-story-breakdown` for the split instead of forcing
   oversized criteria — then continue with the largest valuable slice if
   the user wants.
6. Write Gherkin acceptance criteria. Load `references/gherkin.md`.
   Produce 2–5 scenarios: the main success path first, then key
   variations and failure paths. Rules:
   - One behavior per scenario; Given = context, When = one action,
     Then = observable outcome.
   - Third person, declarative, no UI mechanics ("When the customer
     submits the order", not "When the user clicks the green button").
   - Use `Scenario Outline` + `Examples` only when the same steps repeat
     over a data table.
7. Run the definition-of-ready sanity check (see Output template): story
   has narrative + criteria, fits a Sprint, dependencies known, and is
   testable as written. This is a sanity list, not a formal gate — the
   Scrum Guide's actual bar is "can be Done within one Sprint". (Kanban:
   replace "fits one Sprint" with "flows within target cycle time".)
8. Present the result in the Output template. List every assumption made;
   never silently invent domain rules.
9. Run the Checklist below before presenting the result.

## Output template

Produce exactly this structure:

````markdown
# User story: <short title>

## Story
As a <role>, I want <goal>, so that <benefit>.

## INVEST check
| Letter | Verdict | Note / fix |
|---|---|---|
| Independent | PASS/CONCERN | <one line> |
| Negotiable | PASS/CONCERN | <one line> |
| Valuable | PASS/CONCERN | <one line> |
| Estimable | PASS/CONCERN | <one line> |
| Small | PASS/CONCERN | <one line> |
| Testable | PASS/CONCERN | <one line> |

## Acceptance criteria (Gherkin)
```gherkin
Feature: <capability this story belongs to>

  Scenario: <main success path>
    Given <context>
    When <action>
    Then <observable outcome>

  Scenario: <variation or failure path>
    ...
```

## Ready check
- [ ] Narrative and acceptance criteria complete
- [ ] Small enough to be Done within one Sprint
- [ ] Dependencies known (list or "none")
- [ ] Testable as written

## Assumptions & open questions
- <Anything proposed rather than stated in the input.>
````

### Filled micro-example (style anchor)

For the candidate "Customer edits their own review":

```markdown
## Story
As a returning customer, I want to edit a review I posted, so that my
review stays accurate after my opinion changes.

## Acceptance criteria (Gherkin)
Feature: Review editing

  Scenario: Customer updates their own review
    Given the customer has a published review on a product
    When the customer saves changed review text
    Then the product page shows the updated text
    And the review is marked as edited

  Scenario: Customer cannot edit someone else's review
    Given a review published by a different customer
    When the customer attempts to edit that review
    Then the edit is refused
```

Note the style: concrete role, benefit that answers "why", one When per
scenario, outcomes observable, no button-clicking mechanics.

## References (load on demand)

- `references/SOURCES.md` — source manifest (always present).
- `references/invest.md` — load in step 4, whenever checking or fixing
  story quality against INVEST.
- `references/gherkin.md` — load in step 6, whenever writing or reviewing
  Given/When/Then acceptance criteria.

## Checklist

- [ ] Exactly one story processed (whole-feature input redirected to
      epic-story-breakdown).
- [ ] Narrative names a concrete role and a real benefit; goal is
      solution-free.
- [ ] All six INVEST letters evaluated, each concern paired with a fix.
- [ ] 2–5 Gherkin scenarios: success path first, one behavior each,
      outcomes observable.
- [ ] Assumptions listed; nothing invented silently.
- [ ] Output follows the template above.
