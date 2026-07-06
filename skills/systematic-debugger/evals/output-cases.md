# Output eval cases (≥3)

Each case is run twice — WITH the skill installed and WITHOUT (raw
assistant) — and scored against the rubric in
docs/AUTHORING-GUIDE.md §Eval thresholds. The skill must beat raw output.

## Case 1

- Prompt: "Debug this: our REST endpoint /orders/{id} intermittently
  returns 500 (about 1 in 15 requests). Logs show
  'ConcurrentModificationException in OrderCache.evict'. It started
  sometime in the last two weeks."
- Input artifacts (if any): stack trace snippet, note that a known-good
  tag `v3.2.0` exists from three weeks ago.
- Rubric focus: template compliance, actionability, source accuracy
  (intermittent-bug procedure, bisect).
- Expected qualities: refuses to propose a code fix before a repro
  exists; produces a looped/amplified repro plan with failure-rate
  baseline; proposes `git bisect run` between v3.2.0 and HEAD with an
  automated repro script; one hypothesis at a time with an evidence-log
  table; fix verification defined as FAIL-before/PASS-after on the
  original repro plus statistical re-run for the intermittency.

## Case 2

- Prompt: "Why is this failing? This parser test passes on my machine but
  fails on the build server with 'expected 42, got 0'. Same branch, same
  commit."
- Input artifacts (if any): the failing test name and assertion output.
- Rubric focus: completeness (environment-difference method), template
  compliance.
- Expected qualities: treats it as an environment-diff problem (Rule 7
  "check the plug" + halving the environment diff); enumerates concrete
  candidate variables (locale, timezone, JDK/runtime version, file
  encoding, CPU count, env vars, working directory); designs one-change
  experiments; records exact error text verbatim; ends with the
  Debugging Report template headings (Symptom, Reproduction, Evidence
  log, Root cause, Fix and verification, Follow-ups).

## Case 3

- Prompt: "I've already tried increasing the timeout twice and it still
  deadlocks under load. Find the real cause of the deadlock in the worker
  pool."
- Input artifacts (if any): thread-dump excerpt showing two threads
  blocked on opposite lock order.
- Rubric focus: actionability, source accuracy (quit-loops rule,
  defect/infection/failure chain).
- Expected qualities: explicitly invokes the quit-loops rule (same
  approach — bumping timeouts — already failed twice, so strategy must
  change); reads the thread dump as evidence before hypothesizing; states
  a single falsifiable hypothesis about lock ordering; proposes the
  cheapest discriminating experiment; expresses the conclusion as a
  cause-effect chain from defect to failure; hands the regression test
  off to tdd-developer in Follow-ups.
