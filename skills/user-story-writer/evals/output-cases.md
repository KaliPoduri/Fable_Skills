# Output eval cases (≥3)

Each case is run twice — WITH the skill installed and WITHOUT (raw
assistant) — and scored against the rubric in
docs/AUTHORING-GUIDE.md §Eval thresholds. The skill must beat raw output.

## Case 1

- Prompt: "Write a user story for password reset with acceptance
  criteria."
- Input artifacts (if any): none.
- Rubric focus: template compliance; source accuracy (INVEST letters and
  Gherkin structure correct).
- Expected qualities: As-a/I-want/so-that narrative with a concrete role
  and real benefit; all six INVEST letters evaluated in the table; 2–5
  Gherkin scenarios with the success path first and at least one failure
  path (expired/invalid token); Then steps observable, no UI mechanics;
  Ready check and Assumptions sections present.

## Case 2

- Prompt: "Is this story INVEST? 'As a user I want the new reporting
  module so that reporting works.' Fix what's wrong."
- Input artifacts (if any): the flawed story text.
- Rubric focus: source accuracy (correct diagnosis per letter);
  actionability (each concern paired with a concrete fix).
- Expected qualities: flags Valuable (vague benefit), Small (module-sized,
  recommend epic-story-breakdown for the split), Testable (nothing
  observable), and weak role ("user"); provides a reworded narrative and
  a largest-valuable-slice suggestion rather than gold-plating criteria.

## Case 3

- Prompt: "Add Gherkin scenarios to this story: 'As a returning customer,
  I want to check out with my saved card, so that I don't re-enter
  details.' Cover declines too."
- Input artifacts (if any): the story narrative.
- Rubric focus: template compliance (Gherkin block well-formed);
  completeness (success + decline paths).
- Expected qualities: valid Feature/Scenario structure; one When per
  scenario; Givens describe state, not click history; a declined-card
  scenario with an observable recovery outcome; no invented business
  rules — unknown decline policies land in Assumptions & open questions.
