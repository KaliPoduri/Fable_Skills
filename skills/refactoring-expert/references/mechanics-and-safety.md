# Mechanics and safety: how to refactor without breaking anything

Source: Martin Fowler, *Refactoring: Improving the Design of Existing Code*,
2nd edition, Addison-Wesley Professional, 2018 (ISBN 978-0134757599) —
Chapters 1–2 (principles, two hats, tests-first), Chapter 4 (building tests),
and the per-refactoring "Mechanics" sections; online catalog:
https://refactoring.com/catalog/. See references/SOURCES.md.

## Definitions (Fowler, ch. 2)

- Refactoring (noun): a change made to the internal structure of software to
  make it easier to understand and cheaper to modify WITHOUT changing its
  observable behavior.
- Refactoring (verb): restructuring software by applying a series of such
  refactorings without changing observable behavior.
- Consequence: if the code is broken for more than a few minutes, or the
  external behavior changed, whatever you did was not refactoring.

## The two hats (Kent Beck, via Fowler ch. 2)

Software work alternates between two activities you must never mix:

- **Adding function** — new capability, new tests; don't touch structure.
- **Refactoring** — restructure only; add no capability, and don't add
  tests (except to pin behavior you discovered was untested).

Swap hats as often as needed, but know which one you wear, and keep each
commit single-hatted. When a refactoring reveals a bug: report it, pin it on
the follow-up list, and let the fix be its own behavior-change commit
(tdd-developer's job) — do not fold it silently into the refactoring.

## Precondition: a solid test suite

"Before you start refactoring, make sure you have a solid suite of tests.
These tests must be self-checking." (Fowler, ch. 2/4.) Concretely:

1. Identify every entry point whose behavior the planned transformations
   could alter.
2. Run the suite; note what covers those entry points. Green baseline is
   mandatory — never refactor on red.
3. Where coverage is missing, write **characterization tests**: tests that
   assert what the code CURRENTLY does, watched to pass, including odd or
   suspicious behavior. Their purpose is change detection, not spec
   approval. Mark suspicious behavior in the report as a possible bug —
   with the odd expected value pinned — rather than "fixing" it mid-flight.
4. Risk-proportional depth: a rename needs less scaffolding than splitting
   a 400-line function with hidden state. When in doubt, add the test.

## Small steps and the rhythm

- Each named refactoring's mechanics decompose it into steps so small they
  feel ignorable; the payoff is that nothing is ever broken long, and when
  a test fails you know it was the LAST small step — revert it, don't debug
  forward through a broken transformation.
- Compile/run tests at every point the mechanics say to test. Shorten, never
  lengthen, the interval when the code is unfamiliar or the step surprising.
- Prefer automated IDE refactorings (rename, extract, inline, change
  signature, move) when available — then still run the tests.
- Commit after each named refactoring lands green; message = refactoring
  name + subject ("Extract Function: computeBaseCharge"). Squash trivial
  rename batches if the project prefers, but never bundle a refactoring
  commit with a behavior change.

## Mechanics for the core refactorings (condensed from the catalog)

**Extract Function** (formerly Extract Method)
1. Create a new function named for WHAT it does, not how.
2. Copy the fragment into it.
3. Pass any local variables the fragment reads as parameters; if it writes
   exactly one local, make that the return value. Many written locals →
   first apply Split Variable or Replace Temp with Query, or reconsider the
   fragment boundary.
4. Replace the original fragment with a call. Compile, test, commit.
5. Look for other occurrences of the same fragment and replace them too.

**Inline Function** (reverse; for Lazy Element, Middle Man)
1. Check the function isn't polymorphic (overridden anywhere).
2. Find all callers; replace each call with the body, one caller at a time,
   testing after each.
3. Remove the now-unused definition. Test, commit.

**Change Function Declaration** (rename / change parameters)
1. Simple path: change declaration and all callers in one motion (safe for
   small reach; automated rename does this).
2. Migration path (wide reach / published API): create the new declaration
   as a forwarding wrapper around the old (or vice versa); move callers over
   one at a time, testing; finally inline/remove the old name. Deprecate
   instead of delete when external callers exist.

**Move Function**
1. Examine everything the function uses in its current context; decide what
   moves with it.
2. Copy it into the target context; adjust to fit (new home's data access).
3. Turn the original into a delegating call to the new one. Test.
4. Migrate callers to the new location, then remove the delegator (Inline
   Function on the stub). Test, commit.

**Encapsulate Variable** (gateway to all data moves)
1. Write getter/setter (or accessor functions) for the variable.
2. Replace each direct read/write with the accessors, testing as you go.
3. Restrict visibility of the raw variable; test, commit.
4. Now the accessors are a seam for further change (validation, moving the
   data, making it immutable).

**Extract Class** (Large Class, Data Clumps)
1. Create the new class for the split-off responsibility; link it from the
   old (field reference).
2. Use Move Field for each relevant field, one at a time, testing each.
3. Use Move Function for the methods, lowest-level (least-dependent) first,
   testing each.
4. Trim both interfaces; decide whether to expose the new object. Commit.

**Replace Conditional with Polymorphism** (Repeated Switches)
1. If classes for the variants don't exist, create them with a factory that
   returns the right subclass/strategy for each type code.
2. Move the conditional logic into the superclass/default as-is. Test.
3. For one variant at a time: override the method in that variant's class
   with its leg of the conditional; delete that leg from the shared copy;
   test after each variant.
4. Make the shared fallback abstract or leave it as the default case. Commit.

**Replace Nested Conditional with Guard Clauses**
1. Take the outermost special-case condition; convert it to an early-return
   guard. Test.
2. Repeat inward, one condition per step, until the main path reads
   unnested. Consolidate duplicate guards. Test, commit.

For any refactoring not condensed here, state its catalog name and derive
the same pattern: prepare a parallel structure, migrate piecewise with tests
between moves, remove the old structure last.

## When NOT to refactor (Fowler, ch. 2)

- Ugly code you never need to modify or understand again — leave it.
- Easier to rewrite than refactor (tiny, isolated, well-fenced) — judge and
  say so explicitly.
- Mid-release stabilization or a red suite — wrong moment.
- No tests and no way to add characterization tests safely — reduce scope to
  transformations your tooling can prove safe (automated renames), and say
  the rest is blocked on testability.
- Economics rule: refactor because it makes the NEXT change easier and the
  code cheaper to modify — "clean code" for its own sake is not the
  justification; don't polish beyond need.

## Refactoring vs adjacent activities

| Activity | Behavior | Owner |
|---|---|---|
| Refactoring | Preserved, structure improves | this skill |
| New feature / bug fix | Changes | tdd-developer |
| Performance tuning | Preserved but time/space profile changes; needs measurement | performance-optimizer |
| Formatting / lint style | Preserved, structure unchanged | project formatter/linter — not refactoring |
