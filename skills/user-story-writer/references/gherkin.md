# Gherkin — acceptance criteria syntax and style

Distilled from: Gherkin Reference, Cucumber documentation,
https://cucumber.io/docs/gherkin/reference (last updated 2026-07-03,
verified 2026-07-06). The Rule keyword exists as of Gherkin 6.

Gherkin is a structured plain-text syntax for executable specifications.
For this skill it is the format for acceptance criteria; scenarios must
read correctly even if the team never automates them.

## Keywords

Primary keywords (start a block; all except step keywords take a colon):

| Keyword | Purpose |
|---|---|
| `Feature` | Names the capability; MUST be the first primary keyword in a document; one Feature per file. Free-text description may follow. |
| `Rule` | (Gherkin 6+) Optional grouping of scenarios that illustrate one business rule. |
| `Scenario` (or `Example`) | One concrete example of behavior: steps below it. |
| `Given` | Context — the state of the world before the action. |
| `When` | The event or action under test. |
| `Then` | The expected, observable outcome. |
| `And`, `But`, `*` | Continue the previous step type without repeating it. |
| `Background` | Steps shared by every scenario in the Feature/Rule — one per Feature/Rule, keep it short. |
| `Scenario Outline` (with `Examples`) | Runs the same scenario once per row of the Examples table; placeholders in `<angle brackets>`. |

Secondary syntax: Doc Strings (`"""` multi-line step argument), Data
Tables (`|`-delimited rows attached to a step), Tags (`@tag` above a
Feature/Scenario), Comments (`#` at line start). Recommended indentation
is two spaces per level. Gherkin is localized to 70+ languages; this
library writes English.

## Structure rules

- One `Feature` per file; scenarios sit under the Feature (optionally
  grouped under `Rule`).
- Step order within a scenario: `Given` → `When` → `Then`. Use `And`/`But`
  to extend a type; do not bounce back (no Then-When-Then chains).
- Exactly one `When` per scenario is the norm — more than one action
  means more than one behavior, so split the scenario.
- `Then` outcomes must be observable by a user or an external system
  (message shown, state visible, email sent) — not internal implementation
  ("record is written to the cache").

## Style rules for acceptance criteria

1. Scenario titles state the behavior and its condition: "Expired card is
   declined", not "Test 3".
2. Write steps in third person, present tense, declarative: "When the
   customer submits the order".
3. No UI mechanics: "When the customer confirms the purchase", not "When
   the user clicks the green Buy button". Keep criteria valid across UI
   redesigns.
4. Givens describe state, not action history: "Given the customer has an
   expired card", not "Given the customer went to the card page and typed
   an expired card".
5. First scenario = main success path. Follow with the variations and
   failure paths that change the outcome (2–5 scenarios total for one
   story; more suggests the story is too big — see epic-story-breakdown).
6. Use `Scenario Outline` + `Examples` only when steps are identical and
   only data varies; otherwise separate scenarios are clearer.
7. Use `Background` only for context truly shared by all scenarios, and
   keep it to a few Givens.

## Skeleton

```gherkin
Feature: Order checkout
  Customers pay for the items in their cart.

  Scenario: Successful payment with a valid card
    Given the customer has a cart with one in-stock item
    And the customer has a valid saved card
    When the customer confirms the purchase
    Then the order is confirmed
    And a receipt is sent to the customer's email address

  Scenario: Expired card is declined
    Given the customer has a cart with one in-stock item
    And the customer's saved card is expired
    When the customer confirms the purchase
    Then the payment is declined
    And the customer is asked for another payment method
```
