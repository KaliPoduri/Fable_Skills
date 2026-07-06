# The test pyramid — distilled

Source: Ham Vocke, "The Practical Test Pyramid", martinfowler.com,
2018-02-26 (https://martinfowler.com/articles/practical-test-pyramid.html).
Distilled for offline use — do not fetch the URL at runtime.

## The shape and why it holds

Write tests with different granularity; the more high-level you get, the
FEWER tests you should have:

1. **Unit tests** (base, many) — fast, isolated, cheap to write and run.
2. **Service/integration tests** (middle, fewer) — test integration with
   parts that live outside the process: databases, filesystems, network
   calls to other services.
3. **UI / end-to-end tests** (top, very few) — test the fully integrated
   system as a user would; slowest, most brittle, most expensive to
   maintain and diagnose.

Rationale: as you move up, tests get slower, harder to write, more
brittle, and failures get harder to localize. A failed unit test points at
the broken unit; a failed e2e test points at "somewhere in the system".
The anti-pattern is the **ice-cream cone** (many e2e, few unit tests):
slow builds, vague failures, high maintenance.

Two rules of thumb: (1) write tests with different granularity; (2) if a
test at a higher level catches the same failure a lower-level test already
catches, the higher-level one is redundant.

## Unit tests

- Test one unit (function/method/class) with external collaborators
  replaced by test doubles where they make tests slow or nondeterministic.
  Sociable (real in-process collaborators) vs solitary (all doubled) —
  both are fine; pick per case.
- Test the PUBLIC interface, not private internals. Coupling tests to
  implementation structure makes every refactoring break tests; test
  observable behavior ("if I put in x, do I get back y") instead.
- Cover happy path plus edge cases; don't chase 100% coverage as a goal —
  coverage is a byproduct of testing the behaviors that matter.
- Structure: **Arrange, Act, Assert** (given/when/then) — set up, invoke
  one thing, assert the outcome.

## Integration tests

- Test the serialization/deserialization and wiring at every boundary the
  app has: database queries actually run against a database, filesystem
  reads hit files, HTTP clients hit a stubbed server.
- Prefer running the real dependency locally (container) or a close
  substitute (in-memory DB) — note that in-memory substitutes may differ
  from production engines; when behavior diverges, test against the real
  engine.
- For calls to OTHER TEAMS' services, use a test double for speed and
  determinism, then keep the double honest with **contract tests**
  (consumer-driven contracts: the consumer publishes its expectations;
  the provider runs them in its own build).
- Integration tests are slower than unit tests: write them for every
  place the app serializes or crosses a process boundary, not for every
  logic branch (logic branches belong in unit tests).

## UI and end-to-end tests

- UI tests (does the interface behave: input accepted, state rendered)
  need not be end-to-end: behavior/JS logic can be unit-tested; visual
  regressions caught with focused tools.
- End-to-end tests are the most brittle: browser quirks, timing, animations,
  popups. Keep only a **handful** for the highest-value user journeys
  (e.g. search, checkout) and push everything else down the pyramid.
- If the app has an API, subcutaneous tests (against the API just below
  the UI) give most of the confidence at far less brittleness.

## Avoiding duplication and keeping the suite honest

- Test code is as important as production code — refactor it, keep it
  readable, give it the same care.
- Delete redundant higher-level tests; keep the pyramid slim at the top.
- If a higher-level test adds no confidence beyond existing lower-level
  tests, it only adds runtime and maintenance cost.
- A test suite you don't trust or that takes too long gets ignored or
  skipped — speed and determinism are features of the suite.

## Clean test code rules

- One assertion focus per test ("one logical concept").
- Arrange-Act-Assert structure, visible at a glance.
- No logic in tests (no loops/conditionals computing expectations) — a
  test with logic needs its own tests.
- Don't over-DRY tests: some duplication is fine if it keeps each test
  readable in isolation; extract builders/helpers for SETUP, not for
  assertions.
- Make relevant input values explicit in the test; hide irrelevant setup
  behind helpers/builders.

## CI placement (deployment pipeline integration)

- Run fast unit tests in the earliest pipeline stage on every commit for
  quick feedback.
- Run integration tests in a subsequent stage; long-running e2e/smoke
  suites in later stages or on deploy.
- The later a stage, the fewer and slower the tests — the pipeline mirrors
  the pyramid. (Pipeline/stage design itself: see cicd-pipeline-designer.)
