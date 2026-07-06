# The red-green-refactor loop, distilled

Sources: Kent Beck, *Test-Driven Development: By Example*, 1st ed.,
Addison-Wesley Professional, 2002 (ISBN 978-0321146533) — Preface, Part I
(Money example), Part III (Patterns for Test-Driven Development); Martin
Fowler, "Test Driven Development", martinfowler.com/bliki (updated
2023-12-11). See references/SOURCES.md for verification details.

## The two rules (Beck)

1. Write new code only if an automated test has failed.
2. Eliminate duplication.

Everything else in TDD is consequence: you must design interfaces before
implementations (the test calls code that does not exist yet), you must work
in small steps (each test must fail and pass within minutes), and you must
refactor continuously (rule 2).

## The cycle (Beck, Preface)

- **Red** — write a little test that doesn't work, perhaps doesn't even
  compile at first.
- **Green** — make the test work quickly, committing whatever sins necessary
  in the process.
- **Refactor** — eliminate all the duplication created in merely getting the
  test to work.

Fowler's phrasing of the same loop: write a test for the next bit of
functionality; write functional code until the test passes; refactor both new
and old code to make it well structured. Fowler adds a step zero: write a
test list first, then apply the loop to each item (see
references/test-list-and-bugfix.md).

## RED: fail for the right reason

Before touching production code, run the new test and inspect the failure:

- A compile/parse error because the new function or type does not exist yet
  is a legitimate first red — resolve it with the smallest stub that
  compiles, then re-run to get an assertion failure.
- The failure you accept before going green must be an assertion failure that
  matches the missing behavior. An unrelated exception, a typo failure, or a
  test that unexpectedly passes means the test is wrong or the behavior
  already exists — fix the test or reconsider the list item.
- Record the exact failure message. It is the evidence that the test can
  fail, which is what makes it a meaningful regression guard later.

Write the assertion first, then work backwards to the setup (Beck's "Assert
First" pattern). Use literal, evident data in tests — magic-free inputs whose
expected outputs a reader can verify by inspection ("Evident Data").

## GREEN: the three strategies (Beck, Part III)

| Strategy | What you do | When to use |
|---|---|---|
| Fake It ('Til You Make It) | Return the exact constant the test expects; each later cycle replaces constants with variables/expressions | When the real implementation isn't obvious, when you're stuck, or after a failed Obvious Implementation |
| Obvious Implementation | Type the real implementation directly | Only when it is genuinely a few confident lines; if the test fails anyway, drop back to Fake It |
| Triangulation | Generalize only when a SECOND test with a different example makes the fake impossible | When you don't know the right abstraction; two concrete examples triangulate the general rule |

Beck's gear-shifting advice: Obvious Implementation is high gear; the moment
you get an unexpected red bar, shift down to Fake It and small steps. Speed
matters — green quickly, by any sin, because the refactor step exists to pay
the debt while tests protect you.

Triangulation discipline: after Fake It passes with `return 42`, do NOT
generalize immediately. Either (a) the duplication between the test's
expected value and the faked constant is obvious enough to remove in the
refactor step, or (b) write a second test with different inputs and let its
red bar force the general implementation.

## REFACTOR: only on green

- Refactoring means changing structure without changing behavior; it is only
  safe when the suite is green, and the suite must be re-run after each
  transformation.
- The primary target is the duplication created by going green: constants
  duplicated between test and code, copy-pasted branches, near-identical
  setup. Removing test-vs-code duplication is what turns fakes into real
  implementations.
- Fowler: "the most common way that I hear to screw up TDD is neglecting the
  third step" — refactoring both new and old code is what keeps the codebase
  from becoming tested-but-messy.
- Never add behavior during refactor. If a missing behavior surfaces, add it
  to the test list and start a new red.
- Large restructurings (class extraction across a module, catalog-scale
  work) do not belong inside a cycle — finish green, then hand off to the
  refactoring-expert skill.

## Step size and getting unstuck

- The unit of progress is one green bar. If a cycle stalls twice, the step is
  too big: split the test, fake more, or revert to the last green state.
  Reverting is cheap precisely because cycles are minutes long.
- You are allowed to (and should) vary step size with confidence: big steps
  when bored, tiny steps when uncertain (Beck).
- Keep a strict one-behavior-per-test discipline; a test asserting three
  behaviors gives one bit of information when it fails.

## Common failure modes

| Failure | Why it breaks TDD | Correction |
|---|---|---|
| Writing several tests before any code | Locks in interface guesses; multiple simultaneous reds | One red at a time; the rest live on the test list as prose |
| Never watching the test fail | Test may be vacuous (always-green) | Always run red first; quote the failure |
| Skipping refactor when green | Tested mess accumulates; fakes never become real | Refactor step is mandatory; log "none needed" only when true |
| Generalizing from one example | Speculative abstraction | Triangulate: second example first |
| Weakening an assertion to pass | Silently changes the spec | Never; fix the code or re-scope the test on the list |
| Testing implementation details | Refactors break tests without behavior changes | Test through the public interface you wish existed |

## Benefits to preserve (Fowler)

Writing the test first (a) yields self-testing code — every behavior has an
automatic detector for its regression — and (b) forces thinking about the
interface before the implementation, separating what callers see from how it
works, which is the core design benefit of the practice.
