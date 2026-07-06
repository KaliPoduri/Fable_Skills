# Output eval cases (≥3)

Each case is run twice — WITH the skill installed and WITHOUT (raw
assistant) — and scored against the rubric in
docs/AUTHORING-GUIDE.md §Eval thresholds. The skill must beat raw output.

## Case 1

- Prompt: "Write a PRD for adding scheduled report emails to our analytics dashboard. Users have asked to receive their saved dashboards by email daily or weekly. We want it shipped next quarter."
- Input artifacts (if any): none (deliberately thin input).
- Rubric focus: template compliance; completeness; honesty about unknowns.
- Expected qualities: all 11 template sections present with exact headings; header table with owner/status/target release; problem statement free of solution language; measurable goals with matching success-metrics rows; non-goals section non-empty; FRs numbered, prioritized, goal-traced; every NFR category decided or explicitly waived; missing facts (baseline metrics, user research) appear in Open questions rather than invented; next-steps hand-off names user-story-mapper/epic-story-breakdown.

## Case 2

- Prompt: "Turn these notes into a product requirements document: 'Support team drowning in password-reset tickets (about 40% of volume). Want self-service reset. Must work for SSO and non-SSO accounts. Security requires audit logging. Out of scope: changing the SSO provider. Target: Q4.'"
- Input artifacts (if any): the inline notes above.
- Rubric focus: source accuracy (fidelity to input); actionability.
- Expected qualities: 40% ticket-volume figure carried into problem statement and baseline metric; SSO/non-SSO split becomes testable FRs; audit logging lands as a security NFR; "changing SSO provider" appears under out-of-scope/non-goals; no invented stakeholders or metrics; assumptions (e.g., email deliverability, identity-verification method) listed as falsifiable statements or open questions.

## Case 3

- Prompt: "Review and complete this draft PRD — it only has a problem statement and a feature list: [paste of a two-section draft with mixed requirement/implementation statements like 'use Redis for session cache']."
- Input artifacts (if any): a two-section draft PRD with implementation-flavored requirements.
- Rubric focus: template compliance; requirements quality (problem-not-solution rewrite).
- Expected qualities: implementation statements rewritten as outcome requirements (Redis moved to a note/constraint or removed) per requirements-quality.md; missing sections added rather than the draft merely reformatted; feature list regrouped into scenario-anchored, prioritized, goal-traced FRs; a completeness walk-through (each user type through key tasks) reflected in added FRs or open questions.
