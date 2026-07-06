# Code smells mapped to named refactorings

Source: Martin Fowler, *Refactoring: Improving the Design of Existing Code*,
2nd edition, Addison-Wesley Professional, 2018 (ISBN 978-0134757599) —
Chapter 3 "Bad Smells in Code" (written with Kent Beck) and the catalog
chapters; online catalog: https://refactoring.com/catalog/ (supports the 2nd
edition). Smell concept: Martin Fowler, "CodeSmell", martinfowler.com/bliki
(2006-02-09). See references/SOURCES.md.

A code smell is "a surface indication that usually corresponds to a deeper
problem" (Fowler, bliki). A smell is a prompt to look, not proof of a
problem — record the evidence, then decide. Refactoring names below are the
2nd-edition catalog names; former 1st-edition names in parentheses where they
changed (e.g. Extract Function, formerly Extract Method).

## The 24 smells of the 2nd edition, with primary refactorings

| # | Smell | What it looks like | Primary named refactorings |
|---|---|---|---|
| 1 | Mysterious Name | Function/variable/class name doesn't say what it does | Change Function Declaration; Rename Variable; Rename Field |
| 2 | Duplicated Code | Same structure in more than one place | Extract Function; Slide Statements; Pull Up Method |
| 3 | Long Function | Function you must scroll or study to follow | Extract Function; Replace Temp with Query; Introduce Parameter Object; Preserve Whole Object; Replace Function with Command; Decompose Conditional |
| 4 | Long Parameter List | Callers juggle many arguments | Replace Parameter with Query; Preserve Whole Object; Introduce Parameter Object; Remove Flag Argument; Combine Functions into Class |
| 5 | Global Data | Mutable data reachable from anywhere | Encapsulate Variable (formerly Self-Encapsulate Field / Encapsulate Field) |
| 6 | Mutable Data | Widely-shared data changed in place | Encapsulate Variable; Split Variable; Separate Query from Modifier; Remove Setting Method; Replace Derived Variable with Query; Change Reference to Value |
| 7 | Divergent Change | One module edited for many different reasons | Split Phase; Move Function; Extract Function; Extract Class |
| 8 | Shotgun Surgery | One change forces edits in many modules | Move Function; Move Field; Combine Functions into Class; Combine Functions into Transform; Inline Function; Inline Class |
| 9 | Feature Envy | Function talks to another module's data more than its own | Move Function; Extract Function (then move the piece) |
| 10 | Data Clumps | Same group of fields/params traveling together | Extract Class; Introduce Parameter Object; Preserve Whole Object |
| 11 | Primitive Obsession | Domain concepts encoded as bare strings/numbers | Replace Primitive with Object; Replace Type Code with Subclasses; Replace Conditional with Polymorphism; Extract Class |
| 12 | Repeated Switches | Same conditional dispatch duplicated around the code | Replace Conditional with Polymorphism |
| 13 | Loops | Loop obscures what is being computed | Replace Loop with Pipeline (filter/map/reduce) |
| 14 | Lazy Element | Class/function whose structure no longer pays for itself | Inline Function; Inline Class; Collapse Hierarchy |
| 15 | Speculative Generality | Hooks and flexibility for a future that never came | Collapse Hierarchy; Inline Function; Inline Class; Change Function Declaration (drop unused params); Remove Dead Code |
| 16 | Temporary Field | Field set only in certain situations | Extract Class; Move Function; Introduce Special Case (formerly Introduce Null Object) |
| 17 | Message Chains | a.getB().getC().getD() navigation trains | Hide Delegate; Extract Function + Move Function |
| 18 | Middle Man | Class that mostly delegates elsewhere | Remove Middle Man; Inline Function; Replace Superclass with Delegate / Replace Subclass with Delegate |
| 19 | Insider Trading | Modules whispering to each other's internals | Move Function; Move Field; Hide Delegate; Replace Subclass with Delegate |
| 20 | Large Class | Class with too many fields/responsibilities | Extract Class; Extract Superclass; Replace Type Code with Subclasses |
| 21 | Alternative Classes with Different Interfaces | Two classes do the same job with different signatures | Change Function Declaration; Move Function; Extract Superclass |
| 22 | Data Class | Fields, getters/setters, no behavior | Encapsulate Record; Remove Setting Method; Move Function (bring behavior to the data); Extract Function; Split Phase |
| 23 | Refused Bequest | Subclass ignores most of what it inherits | Push Down Method; Push Down Field; Replace Subclass with Delegate; Replace Superclass with Delegate |
| 24 | Comments (as deodorant) | Comment compensating for unclear code | Extract Function; Change Function Declaration; Introduce Assertion |

Note on Comments: comments are fine; the smell is a comment doing the job a
better name or smaller function should do. When you feel the need to write
one, first try to refactor so the comment becomes superfluous.

## Frequently used catalog refactorings (quick index)

First-line tools you will reach for most, all in the online catalog:

- **Extract Function / Inline Function** — the workhorses for Long Function,
  Duplicated Code, Comments, Lazy Element.
- **Change Function Declaration** — renames and re-parameterizes (absorbs
  1st-edition Rename Method, Add/Remove Parameter).
- **Rename Variable / Rename Field / Encapsulate Variable** — naming and
  data-access hygiene.
- **Move Function / Move Field** — realigning behavior with the data it uses
  (Feature Envy, Shotgun Surgery, Insider Trading).
- **Extract Class / Inline Class** — right-sizing modules (Large Class, Data
  Clumps, Temporary Field vs Lazy Element).
- **Replace Temp with Query, Split Variable, Slide Statements** — preparing a
  Long Function for clean extraction.
- **Decompose Conditional, Replace Conditional with Polymorphism, Replace
  Nested Conditional with Guard Clauses, Consolidate Conditional
  Expression, Introduce Special Case** — conditional logic family.
- **Split Phase, Replace Loop with Pipeline, Combine Functions into
  Class/Transform** — 2nd-edition additions for tangled computation.
- **Remove Dead Code, Remove Flag Argument, Separate Query from Modifier** —
  API and hygiene cleanups.

## Diagnosis discipline

- Name the smell using the vocabulary above; "this code is bad" is not a
  finding. Format: location, smell, one line of evidence.
- One smell can suggest several refactorings and one refactoring can cure
  several smells — choose the SMALLEST transformation that removes the
  observed smell; do not redesign around a hypothetical.
- Smells found while doing something else go on the follow-up list, not into
  the current change (scope discipline).
- If the smell is only visible with profiling data (slow loop, allocation
  churn), it is a performance concern, not a smell — route to
  performance-optimizer.
