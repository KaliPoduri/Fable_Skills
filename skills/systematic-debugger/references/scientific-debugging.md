# Scientific Debugging — hypothesis loop, delta debugging, bisect

Sources: Andreas Zeller, *Why Programs Fail: A Guide to Systematic
Debugging*, 2nd edition, Morgan Kaufmann, 2009 (ISBN 978-0-12-374515-6);
git-bisect procedure from Git documentation (git-scm.com/docs/git-bisect,
Git 2.55.0 docs). Distilled for offline use; see `SOURCES.md`.

## Terminology: defect → infection → failure

Zeller separates three things that casual speech calls "the bug":

- **Defect**: the incorrect code (the thing to fix).
- **Infection**: the incorrect program *state* the defect creates at
  runtime.
- **Failure**: the externally visible wrong behavior (the symptom).

Debugging is tracing the cause-effect chain backwards: failure → infected
state → earlier infected state → the defect that first infected a sane
state. A fix is only a root-cause fix if it breaks this chain at the
defect, not merely at a later infection (that is symptom-patching).

## The TRAFFIC process

Zeller's overall debugging workflow, step by step:

1. **T**rack the problem — record it (issue, exact symptom, environment).
2. **R**eproduce the failure — deterministically, on demand.
3. **A**utomate and simplify the test case — a one-command repro, as
   small as possible.
4. **F**ind possible infection origins — where could the bad state come
   from? (data flow backwards from the failure).
5. **F**ocus on the most likely origins — prioritize by suspicion:
   recently changed code, code failing other tests, complex/known-risky
   code.
6. **I**solate the infection chain — hypothesis loop (below) until the
   earliest infection, i.e. the defect, is identified.
7. **C**orrect the defect — fix, then prove the failure is gone and
   nothing else broke.

## The scientific-method loop (one hypothesis at a time)

Repeat until the defect is isolated:

1. **Hypothesis** — one falsifiable sentence consistent with all
   observations so far ("the cache returns a stale entry when the key
   contains a slash").
2. **Prediction** — something observable that must be true if the
   hypothesis holds ("logging the cache hit at line N will show the old
   timestamp").
3. **Experiment** — the cheapest test of the prediction. Change or
   observe exactly one thing.
4. **Observation** — run it; record the actual result verbatim in the
   evidence log.
5. **Conclusion** — hypothesis *supported* (refine it, narrow scope) or
   *refuted* (discard it, form the next one from the evidence).

Rules of the loop:

- Never hold two active hypotheses; interleaved experiments contaminate
  each other.
- A refuted hypothesis is progress — log it so it is not retried.
- If two consecutive experiments under the same overall approach fail to
  discriminate anything, the approach is wrong — change strategy
  (quit-loops rule): pick a different dimension to search (input vs
  history vs code path), or re-check assumptions.

## Delta debugging: minimize the failing input (ddmin)

Goal: the smallest input that still fails. Small inputs make every later
experiment faster and usually point straight at the defect.

Manual binary-search version (sufficient in practice):

1. Split the failing input in half.
2. Test each half alone. If one half still fails, continue with that half.
3. If neither half fails alone, the failure needs a combination: remove
   smaller chunks (quarters, eighths) from the full input, keeping every
   removal that preserves the failure.
4. Stop when removing any remaining piece makes the failure disappear.
   That is a *1-minimal* failing input.

The same halving works on any dimension: lines of a config file, records
in a dataset, steps in a repro script, enabled feature flags, browser
extensions, environment differences between "works on my machine" and the
failing machine (diff the two environments, then halve the diff).

## Bisecting history: which commit introduced the failure

Precondition: an automated repro command that exits 0 on good, non-zero
on bad.

```
git bisect start
git bisect bad                  # current commit fails
git bisect good <known-good>    # e.g. last release tag
# git checks out the midpoint; run the repro, then:
git bisect good   # or: git bisect bad
# repeat until git prints the first bad commit
git bisect reset                # return to the original HEAD
```

Automated (preferred):

```
git bisect start HEAD <known-good> --
git bisect run <repro-command>   # exit 0 = good, 1-127 (not 125) = bad,
                                 # 125 = cannot test, skip this commit
git bisect reset
```

Notes:

- log2(N) steps for N commits — 1000 commits ≈ 10 tests. Always worth it
  when a known-good version exists.
- If the build is broken at some commits, exit 125 to skip them.
- The first bad commit is where to *look*, not automatically the defect —
  read its diff and connect it to the infection chain.

## Intermittent failures: control the nondeterminism

An intermittent bug is a deterministic bug with an uncontrolled variable.
Procedure:

1. Automate the repro in a loop; record failure rate (N failures / M
   runs) as the baseline.
2. Log candidates for the uncontrolled variable on every run: thread
   interleaving, timing, random seeds, wall clock, input arrival order,
   external service responses, memory addresses, environment.
3. Diff a failing run's log against a passing run's log. The systematic
   difference is the variable.
4. Pin variables one at a time (fix the seed, freeze the clock, force one
   thread, mock the dependency) and watch the failure rate move toward
   0% or 100%. At 100% you have a deterministic repro — proceed normally.
5. Statistical verification: after the fix, run the same loop; the
   failure rate must drop to 0 over materially more runs than the
   baseline needed to show a failure.

## Fix verification (Correct step)

- Run the original automated repro: FAIL before the fix, PASS after.
- Re-introduce the defect where practical and confirm the failure
  returns — proves the fix, not coincidence, killed the failure.
- Run the surrounding test suite to catch collateral damage.
- The confirmed cause-effect chain plus the minimal repro is the handoff
  package for a regression test (owned by tdd-developer).
