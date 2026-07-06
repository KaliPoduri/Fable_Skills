# Risk-based testing — distilled

Source: ISTQB Certified Tester Foundation Level Syllabus v4.0.1, chapter 5
(Managing the Test Activities), sections 5.2 (Risk Management)
(https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf).
Distilled for offline use — do not fetch the URL at runtime.

## Risk fundamentals (5.2.1)

- **Risk** = a potential event, hazard, threat, or situation whose
  occurrence causes an adverse effect.
- **Risk level** = likelihood of occurrence x impact (harm) if it occurs.
- Risk-based testing exists because exhaustive testing is impossible
  (principle 2): risk decides where the limited test budget goes.

## Product risk vs project risk (5.2.2)

- **Product risks** — quality-related: missing or wrong functionality,
  incorrect calculations, runtime failures, poor architecture, inefficient
  algorithms, inadequate response time, poor UX, security vulnerabilities.
  Consequences: user dissatisfaction, revenue/reputation loss, criminal
  penalties, in extreme cases injury or death.
- **Project risks** — management/control-related: schedule delays,
  budget overruns, scope creep, people issues (skill gaps, conflicts,
  communication), supplier failure, organizational pressure. Consequences:
  late delivery, cost overrun, quality compromise.
- The test strategy mitigates PRODUCT risks with testing; PROJECT risks go
  to the plan's risk register with owners and mitigations, not test cases.

## Product risk analysis (5.2.3)

Two steps, done early (early testing, principle 3), repeated as knowledge
grows:

1. **Risk identification** — brainstorm what could fail, with
   stakeholders: wrong outputs, data corruption, unavailability, slow
   response, unusable UI, insecure interfaces. Use defect history
   (defects cluster, principle 4), domain knowledge, and requirement
   ambiguity as sources.
2. **Risk assessment** — categorize each risk; rate likelihood and impact
   (a High/Medium/Low scale is enough at foundation level); compute risk
   level; prioritize.

Record as a table: ID, risk, likelihood, impact, level, mitigation.

## How risk level drives the test approach (5.2.3-5.2.4)

Product risk analysis results determine:

- **Thoroughness** — higher risk => more test cases, more techniques, more
  coverage; lowest risk may get only smoke-level or no dedicated testing.
- **Scope** — which test levels and test types are performed at all.
- **Order** — execute tests for the highest risks earliest, so the worst
  problems surface with maximum remaining reaction time.
- **Technique selection** — e.g. formal black-box techniques plus
  white-box coverage for critical components; exploratory only for
  low-risk areas.
- **Beyond-testing actions** — risks can also be mitigated by reviews,
  training, design changes; note when testing is not the right mitigation.

## Risk control and residual risk (5.2.4)

- **Risk mitigation** — the planned test (and non-test) actions reduce
  likelihood or impact.
- **Risk monitoring** — re-evaluate risk levels as test results arrive;
  new failures raise likelihood estimates; passed high-risk tests reduce
  residual risk.
- **Residual risk** — whatever remains after mitigation, INCLUDING
  everything deliberately not tested. Exit criteria must make residual
  risk explicit; stakeholders accept it consciously, never by omission.
  This is the syllabus basis for the "what NOT to test, and why" section:
  every exclusion is a residual risk with a named acceptor.

## Practical prioritization heuristics

Consistent with the principles above:

- Defect clustering (principle 4): weight modules with bad defect history
  or high churn as higher likelihood.
- New and changed code carries more risk than stable code; regression
  testing guards the stable part (automate it — see
  test-automation-engineer).
- Complex integrations, third-party dependencies, and concurrency raise
  likelihood; money, safety, legal compliance, and privacy raise impact.
- Under time pressure, cut lowest-RISK items first — never cut by lowest
  effort, and record each cut in the out-of-scope table.
