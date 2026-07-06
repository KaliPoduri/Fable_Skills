# Output eval cases (≥3)

Each case is run twice — WITH the skill installed and WITHOUT (raw
assistant) — and scored against the rubric in
docs/AUTHORING-GUIDE.md §Eval thresholds. The skill must beat raw output.

## Case 1

- Prompt: "Write automated tests for this function" + a ~40-line pure
  function with branching logic (e.g. shipping-cost calculation with
  weight tiers and a null-input error path).
- Input artifacts (if any): the function source.
- Rubric focus: template compliance, completeness.
- Expected qualities: follows the Automated Tests template with a CASE-n
  design table; all tests at unit layer with rationale; happy path, tier
  boundaries, and error path covered; Arrange-Act-Assert structure;
  behavior-revealing names; no test logic (loops/conditionals); CI
  placement stated.

## Case 2

- Prompt: "Our nightly suite is flaky: TestOrderExport fails about 1 in 5
  runs with a timeout, but only on CI. It calls an async export job and
  then asserts the file exists after sleep(3). TestUserCleanup fails only
  when run after TestUserCreate."
- Input artifacts (if any): the two test snippets.
- Rubric focus: source accuracy (root-cause categories), actionability.
- Expected qualities: follows the Flakiness Diagnosis template; classifies
  TestOrderExport as async behavior (bare sleep) and fixes it with
  poll-with-timeout or a completion handle, NOT a longer sleep or retry;
  classifies TestUserCleanup as isolation/shared state and fixes with
  per-test data or state rebuild; verification plan includes repeated,
  shuffled, and parallel runs; quarantine treated as capped and temporary.

## Case 3

- Prompt: "Set up integration tests for our repository layer (PostgreSQL)
  and tell me what belongs in unit tests vs integration tests vs e2e for
  this service."
- Input artifacts (if any): a repository class outline and one service
  endpoint description.
- Rubric focus: source accuracy (pyramid), actionability.
- Expected qualities: queries/serialization tested at integration layer
  against a real or containerized database with the in-memory tradeoff
  noted; business logic pushed to unit tests; at most a handful of e2e
  journeys recommended; duplicated higher-level coverage explicitly
  removed or rejected; CI placement stated per suite without designing
  the pipeline (routes that to cicd-pipeline-designer).
