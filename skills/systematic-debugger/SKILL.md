---
name: systematic-debugger
description: "Diagnoses bugs hypothesis-first: reproduce, gather evidence, one hypothesis at a time, binary search. Use this skill when asked to debug, why is this failing, intermittent bug, works on my machine. Do not use to fix a known cause; use tdd-developer instead. Do not use for general code quality review; use code-reviewer instead. Covers evidence logs, git bisect, minimal repro, and fix verification."
metadata:
  version: "1.0.0"
  last-verified: "2026-07-06"
---

# Systematic Debugger

Diagnose bugs with a disciplined, hypothesis-driven method instead of guessing.
Reproduce the failure reliably before anything else, gather evidence before
touching code, test exactly one hypothesis at a time with the cheapest
discriminating experiment, and binary-search the failure space — inputs,
commit history, and code paths. Keep an evidence log throughout, and never
declare victory until the fix demonstrably kills the original reproduction.
The method distills Agans' nine debugging rules and Zeller's scientific
debugging process (see References).

## Constraints

Assume no external internet access, no paid tools, and English output.
Never send project code or data to external services.
Never apply a fix before the root cause is confirmed by an experiment.
Change one thing at a time; back out any change that did not help.
Quit-loops rule: if the same fundamental approach fails twice, stop and
change strategy — do not attempt a third variation of the same idea.

## Workflow

1. **Capture the symptom verbatim.** Record the exact error text, stack
   trace, or wrong output — never paraphrase. Record environment: OS,
   runtime version, branch, commit, config that differs from default.
2. **Reproduce reliably before touching anything.** Find a sequence of
   steps that triggers the failure on demand. Automate it (a script, a
   test invocation, a curl call). If you cannot reproduce, that is the
   first problem to solve — do not "fix" what you cannot see fail.
3. **If the bug is intermittent, make it fail more.** Loop the repro,
   amplify load, fix random seeds, freeze the clock, pin thread counts,
   log every run. Compare failing runs against passing runs to find the
   uncontrolled variable. Load `references/scientific-debugging.md` for
   the intermittent-bug procedure.
4. **Gather evidence before changing code.** Read logs, stack traces,
   recent diffs (`git log --stat` since the last known-good state), and
   the actual runtime state (debugger, print instrumentation, core dump).
   Quit thinking and look: see the failure happen, don't theorize it.
5. **Establish the last known-good baseline.** Identify a version, input,
   or environment where the behavior is correct. Every later step
   discriminates between the good and bad states.
6. **Form ONE falsifiable hypothesis.** Write it as a single sentence:
   "The failure occurs because X." It must predict something observable.
   Do not hold multiple hypotheses in play at once.
7. **Design the cheapest discriminating experiment.** Pick the experiment
   that most cheaply confirms or refutes the hypothesis: a log line, a
   narrowed input, a toggled flag, a stubbed dependency. Change one thing,
   run the repro, record the result in the evidence log.
8. **Binary-search the failure space.** Halve whichever dimension is
   largest:
   - **Inputs:** delete half the failing input; keep whichever half still
     fails; repeat until minimal (delta debugging).
   - **History:** `git bisect start`, mark bad and good commits, let git
     halve the range; automate with `git bisect run <repro-script>`.
   - **Code path:** instrument the midpoint of the suspect flow; determine
     whether state is already corrupt there; recurse into the bad half.
   Load `references/scientific-debugging.md` for exact procedures.
9. **Keep the evidence log current.** After every experiment append one
   row: what you did, what you observed, what it proved or refuted. What
   you did NOT change and what did NOT work is evidence too.
10. **Apply the quit-loops rule.** If two experiments driven by the same
    fundamental approach both failed to discriminate, stop. Re-read the
    evidence log, question an assumption ("check the plug": is the right
    build deployed? right config? right database?), or explain the problem
    end-to-end to a rubber duck / colleague. Load
    `references/nine-rules.md` when stuck.
11. **Confirm the root cause.** State the full cause-effect chain from
    defect to observed failure. Prediction test: using only the stated
    cause, predict a second observable consequence and verify it.
12. **Verify the fix kills the original repro.** Run the exact repro from
    step 2: it must fail before the fix and pass after. Where practical,
    re-introduce the defect and confirm the failure returns — if you
    didn't fix it, it ain't fixed. Check that nothing else broke.
13. **Hand off for a regression test.** Once the cause is confirmed,
    pinning it with a failing automated test and implementing the durable
    fix is owned by `tdd-developer`. Deliver the report below as input.

## Output template

Produce the debugging report in exactly this structure:

```markdown
# Debugging Report: <one-line symptom>

## Symptom
Exact error text / wrong behavior, verbatim. Environment and version.

## Reproduction
Numbered steps or the command that triggers the failure on demand.
Reliability: deterministic | intermittent (N failures per M runs).

## Evidence log
| # | Experiment (one change) | Observation | Hypothesis status |
|---|---|---|---|
| 1 | ... | ... | supported / refuted |

## Root cause
The defect, its location, and the cause-effect chain to the symptom.
Confirmed by: <experiment #>.

## Fix and verification
What changed. Repro result before fix: FAIL. After fix: PASS.
Side effects checked: <what else was run>.

## Follow-ups
- Regression test to add (hand to tdd-developer).
- Related latent risks noticed but out of scope.
```

## References (load on demand)

- `references/SOURCES.md` — source manifest (always present).
- `references/nine-rules.md` — load at the start of any debugging session
  and whenever stuck or looping; full distillation of Agans' nine rules.
- `references/scientific-debugging.md` — load when minimizing a failing
  input, running `git bisect`, chasing an intermittent bug, or formalizing
  the hypothesis loop; distilled from Zeller.

## Checklist

- [ ] Failure reproduced on demand (or intermittency quantified) before
      any code was changed.
- [ ] Exact error text recorded verbatim, never paraphrased.
- [ ] Every experiment changed exactly one thing and is in the evidence log.
- [ ] Only one hypothesis was active at a time.
- [ ] Quit-loops rule respected: no third variation of a failed approach.
- [ ] Root cause states a full cause-effect chain, confirmed by experiment.
- [ ] Original repro ran FAIL-before / PASS-after the fix.
- [ ] Follow-up regression test handed to tdd-developer.
- [ ] Output follows the template above.
