# Output eval cases (≥3)

Each case is run twice — WITH the skill installed and WITHOUT (raw
assistant) — and scored against the rubric in
docs/AUTHORING-GUIDE.md §Eval thresholds. The skill must beat raw output.

## Case 1

- Prompt: "Write a test strategy for our online checkout feature (cart,
  payment via third-party gateway, order confirmation email). Team of 2
  testers, 3 weeks before release."
- Input artifacts (if any): the feature description above.
- Rubric focus: template compliance, source accuracy (ISTQB terms).
- Expected qualities: follows the Test Strategy template; risks tabled as
  RISK-n with likelihood x impact; payment/gateway risks rated highest and
  covered by system integration testing; levels and types use ISTQB CTFL
  v4.0.1 names; entry/exit criteria measurable; syllabus cited in Sources.

## Case 2

- Prompt: "What should we test for the v3 migration of our reporting
  database, and what can we safely skip? We cannot test everything."
- Input artifacts (if any): none (assumptions must be stated).
- Rubric focus: completeness, actionability.
- Expected qualities: explicit assumptions section; risk-based
  prioritization drives the ordering; a populated "Out of scope" table
  where every exclusion has a reason and a residual-risk owner; cuts are
  by lowest risk, not lowest effort; no test code produced.

## Case 3

- Prompt: "I need a test plan for the mobile app 2.0 release — include
  entry/exit criteria, environments, and test data needs. We follow
  two-week sprints."
- Input artifacts (if any): none.
- Rubric focus: template compliance, source accuracy (iterative SDLC
  handling).
- Expected qualities: notes that in an iterative SDLC all test levels can
  occur within each iteration; entry/exit criteria per level as a table;
  environments and test data section covers ownership, privacy handling
  (anonymized/synthetic data), and reset strategy; confirmation and
  regression testing placed explicitly.
