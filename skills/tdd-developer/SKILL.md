---
name: tdd-developer
description: Implements features and bugfixes test-first with the TDD red-green-refactor loop. Use this skill when asked for TDD or test-first work. Do not use for cleanup-only work; use refactoring-expert. For unknown-bug diagnosis use systematic-debugger instead. Once the cause is known, or when asked to write the failing test first, apply this skill to pin behavior with a test. Covers test lists, triangulation, and fake-it-till-you-make-it.
metadata:
  version: "1.0.0"
  last-verified: "2026-07-06"
---

# TDD Developer

Implement features and bugfixes by strict test-driven development as defined
by Kent Beck (Test-Driven Development: By Example, Addison-Wesley, 2002) and
Martin Fowler (martinfowler.com/bliki/TestDrivenDevelopment.html): maintain a
test list, write one failing test at a time, make it pass with the smallest
change that works, then refactor on green. Never write production code except
in response to a failing test, and never skip the refactor step — Fowler
calls skipping it the most common way to ruin TDD.

## Constraints

Assume no external internet access, no paid tools, and English output.
Never send project code or data to external services.
Run the real test command and read its output; never assume a test passes or fails.
Never weaken, delete, or skip an existing test to reach green.
Wear one hat at a time: change behavior OR structure in a step, never both.
Keep this skill technology-agnostic: apply the same loop in any language with any test runner the project already uses.

## Workflow

1. **Confirm the mode.** New behavior or a bugfix with a KNOWN cause → proceed.
   Unknown failure cause → stop and route to `systematic-debugger`; resume
   here at step 7 once the cause is identified. Pure structure cleanup with
   no new behavior → route to `refactoring-expert`.
2. **Find the test command.** Locate how this project runs tests (build file,
   CI config, README, package manifest). Run the existing suite once to
   confirm a green baseline. If the baseline is red, report it and ask before
   proceeding.
3. **Write the test list.** Before any code, list every behavior the change
   implies: normal cases, boundaries, error cases, and the refactorings you
   already suspect. Keep the list in the output template and update it as new
   cases occur to you mid-loop — add them to the list, do not chase them
   immediately.
4. **Pick the next test.** Choose the test that teaches the most while being
   small enough to pass within minutes — usually the simplest unimplemented
   behavior, or for a brand-new unit, a degenerate "starter" case (empty
   input, zero, one element).
5. **RED — write the failing test first.**
   - Write one concrete test asserting the desired behavior through the
     interface you WISH existed (this is the design step).
   - Run it. Confirm it fails, and fails for the right reason: an assertion
     failure or a missing symbol matching the new behavior — not an unrelated
     error, and never an unexpected pass.
   - Quote the observed failure message in the cycle log.
6. **GREEN — smallest change that passes.** Pick one strategy:
   - **Fake It**: return the constant the test expects, then generalize in
     later cycles. Use when the real implementation is not obvious or the
     last step failed.
   - **Obvious Implementation**: type the real code directly. Use only when
     you are confident it is a few clean lines; if the test then fails, drop
     back to Fake It.
   - **Triangulation**: only generalize an implementation when a second test
     with a different example forces it. Use when unsure what the right
     abstraction is.
   Sins committed on the way to green (duplication, constants, ugliness) are
   allowed — they are debts step 8 repays. Run the failing test until it
   passes, then run the whole suite.
7. **Bugfix variant.** With the cause known, first write the smallest test
   that reproduces the bug at the lowest level that can express it — watch it
   fail with the bug's symptom — then fix with the smallest change and watch
   it pass. The reproduction test stays in the suite as a regression guard.
8. **REFACTOR — only on green.** Remove the duplication just introduced,
   between production code and between test and code (a faked constant
   duplicated in test and implementation is the signal to generalize).
   Improve names. Run the suite after each transformation. If a large,
   catalog-scale restructuring is needed, finish the current loop green and
   route that work to `refactoring-expert`.
9. **Tick the list and commit.** Mark the test done, add any newly discovered
   cases to the list, and commit the green state with a message naming the
   behavior added. One behavior per commit keeps every step reversible.
10. **Repeat or finish.** Loop to step 4 until the test list is empty and no
    known duplication remains. Then fill in the output template, including
    real command output for the final green run.

If you go around the loop twice without reaching green, shrink the step:
smaller test, Fake It instead of Obvious Implementation, or revert to the
last green state and restart the cycle.

## Decision guide

Choosing the green strategy (Beck, Part III):

| Situation | Strategy |
|---|---|
| Real implementation is a few confident, clean lines | Obvious Implementation |
| Not sure how to implement, or last step went red unexpectedly | Fake It (return the expected constant) |
| Fake passed but the right generalization is unclear | Triangulation — add a second test with a different example and let it force the general code |
| Cycle stalled twice | Shrink the step: smaller test, more faking, or revert to last green |

Fake vs make it real for dependencies:

| Dependency | Default |
|---|---|
| Pure in-process collaborator | Use the real thing |
| Clock, randomness, network, filesystem, database | Substitute an owned-interface double; introduce the seam as a refactor step |
| Interaction IS the behavior (e.g. "sends exactly one email") | Mock-style assertion on the interaction — sparingly |
| Double drifting from the real contract | Keep one real-collaborator (contract/integration) test where the environment allows |

Routing:

| Signal | Route |
|---|---|
| Failure cause unknown | `systematic-debugger`, then return here to pin it with a test |
| Structure-only cleanup, no new behavior | `refactoring-expert` |
| New behavior discovered mid-loop | Add to the test list; never chase it while red |

## Output template

Produce exactly this structure when the session ends:

```markdown
# TDD Session — <feature or bug>

## Test list
- [x] <behavior — done>
- [ ] <behavior — deferred, with reason>

## Cycles
### Cycle <n>: <test name>
- RED: <test added; observed failure message>
- GREEN: <strategy: Fake It | Obvious Implementation | Triangulation; change made>
- REFACTOR: <duplication removed / rename applied, or "none needed">
- Suite: <command> → <summary, e.g. 42 passed>

## Result
- Behavior added: <one line per behavior>
- Final suite run: <command> → <pasted summary line from real output>
- Regression tests added (bugfixes): <test names or "n/a">
- Deferred items / follow-ups: <list, including anything routed to refactoring-expert>
```

## References (load on demand)

- `references/SOURCES.md` — source manifest (always present).
- `references/red-green-refactor.md` — load when executing cycles: the loop
  in detail, choosing Fake It vs Obvious Implementation vs Triangulation,
  failing for the right reason, and common failure modes.
- `references/test-list-and-bugfix.md` — load when building or reordering the
  test list, writing a bug-reproduction test, deciding on test doubles
  (fake vs make it real), or judging when to stop.

## Checklist

- [ ] Every production change was preceded by a failing test I ran and watched fail.
- [ ] Each cycle's failure message and final suite output come from real command runs this session.
- [ ] Refactor step performed (or explicitly "none needed") in every cycle; suite green after each.
- [ ] No existing test was weakened, deleted, or skipped.
- [ ] Test list is empty or every remaining item is listed as deferred with a reason.
- [ ] Bugfix work includes a regression test that failed before the fix.
- [ ] Output follows the template above.
