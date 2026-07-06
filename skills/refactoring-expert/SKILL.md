---
name: refactoring-expert
description: Improves existing code without changing behavior using Fowler's refactoring catalog. Use this skill when asked to refactor or clean up code. Do not use for new behavior; use tdd-developer. For performance tuning use performance-optimizer instead. Also use when a function is too long or duplication needs removing. Maps code smells to named refactorings with mechanical safety steps, test-coverage preconditions, and commit rhythm. Style-only lint fixes are not refactoring.
metadata:
  version: "1.0.0"
  last-verified: "2026-07-06"
---

# Refactoring Expert

Improve the internal structure of existing code without changing its
observable behavior, following Martin Fowler's *Refactoring: Improving the
Design of Existing Code*, 2nd edition (Addison-Wesley, 2018) and the online
catalog at refactoring.com/catalog. Diagnose code smells, map each to a named
refactoring, and apply it as a series of small, individually-safe mechanical
steps with the test suite run between steps — so the code is never broken for
more than minutes and any step can be reverted cheaply.

## Constraints

Assume no external internet access, no paid tools, and English output.
Never send project code or data to external services.
Never change observable behavior: no new features, no bug fixes, no output or API contract changes, unless the user explicitly re-scopes.
Wear one hat at a time (Fowler's "two hats"): never mix refactoring with behavior changes in the same step or commit.
Never refactor code that lacks a safety net of tests — build one first (step 2).
Run the real test suite between steps and read the output; a skipped run is an unverified step.
Style-only lint fixes (formatting, quote style, import order) are not refactoring — say so and route them to the project's formatter/linter.

## Workflow

1. **Confirm the scope is behavior-preserving.** If the request includes new
   behavior, route that part to `tdd-developer` (refactor first to make the
   change easy if needed, then hand over). If the motivation is speed or
   memory, route to `performance-optimizer` — performance work needs
   measurement, not smell-driven transformation. If it is purely formatting
   or lint style, state that this is not refactoring and stop.
2. **Verify the test precondition.** Find and run the test command. The code
   to be changed must be covered by self-checking tests that currently pass.
   - Coverage exists and is green → proceed.
   - Coverage is missing → write characterization tests first: pin the
     CURRENT behavior (including its oddities) with tests you watch pass;
     record any suspected bugs separately without fixing them.
   - Suite is red → stop and report; refactoring on red is unverifiable.
3. **Diagnose smells.** Read the target code and name what is wrong using the
   smell vocabulary (load `references/smells-to-refactorings.md`). For each
   finding record: location, smell name, evidence (one line).
4. **Map smells to named refactorings.** For every smell choose the
   catalog refactoring(s) that address it, and order the work so each
   transformation leaves the code compiling and green. Prefer the smallest
   refactoring that removes the smell; do not chain speculative redesigns.
5. **Present the plan** (table from the output template) before large or
   multi-file changes; for a single small, unambiguous refactoring, proceed.
6. **Apply each refactoring by its mechanics.** Load
   `references/mechanics-and-safety.md` and follow the step list for the
   chosen refactoring: tiny steps, compile/tests after each, never a big-bang
   edit. Use IDE/automated refactorings where available; they are safer than
   hand edits, but still run the tests.
7. **Run the suite after every transformation.** Green → continue. Red →
   revert the last step (do not debug forward through a broken refactoring)
   and retry in smaller steps.
8. **Commit at each green milestone.** One named refactoring (or one
   coherent batch of trivial ones, e.g. renames) per commit, message naming
   the refactoring: "Extract Function: computeCharge". Small commits keep
   every transformation reversible.
9. **Re-scan.** After the mapped smells are gone, re-read the result: did
   the change expose a deeper smell (it often does)? Add follow-ups to the
   report rather than expanding scope silently.
10. **Report** using the output template, with real final suite output, and
    list anything deliberately NOT done (bugs found, perf ideas, new-behavior
    wishes) routed to the owning skill.

## Decision guide

Fast smell-to-refactoring map for the most frequent cases (full 24-smell
table in `references/smells-to-refactorings.md`):

| Smell | First-line refactoring |
|---|---|
| Long Function | Extract Function (prepare with Replace Temp with Query, Split Variable) |
| Duplicated Code | Extract Function; Slide Statements; Pull Up Method |
| Mysterious Name | Change Function Declaration; Rename Variable/Field |
| Long Parameter List | Introduce Parameter Object; Preserve Whole Object |
| Repeated Switches | Replace Conditional with Polymorphism |
| Feature Envy | Move Function (extract the envious piece first if needed) |
| Large Class | Extract Class |
| Nested conditionals | Replace Nested Conditional with Guard Clauses; Decompose Conditional |

Routing:

| Signal | Route |
|---|---|
| Request includes new behavior or a bug fix | `tdd-developer` (refactor first only to make that change easy) |
| Motivation is speed or memory | `performance-optimizer` — measure, don't smell |
| Formatting, quote style, import order | Project formatter/linter — state that this is not refactoring |
| Failure of unknown cause found mid-refactor | Revert the last step; if it predates your work, report and route to `systematic-debugger` |
| Suspicious behavior found while adding characterization tests | Pin it as-is, flag as possible bug in the report — never fix silently |

When NOT to refactor (Fowler, ch. 2):

- Ugly code that never needs to be understood or modified again — leave it,
  and say why.
- A tiny, well-fenced unit that is easier to rewrite than refactor — call
  the rewrite out explicitly as a rewrite, not a refactoring.
- A red suite or mid-release stabilization — wrong moment; report the block.
- Refactor because it makes the NEXT change easier and the code cheaper to
  modify — not to reach an abstract ideal of clean code. Stop when the
  motivating smell is gone.

## Output template

Produce exactly this structure:

```markdown
# Refactoring Report — <target>

## Precondition
- Test command: <command>
- Baseline: <green / characterization tests added (list) / blocked-red>

## Smells and mapped refactorings
| Location | Smell | Named refactoring | Why |
|---|---|---|---|
| <file:function> | <catalog smell> | <catalog name> | <one line> |

## Change log
| Step | Refactoring applied | Suite result | Commit |
|---|---|---|---|
| 1 | <name: subject> | <e.g. 42 passed> | <hash or message> |

## Behavior verification
- Final suite run: <command> → <pasted summary line from real output>
- Observable behavior changes: none <or explain re-scope approved by user>

## Out of scope / follow-ups
- <suspected bug found — NOT fixed; route to systematic-debugger/tdd-developer>
- <performance idea — route to performance-optimizer>
- <remaining smells worth a future pass>
```

## References (load on demand)

- `references/SOURCES.md` — source manifest (always present).
- `references/smells-to-refactorings.md` — load when diagnosing (step 3–4):
  the smell catalog with each smell mapped to its named refactorings.
- `references/mechanics-and-safety.md` — load when executing (step 6–8):
  two-hats discipline, characterization tests, step-by-step mechanics for the
  core refactorings, and the commit rhythm.

## Checklist

- [ ] Scope confirmed behavior-preserving; new-behavior and performance asks routed to tdd-developer / performance-optimizer.
- [ ] Tests existed or characterization tests were added BEFORE any transformation; baseline was green.
- [ ] Every smell finding names a catalog smell and a catalog refactoring.
- [ ] Suite was run after each transformation; any red step was reverted, not debugged forward.
- [ ] Commits are small, each named after the refactoring applied.
- [ ] No behavior change: no assertions edited, no outputs or public contracts altered.
- [ ] Bugs discovered were reported, not silently fixed.
- [ ] Output follows the template above.
