# Output eval cases (≥3)

Each case is run twice — WITH the skill installed and WITHOUT (raw
assistant) — and scored against the rubric in
docs/AUTHORING-GUIDE.md §Eval thresholds. The skill must beat raw output.

## Case 1

- Prompt: "Review this code" + a ~80-line diff adding a discount-calculation
  function with an off-by-one in a loop boundary, a vague function name
  (`calc2`), and no tests.
- Input artifacts (if any): the diff (any language).
- Rubric focus: template compliance, completeness, actionability.
- Expected qualities: output follows the Code Review template; the
  off-by-one is a REV-n BLOCKER with file:line and a concrete fix; missing
  tests is MAJOR; naming is MINOR/NIT; verdict is "Request changes";
  at least one specific positive; comments address the code, not the author.

## Case 2

- Prompt: "Review my PR" + a diff that mixes a bug fix with string
  concatenation of user input into a SQL statement and an N+1 query loop.
- Input artifacts (if any): the diff.
- Rubric focus: source accuracy (routing rule), template compliance.
- Expected qualities: the SQL injection appears ONLY as a one-line routed
  observation to security-code-reviewer (SEC-), the N+1 loop as a one-line
  PERF- routing to performance-optimizer, and query shape/index concerns as
  SQL- to sql-optimizer — no in-skill deep security or performance
  analysis; general findings (correctness, tests, naming) still reviewed
  with REV-n IDs.

## Case 3

- Prompt: "Review this diff — it's 1,800 lines touching 14 files across
  two unrelated features."
- Input artifacts (if any): CL description plus representative excerpts.
- Rubric focus: source accuracy (design/altitude first), actionability.
- Expected qualities: recommends splitting the CL before line-level review
  (Google guidance on large CLs); reviews design/altitude of the central
  change first; does not attempt exhaustive line comments on everything;
  verdict and next steps are explicit.
