# Test lists, bugfix TDD, and test doubles

Sources: Kent Beck, *Test-Driven Development: By Example*, 1st ed.,
Addison-Wesley Professional, 2002 (ISBN 978-0321146533) — "Test List",
"Test-First", "Assert First", "Evident Data", "Child Test", "Mock Object",
"Broken Test", "Clean Check-in", and the Part III patterns; Martin Fowler,
"Test Driven Development", martinfowler.com/bliki (updated 2023-12-11). See
references/SOURCES.md.

## The test list (Beck: "Test List")

Before starting, write down every test you know you'll need — on the
deliverable itself, not in your head:

- One entry per behavior, phrased as a checkable sentence
  ("empty cart totals to zero", "reject password shorter than 12").
- Include the null/degenerate case, the plain cases, the boundaries, the
  error cases, and refactorings you already know are coming.
- The list is the scope contract: when it is empty and duplication is gone,
  the task is done. Work not on the list is scope creep — add it to the list
  or decline it.

Mid-loop discipline: when a new case occurs to you while coding, ADD IT TO
THE LIST and keep going. Never abandon a red bar to chase a new idea. Beck's
rule of thumb: interruptions of interruptions go no deeper than two levels.

## Ordering the list

Pick next the test that (a) teaches you something and (b) you are confident
you can make pass quickly:

- Brand-new unit → start with a degenerate case (empty input, zero, one
  element). It forces the interface into existence with trivial logic —
  "Starter Test": pick a test that teaches something about the design but
  that you can make work fast.
- Existing unit, new behavior → the simplest variant of the new behavior.
- Uncertain design → the test whose interface you most need to see written
  down; writing the call site IS the design act ("Test-First").
- Use "Child Test": if a test turns out too big to go green in minutes,
  comment it out or park it, write a smaller test that represents a piece of
  the broken case, get that passing, then reinstate the big one.

## One behavior per test

- Each test asserts one behavior; name it after the behavior, not the method
  under test.
- Structure: setup → action → assertion. Write the assertion first and build
  backwards ("Assert First").
- Use inline, literal data whose relationship to the expected output is
  visible in the test itself ("Evident Data"). Avoid shared mutable fixtures
  that couple tests together — tests must pass in any order, independently.

## Bugfix TDD: pin the cause with a test

Precondition: the CAUSE is known. Diagnosing an unknown failure is the
systematic-debugger skill's job; this skill takes over after diagnosis.

1. Write the smallest test that reproduces the bug at the lowest level that
   can express it — prefer a unit test on the faulty function over an
   end-to-end test, because it fails faster and localizes better. Where the
   report arrives as a broken end-to-end scenario, keep that as a second,
   outer test if the project's suite supports it.
2. Run it; confirm it fails with the bug's actual symptom (wrong value,
   exception). Quote the failure.
3. Fix with the smallest change that makes the test pass; run the full suite.
4. The reproduction test remains in the suite permanently as a regression
   guard. Note in the session output which test pins which bug.
5. Then look around: does the same faulty pattern exist elsewhere? Each
   sibling occurrence gets its own list entry and cycle.

If an existing test was already failing when you arrived (Beck's "Broken
Test" is a deliberate device for solo work-resumption, not an excuse):
never "fix" it by editing its assertions to match current behavior without
explicit confirmation that the spec changed.

## Fake it vs make it real: dependencies and doubles

Default: use the real collaborator. Reach for a double only when the real
thing is slow, nondeterministic, unavailable offline, or has side effects
(clock, network, filesystem, database, randomness).

- **Fake constant inside your own unit** — normal Fake It; erased by
  triangulation or refactor within a few cycles.
- **Stub/fake collaborator** — a hand-rolled in-memory implementation of the
  dependency's interface (e.g. in-memory repository). Prefer this for state.
- **Mock Object** (Beck, Part III) — a double that also asserts how it was
  called. Use sparingly, only when the interaction IS the behavior under
  test (e.g. "sends exactly one notification"); over-mocking couples tests
  to implementation.
- Doubles must sit behind an interface the production code owns. If you
  cannot substitute the dependency, that is a design smell the test just
  exposed — introduce the seam as the refactor step of a cycle.
- Never let a double drift from the real contract silently: keep at least
  one integration-level test (or contract test) that exercises the real
  collaborator where the environment allows it.

## Commit rhythm and when to stop

- Commit on green, after the refactor step, one behavior per commit
  ("Clean Check-in": check in only when all tests pass).
- Stop when: the test list is empty; the suite is green; no duplication you
  know of remains; and every deferred item is written down with a reason.
- Do NOT stop at "it works on the happy path" — the boundaries and error
  cases on the list are part of the behavior.

## Test quality self-check

Ask of each test before ticking the list:
- Would it fail if the behavior regressed? (It failed once — you watched.)
- Can a reader tell what behavior it specifies from name + assertion alone?
- Does it survive refactoring of internals without edits?
- Does it run fast enough to run with the whole suite every cycle?
