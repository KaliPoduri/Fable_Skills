# The Nine Debugging Rules — distilled

Source: David J. Agans, *Debugging: The 9 Indispensable Rules for Finding
Even the Most Elusive Software and Hardware Problems*, AMACOM
(ISBN 978-0-8144-7457-0). Distilled for offline use; see
`SOURCES.md` for verification details.

The rules are ordered; the early ones are preconditions for the later
ones. When a debugging session stalls, re-read the list top to bottom and
identify which rule is currently being violated — there is almost always
exactly one.

## Rule 1 — Understand the System

- Read the manual, the design doc, the API contract, the schema — before
  forming theories. Most "impossible" bugs are impossible only under a
  wrong mental model of the system.
- Know what the system is *supposed* to do and how data is supposed to
  flow. You cannot recognize wrong behavior without knowing right behavior.
- Know your tools: what the debugger, profiler, and log levels can show
  you. An unused capability is evidence you never collected.

## Rule 2 — Make It Fail

- Reproduce the failure on demand before doing anything else. A bug you
  can trigger at will is already half-diagnosed.
- Write the trigger down as an exact, replayable procedure (ideally a
  script). "Click around until it breaks" is not a repro.
- Start from a known state: fixed data, fixed config, clean environment.
- For intermittent failures: do not chase them manually. Automate the
  repro in a loop, log every run, and compare failing runs with passing
  runs — the difference is the uncontrolled variable (timing, input,
  concurrency, uninitialized state, external dependency).
- Never simulate the failure with a different mechanism and call it the
  same bug. Make *it* fail, not something that looks like it.

## Rule 3 — Quit Thinking and Look

- Theorizing is cheap and usually wrong. Observation beats speculation:
  attach the debugger, add the log line, inspect the actual state.
- See the failure happen at the lowest level you practically can. Guessing
  saves minutes and wastes days.
- Instrument first, then interpret. When a guess and an observation
  disagree, the observation wins.
- Do not fix anything until you have *seen* the failure mechanism.

## Rule 4 — Divide and Conquer

- Binary-search the failure space. Repeatedly split the range that must
  contain the defect and test the midpoint:
  - the data flow (is the value already wrong here?),
  - the input (does half the input still fail?),
  - the history (which commit introduced it? — `git bisect`),
  - the configuration (which flag flips the behavior?).
- Always narrow from the side where the failure is visible back toward
  the origin. Start upstream of the symptom, confirm bad state, move up.
- Fix bugs you find on the way — known defects add noise to every later
  experiment.

## Rule 5 — Change One Thing at a Time

- One experiment = one change. If you change two things and the behavior
  changes, you learned nothing attributable.
- After every experiment that did not help, revert the change before the
  next one. Do not let dead experiments accumulate in the working tree.
- Compare against a baseline: keep a known-good version, input, or
  environment and diff behavior against it.
- Grab the low-hanging fruit: if something recently changed and the bug is
  new, suspect the change first.

## Rule 6 — Keep an Audit Trail

- Write down every experiment: what you did, in what order, what happened.
  Memory lies, especially about what you already tried.
- Record what did NOT work and what you did NOT change — negative results
  eliminate hypotheses and prevent loops.
- Be specific: exact commands, exact inputs, exact error text. "It failed
  differently" is useless a day later.
- The audit trail is the evidence log in the skill's output template.

## Rule 7 — Check the Plug

- Question your assumptions, starting with the dumbest ones: Is the right
  build deployed? Right branch? Right database? Is the code you are
  editing the code that is running? Is the test even executing?
- Validate the foundations, not just the logic: environment variables,
  file permissions, versions of runtime and dependencies, clock, disk
  space, network reachability (in-org).
- When nothing makes sense, the flaw is usually in a "certainty," not in
  an unknown.

## Rule 8 — Get a Fresh View

- Explain the problem end-to-end to someone else (or a rubber duck). The
  act of serializing your reasoning exposes the hidden assumption.
- Report symptoms, not your theory — handing someone your conclusion
  contaminates their fresh view.
- Ask an expert on the subsystem when one exists; read the bug tracker and
  changelog for the same symptom seen before.
- Pride is expensive: asking for help after two failed approaches is
  cheaper than a third failed approach (quit-loops rule).

## Rule 9 — If You Didn't Fix It, It Ain't Fixed

- After the fix, run the *original* repro. It must fail before the fix and
  pass after — both directions, on the same procedure.
- Where practical, take the fix back out and confirm the failure returns.
  If the bug disappeared without the fix explaining it, it is not fixed;
  it is hiding.
- "It hasn't happened again lately" is not a fix. Intermittent bugs must
  be verified with the amplified repro from Rule 2.
- Verify the fix did not break anything nearby: run the surrounding test
  suite, not just the repro.
