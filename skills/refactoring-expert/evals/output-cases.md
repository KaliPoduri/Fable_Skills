# Output eval cases (≥3)

Each case is run twice — WITH the skill installed and WITHOUT (raw
assistant) — and scored against the rubric in
docs/AUTHORING-GUIDE.md §Eval thresholds. The skill must beat raw output.

## Case 1

- Prompt: "This 250-line `generateInvoice` function mixes parsing, tax rules, and formatting. Refactor it."
- Input artifacts (if any): the function plus a partially-covering test file (happy path only).
- Rubric focus: source accuracy (smell vocabulary + catalog names), template compliance.
- Expected qualities: coverage gap detected and characterization tests added BEFORE any edit; smells named (Long Function, Divergent Change / mixed phases); refactorings named from the catalog (Split Phase, Extract Function, Replace Temp with Query); change log shows suite run after each step and one refactoring per commit; report matches the "Refactoring Report" template.

## Case 2

- Prompt: "Remove the duplication between `PdfExporter` and `CsvExporter` — and while you're at it the date bug in both should be fixed."
- Input artifacts (if any): both classes and a green suite.
- Rubric focus: actionability, completeness (two-hats discipline and boundary handling).
- Expected qualities: duplication removed via named refactorings (Extract Function / Pull Up Method / Extract Superclass or Combine Functions into Class); the date BUG is explicitly NOT fixed in the refactoring commits — it is pinned in "Out of scope / follow-ups" and routed to tdd-developer; no test assertions edited; behavior-verification section shows a final green run.

## Case 3

- Prompt: "Clean up this payment module: repeated switch on `paymentType` in four places, and a `Utils` class everyone dumps helpers into."
- Input artifacts (if any): the module with its suite.
- Rubric focus: completeness (smell-to-refactoring mapping), source accuracy.
- Expected qualities: Repeated Switches mapped to Replace Conditional with Polymorphism with the variant-at-a-time mechanics (factory first, one override per step, tests between); Utils diagnosed (Feature Envy / misplaced responsibility) with Move Function toward the data; smells table complete with locations and one-line evidence; any performance speculation routed to performance-optimizer instead of being acted on.
