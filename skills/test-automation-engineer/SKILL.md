---
name: test-automation-engineer
description: Designs and writes automated tests - test pyramid balance, Arrange-Act-Assert, flaky-test fixes. Use this skill when asked to 'write automated tests', fix 'flaky tests', or set up integration tests. Do not use for test plans; use test-strategist. For CI pipeline/stage design use cicd-pipeline-designer; for test-first red-green development use tdd-developer. Covers naming, test data management, determinism (async waits, shared state, time, ordering), and CI integration points.
metadata:
  version: "1.0.0"
  last-verified: "2026-07-06"
---

# Test Automation Engineer

Design and write automated tests for existing or new code: choose the
right test pyramid layer, structure each test Arrange-Act-Assert, name
tests after behavior, manage test data deliberately, and keep every test
deterministic. Diagnose and fix flaky tests by root cause, not by rerun.
Treat test code as production code. This skill writes and repairs tests;
it does not produce test plans (test-strategist), design CI pipelines
(cicd-pipeline-designer), or drive test-first feature development
(tdd-developer).

## Constraints

Assume no external internet access, no paid tools, and English output.
Never send project code or data to external services.
Match the project's existing test framework and conventions; do not
introduce new frameworks without flagging the tradeoff.
Never "fix" flakiness with retries or longer sleeps; find the root cause.
Never delete or weaken an existing test without explicit approval.

## Workflow

### Writing new tests

1. Understand the subject. Read the code under test, its public interface,
   dependencies, and existing tests. Identify seams where dependencies can
   be substituted.
2. Choose the pyramid layer. Write each test at the LOWEST layer that can
   catch the failure it targets: unit for logic and edge cases, integration
   for serialization, queries, and wiring at boundaries, end-to-end only
   for a few critical user journeys. If a higher-level test duplicates a
   lower-level one, push it down or delete it. Load
   references/test-pyramid.md when deciding layers, ratios, or duplication.
3. List the cases. Happy path, edge cases (empty, null, zero, boundary,
   unicode), error paths, and any observed-bug reproductions. Give each a
   CASE-<n> ID in the design table.
4. Structure every test Arrange-Act-Assert (given-when-then): set up,
   invoke ONE behavior, assert the outcome. One logical assertion focus
   per test; split tests that verify unrelated outcomes.
5. Name tests after behavior, not implementation:
   `<unit>_<scenario>_<expectedOutcome>` or should-style sentences. A
   failing test's name alone must say what broke.
6. Manage test data. Build minimal data per test (builders/factories over
   large shared fixtures); make relevant values explicit in the test and
   irrelevant ones defaulted; never share mutable fixtures across tests.
7. Use test doubles at boundaries. Stub/mock external services and slow
   collaborators in unit tests; hit real (or containerized/in-memory)
   dependencies in integration tests and note fidelity tradeoffs; keep
   contract expectations for external teams explicit.
8. Enforce determinism as you write — see the determinism rules below.
9. Place tests in CI: fast unit suite on every commit; integration suite
   in a later stage; e2e smoke on deploy. Name the intended stage only —
   pipeline design itself belongs to cicd-pipeline-designer.
10. Write clean test code: no logic (loops/conditionals) inside tests,
    no copy-paste walls, production-level care. Deliver per the Output
    template.

### Determinism rules (apply to every test)

- Async: never bare sleep. Poll with timeout, await completion callbacks,
  or use the framework's synchronization primitives.
- Time: never call the system clock directly in tested code paths; inject
  a clock/time provider and control it in tests.
- Isolation: each test creates its own state and cleans up; tests must
  pass in any order and in parallel.
- Randomness: seed it or inject it.
- Resources: close connections, files, and servers in teardown; leaks fail
  later, unrelated tests.

### Fixing flaky tests

1. Reproduce and characterize: how often it fails, error signature,
   alone vs in suite, order dependence, parallel vs serial.
2. Quarantine promptly if it blocks the team — move it to a quarantined
   suite so the main build stays trusted — but cap the quarantine queue
   and schedule the fix; quarantine is a holding pen, not a graveyard.
3. Classify the root cause: lack of isolation (shared state), async
   behavior (sleeps, missing waits), remote services (real external
   calls), time (clock reads, timezone/DST), ordering dependence, or
   resource leaks. Load references/flaky-tests.md for symptoms and
   remedies per category.
4. Fix the cause, verify by running the test repeatedly (e.g. 20-100x,
   including parallel and shuffled order), then release it from
   quarantine. Record the diagnosis in the output table.

## Output template

For new tests:

```markdown
# Automated Tests: <subject>

## Test design
Layer choice and rationale: <unit/integration/e2e and why>
| ID | Case | Layer | Type |
|---|---|---|---|
| CASE-1 | <behavior + condition> | unit | happy path / edge / error |

## Test code
<the tests, in the project's framework and conventions>

## Data and doubles
<builders/fixtures used; what is stubbed/mocked and why; real deps used
in integration tests and their setup>

## CI placement
<which suite/stage each group runs in; expected runtime>

## Notes
<gaps, follow-ups, anything intentionally not covered>
```

For flaky-test work:

```markdown
# Flakiness Diagnosis: <suite or test>

| Test | Symptom | Root cause category | Root cause | Fix |
|---|---|---|---|---|

## Verification
<how the fix was proven: repeat runs, order shuffling, parallel runs>

## Quarantine status
<what remains quarantined, owner, deadline>
```

## References (load on demand)

- `references/SOURCES.md` — source manifest (always present).
- `references/test-pyramid.md` — load when choosing test layers, balancing
  unit/integration/e2e ratios, or removing duplicated coverage.
- `references/flaky-tests.md` — load when diagnosing non-deterministic
  tests or designing quarantine and remediation.

## Checklist

- [ ] Each test sits at the lowest layer that catches its failure; no
      duplicate coverage across layers.
- [ ] Every test is Arrange-Act-Assert with one behavior per test and a
      behavior-revealing name.
- [ ] No bare sleeps, direct clock reads, shared mutable fixtures,
      order dependence, or unseeded randomness.
- [ ] Test data minimal and explicit; doubles only at boundaries.
- [ ] CI placement stated (stage only — no pipeline design here).
- [ ] Flaky fixes verified by repeated/shuffled/parallel runs, not by
      adding retries.
- [ ] Output follows the template above.
