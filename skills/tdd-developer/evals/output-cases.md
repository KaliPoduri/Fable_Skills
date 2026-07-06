# Output eval cases (≥3)

Each case is run twice — WITH the skill installed and WITHOUT (raw
assistant) — and scored against the rubric in
docs/AUTHORING-GUIDE.md §Eval thresholds. The skill must beat raw output.

## Case 1

- Prompt: "Implement a `parseDuration` function with TDD: it accepts strings like '2h', '45m', '1h30m' and returns total minutes; invalid input raises an error."
- Input artifacts (if any): an empty project with a working test runner (any mainstream language).
- Rubric focus: template compliance, source accuracy (red-green-refactor discipline), completeness.
- Expected qualities: a written test list before any code covering degenerate, plain, compound, and error cases; each cycle logged RED (with a quoted, observed failure) → GREEN (strategy named: Fake It / Obvious / Triangulation) → REFACTOR; final suite output pasted from a real run; output matches the "TDD Session" template.

## Case 2

- Prompt: "We diagnosed the checkout bug: `applyCoupon` divides before rounding, so totals drift by a cent. Fix it test-first."
- Input artifacts (if any): the faulty function plus its existing (green) test file.
- Rubric focus: actionability, source accuracy (bugfix variant: reproduce-then-fix).
- Expected qualities: a minimal reproduction test written FIRST at the unit level, shown failing with the drift symptom; smallest fix applied; full suite rerun; the reproduction test kept and named as a permanent regression guard; a check for sibling occurrences of the same pattern; no existing assertion weakened.

## Case 3

- Prompt: "Add a 'retry with exponential backoff' option to our HTTP wrapper, test-driven. The clock and the transport are real objects today."
- Input artifacts (if any): the wrapper module and its suite.
- Rubric focus: completeness, actionability (test doubles decision), template compliance.
- Expected qualities: test list includes boundaries (zero retries, max retries, jitter off) and error paths; nondeterministic clock and network replaced by owned-interface doubles with the seam introduced as a refactor step; interaction assertions (mock-style) used only where the interaction is the behavior; commit-per-green-behavior rhythm; deferred items listed explicitly.
