# Flaky (non-deterministic) tests — root causes and remedies

Source: Martin Fowler, "Eradicating Non-Determinism in Tests",
martinfowler.com, 2011-04-14
(https://martinfowler.com/articles/nonDeterminism.html). Distilled for
offline use — do not fetch the URL at runtime. Supplemented with the
async-wait patterns implied by the same article.

## Why flakiness is toxic

Non-deterministic tests fail sometimes and pass sometimes with no code
change. They are worse than useless:

- They are **infections**: one red-for-no-reason test teaches the team to
  ignore red builds, which buries real regressions ("virulent infection
  that can completely ruin your entire test suite").
- They destroy the suite's value as a regression bug detector — the whole
  point of automated tests.

Never remediate with automatic retries or longer sleeps; both hide the
root cause and slow the suite.

## Quarantine

- When a nondeterministic test blocks the team, move it to a
  **quarantined** suite that does not gate the main build, so the deployment
  pipeline stays trusted.
- Quarantine is a hospital, not a graveyard: cap the queue size (e.g. a
  small fixed number per team), assign an owner, and fix or delete within
  a deadline. Tests that stay quarantined provide zero protection.

## Root cause catalog

### 1. Lack of isolation (shared state)

- Symptom: test passes alone, fails in the suite (or vice versa); failures
  depend on execution order; parallel runs fail.
- Cause: tests share mutable state — database rows, static/global
  variables, files, singletons — and a prior test's leftovers corrupt the
  next test's preconditions. A single rogue test breaks OTHER tests.
- Remedy: each test builds its own state from a known start. Two ways:
  rebuild state at test START (leftovers from crashes get cleaned) or
  roll back in teardown (transactions). Prefer per-test unique data (ids,
  temp dirs) so tests can run in parallel. Immutable shared fixtures are
  safe; mutable shared fixtures are not.

### 2. Asynchronous behavior (the #1 practical cause)

- Symptom: fails under load or on slow CI agents, passes locally; "worked
  when I added a sleep".
- Cause: test checks a result before the async operation finished; bare
  `sleep(n)` is either too short (flaky) or too long (slow suite) — and
  usually both across environments.
- Remedy, in order of preference:
  1. **Callback/completion handle** — block on a future/promise/notification
     the operation provides, with a timeout.
  2. **Polling** — loop checking the observable condition every short
     interval until a bounded timeout; fail loudly on timeout. Make
     interval and timeout configurable per environment.
  3. Never a bare sleep as the synchronization mechanism.
- Design help: put async plumbing behind a seam so most logic is testable
  synchronously; test the async machinery itself in few, dedicated tests.

### 3. Remote services

- Symptom: fails when the third-party system or shared test environment is
  down, slow, or returns changed data.
- Cause: tests call real remote systems that are outside the team's
  control and nondeterministic.
- Remedy: replace remote calls with test doubles/stubs for the main suite;
  keep a SEPARATE, non-gating integration/contract suite that exercises
  the real service; use consumer-driven contract tests to detect provider
  changes deliberately instead of randomly.

### 4. Time

- Symptom: fails at midnight, month/year end, DST changes, leap years; or
  intermittently when comparing "now" taken twice.
- Cause: code or test reads the system clock directly.
- Remedy: **always wrap the system clock** behind an injectable provider;
  tests set fixed or scripted times. Also isolate date-boundary test data.
  Never assert on two separate "now" reads being equal.

### 5. Resource leaks

- Symptom: suite fails after N tests, or under parallelism; errors about
  exhausted connections/handles/memory; the failing test varies.
- Cause: tests (or code under test) leak database connections, file
  handles, threads, or memory; the failure surfaces far from the leak.
- Remedy: manage resources with pools that complain loudly on exhaustion;
  guaranteed teardown (try/finally, fixtures, containers); investigate the
  leak rather than bumping the limit.

## Diagnosis quick table

| Observation | Suspect first |
|---|---|
| Passes alone, fails in suite | Isolation / shared state |
| Fails only on slow CI agents | Async waits (bare sleeps) |
| Fails when external env is down | Remote services |
| Fails at date boundaries | Time |
| Fails after long runs / in parallel | Resource leaks, isolation |
| Fails only in a particular order | Ordering / isolation |

## Verifying a fix

Run the repaired test repeatedly (dozens of runs), in shuffled order, and
in parallel with the rest of its suite, before releasing it from
quarantine. A fix you cannot demonstrate under those conditions is a
guess.
