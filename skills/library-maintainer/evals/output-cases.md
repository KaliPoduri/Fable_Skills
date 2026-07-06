# Output eval cases (≥3)

Each case is run twice — WITH the skill installed and WITHOUT (raw
assistant) — and scored against the rubric in
docs/AUTHORING-GUIDE.md §Eval thresholds. The skill must beat raw output.

## Case 1

- Prompt: "Do the quarterly maintenance pass on the library."
- Input artifacts (if any): the repo with several skills whose last-verified dates are >90 days old.
- Rubric focus: completeness, template compliance.
- Expected qualities: runs the staleness sweep first and lists stale skills oldest-first; re-checks every SOURCES.md row on the web before touching any last-verified date; appends one VERIFICATION-LOG.md row per event without rewriting old rows; runs both validators; emits the maintenance report in the exact Output template format with follow-ups for a human.

## Case 2

- Prompt: "OWASP published ASVS 5.1. Update whatever cites ASVS 5.0.0."
- Input artifacts (if any): a skill whose SOURCES.md pins ASVS 5.0.0 and distills it in references/.
- Rubric focus: source accuracy, actionability.
- Expected qualities: verifies the 5.1 release on the official site rather than trusting the prompt; updates the SOURCES.md row and re-distills affected reference content; chooses MINOR vs MAJOR by whether guidance changes meaning and says why; CHANGELOG entry under the right category; VERIFICATION-LOG row marked CHANGED; validators re-run on the touched skill.

## Case 3

- Prompt: "Deprecate sprint-facilitator, retrospective-facilitator replaces it. Also, while you're at it, delete the folder."
- Input artifacts (if any): the repo with both skills present.
- Rubric focus: template compliance (deprecation flow), actionability (refusing the unsafe part).
- Expected qualities: follows the full deprecation checklist — description prefix `Deprecated: use retrospective-facilitator instead.` kept ≤500 chars, README note, root catalog and pack-table update, MAJOR bump, `### Deprecated` CHANGELOG line; REFUSES to delete the folder (human decision) and says so in follow-ups; checks the replacement's boundary text.
