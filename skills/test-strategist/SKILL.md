---
name: test-strategist
description: Writes test strategies and test plans in ISTQB CTFL v4.0.1 terms (test levels, types, risk priorities). Use this skill when asked 'test strategy', 'test plan for', 'what should we test'. Do not use to write test code; use test-automation-engineer. For developer red-green TDD loops use tdd-developer. Also covers risk-based prioritization, entry/exit criteria, environments and test data needs, and what NOT to test and why.
metadata:
  version: "1.0.0"
  last-verified: "2026-07-06"
---

# Test Strategist

Produce a test strategy or test plan for a feature, release, or system
using ISTQB Certified Tester Foundation Level (CTFL) syllabus v4.0.1
vocabulary: test levels, test types, risk-based prioritization, entry and
exit criteria, environment and test data needs, and an explicit
out-of-scope list with reasons. The deliverable is a planning document,
not test code — hand implementation to test-automation-engineer.

## Constraints

Assume no external internet access, no paid tools, and English output.
Never send project code or data to external services.
Produce planning documents only; never write automated test code here.
Use ISTQB CTFL v4.0.1 terminology consistently and cite the syllabus in
the deliverable.
State assumptions explicitly when project context is missing; ask at most
once for the highest-impact unknowns.

## Workflow

1. Gather context. Identify the test object (feature, release, system),
   quality goals, SDLC model (sequential vs iterative — it changes when
   and how test levels run), stakeholders, and constraints (time, people,
   environments). List unknowns as assumptions rather than stalling.
2. Analyze product risks. Enumerate what could fail in the product and
   what the impact would be. Score each risk: likelihood x impact, on a
   simple High/Medium/Low scale. Give each a RISK-<n> ID. Load
   references/risk-based-testing.md for the method.
3. Derive the test approach from the risks. Risk level drives test
   thoroughness, choice of techniques, order of execution, and which test
   levels/types carry each risk's mitigation.
4. Select test levels. Choose from component, component integration,
   system, system integration, and acceptance testing — state which apply,
   who performs each, and the test basis for each. Load
   references/istqb-vocabulary.md when naming levels, types, or terms.
5. Select test types per level: functional, non-functional (name the
   specific characteristics, e.g. performance efficiency, usability,
   security, reliability), black-box vs white-box coverage, and where
   confirmation and regression testing fit.
6. Prioritize. Order test activities so the highest product risks are
   covered earliest; state what gets cut first if time runs out (lowest
   risk, not lowest effort).
7. Define entry and exit criteria for each level (definition of ready /
   definition of done): what must hold before testing starts, and the
   measurable conditions for declaring it complete (coverage achieved,
   open-defect thresholds, residual risk accepted).
8. Specify environments and test data: environments per level, who owns
   them, data needed (volume, realism, privacy constraints — anonymize or
   synthesize personal data), and refresh/reset strategy.
9. Declare what NOT to test, and why: each exclusion tied to a reason —
   low risk, covered at another level, out of scope contractually, or not
   cost-effective. Untested-by-choice must be visible to stakeholders as
   accepted residual risk.
10. Assemble the document per the Output template, cite ISTQB CTFL
    syllabus v4.0.1, and run the Checklist.

## Output template

Produce exactly this structure:

```markdown
# Test Strategy: <test object>

## Context and quality goals
<Test object, SDLC model, stakeholders, constraints. Quality goals.>

## Assumptions and open questions
- <assumption or question>

## Product risk analysis
| ID | Risk | Likelihood | Impact | Risk level | Mitigated by |
|---|---|---|---|---|---|
| RISK-1 | <what could fail> | H/M/L | H/M/L | H/M/L | <level(s)/type(s)> |

## Test levels
| Level | In scope? | Performed by | Test basis | Key objects |
|---|---|---|---|---|

## Test types
<Per level: functional / non-functional (named characteristics) /
black-box vs white-box / confirmation and regression placement.>

## Prioritization
<Risk-ordered sequence; what is cut first under time pressure and why.>

## Entry and exit criteria
| Level | Entry criteria | Exit criteria |
|---|---|---|

## Environments and test data
<Environment per level, ownership, data needs, privacy handling, reset.>

## Out of scope (what we will NOT test, and why)
| Exclusion | Reason | Residual risk owner |
|---|---|---|

## Sources
Based on ISTQB CTFL Syllabus v4.0.1 (istqb.org).
```

## References (load on demand)

- `references/SOURCES.md` — source manifest (always present).
- `references/istqb-vocabulary.md` — load when naming test levels, test
  types, testing principles, or plan sections, to keep terminology
  syllabus-accurate.
- `references/risk-based-testing.md` — load when performing the product
  risk analysis, prioritization, or entry/exit criteria definition.

## Checklist

- [ ] Every risk has an ID, likelihood, impact, level, and a mitigating
      test level/type.
- [ ] Test levels and types use ISTQB CTFL v4.0.1 names, and the syllabus
      is cited in the Sources section.
- [ ] Entry AND exit criteria present for every in-scope level, and they
      are measurable.
- [ ] Environments and test data addressed, including privacy handling.
- [ ] Out-of-scope section present with a reason per exclusion.
- [ ] No test code in the deliverable (that is test-automation-engineer's
      job).
- [ ] Output follows the template above.
