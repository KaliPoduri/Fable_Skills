---
name: spark-performance-advisor
description: "Tunes slow (not failed) Spark jobs from runtime evidence: physical plan, Spark UI, YARN logs, shuffle, skew, config. Use this skill when a Spark job is slow. Do not use for failed jobs (etl-assistant) or database EXPLAIN tuning (sql-optimizer). Plain-language interview; requires the exact Apache Spark 3.x minor version before config advice; advise-only - never executes anything against a cluster."
metadata:
  version: "1.0.0"
  last-verified: "2026-07-10"
---

# Spark Performance Advisor

Speed up Apache Spark jobs that run but run too slowly, using the user's
own runtime evidence — physical plan text, Spark UI observations, YARN
logs — never folklore. Interview the user in plain language (they may
have zero Spark knowledge), diagnose from the evidence, then deliver a
SQL rewrite and/or specific config parameters for their specific
scenario, with a non-prod experiment protocol to prove the win. Every
conclusion carries its evidence and a confidence level.

## Constraints

Assume no external internet access, no paid tools, and English output.
Never send project code or data to external services.
Advise-only: never execute anything against a cluster, scheduler, or
production system — every command in the output is for the user to run
and review themselves.
Never give config advice before the user states the exact Spark 3.x
minor version (which settings exist and which are on by default depend
on it).
Propose config changes job-scoped by default (spark-submit --conf or the
job's config file); flag anything cluster-scoped as "requires cluster
admin". Every config change needs job-owner approval before any run.
Run the safe-to-share checklist on every pasted or attached artifact
before analyzing it.
When evidence is insufficient, say "I cannot tell from what I have" and
list exactly what is missing and how to get it; guessing is a defect.
Assume zero Spark knowledge: define every Spark term in parentheses on
first use — e.g., "shuffle (data reshuffling between machines)".

## Workflow

1. **Triage: failed vs slow.** If the job FAILED (error message, stack
   trace, nonzero exit), this is the wrong skill: tell the user to
   invoke `etl-assistant` for error-to-root-cause analysis, and say
   explicitly that no automatic handoff exists — they must start it
   themselves. Proceed only when the job completes (or keeps running)
   but is too slow.
2. **Artifact receipt.** The FIRST response to any pasted or attached
   log, plan, or screenshot is the safe-to-share checklist — scan the
   content for: secrets or passwords; tokens, credentials, or API keys;
   customer identifiers (names, emails, account or ID numbers); raw data
   row values (literals in predicates count). Ask the user to confirm it
   is clean or to redact BEFORE any analysis. Length limits elsewhere in
   this skill are brevity rules, not privacy controls — only this
   content check protects data.
3. **Intake interview.** In plain language, collect:
   - REQUIRED GATE: the exact Spark 3.x minor version (e.g., 3.1 vs
     3.4). Explain why in one sentence: which settings exist and which
     are on by default depend on the exact version — for example AQE
     (Adaptive Query Execution, Spark's runtime re-optimizer) is on by
     default only since Spark 3.2. No config advice before this answer.
   - What "slow" means: how long it takes now, how long it took before
     or is expected to take, when it changed, and whether the input data
     grew.
   - What evidence exists: physical plan text, Spark UI access (running
     job), Spark History Server access (finished job), YARN logs.
   - Where the job runs and whether a non-prod environment is available
     for experiments.
4. **Gather or teach evidence.** When evidence is missing, load
   `references/evidence-gathering.md` and give exact fetch steps —
   including for FINISHED jobs (History Server / event logs) and
   `yarn logs -applicationId <app ID>` — always with the caveat to
   confirm access and log retention with the cluster admin. Ask for
   specific artifacts back (which tab, which numbers to copy).
5. **Read the plan.** Load `references/physical-plan-reading.md`.
   Identify: AdaptiveSparkPlan wrapper, Exchange (shuffle) count, join
   operators and build sides, scan nodes with PushedFilters and
   PartitionFilters, partition counts, whole-stage codegen groups.
6. **Diagnose.** Load `references/diagnosis-playbooks.md` and match the
   evidence against the playbooks: data skew, spill, partition count
   (too many / too few), join strategy, small files, missing
   filter/partition pushdown. Tie every claim to the user's own
   evidence. If the evidence does not settle it, say "I cannot tell
   from what I have", list what is missing, and stop short of guessing.
7. **Design the fix.** Prefer SQL/code rewrites first, then configs.
   Load `references/config-table.md` before proposing any parameter
   value; check its version notes against the user's minor version.
   Job-scoped mechanisms by default; mark cluster-scoped items
   "requires cluster admin".
8. **Deliver** using the Output template. Agree the minimum-improvement
   threshold with the user and RECORD it in the output BEFORE any
   experiment run happens.

## Output template

```markdown
# Spark tuning advice — <job name>

## Diagnosis
<the bottleneck in one plain-language sentence; terms defined>

## Why (your evidence)
- <claim> — <the exact plan node / UI metric / log line from the
  user's own material that supports it>

## Fix
<SQL/code rewrite first when one exists, as before/after; then:>
| Setting | Current | Proposed | Scope |
|---|---|---|---|
| <spark.…> | <value or unknown> | <value> | job (--conf) OR cluster — requires cluster admin |
Config changes need job-owner approval before any run.

## Try it in non-prod (experiment protocol)
- Input: the same input snapshot for every run.
- Conditions: note cache state and cluster load for each run.
- Runs: at least 3 per variant (baseline and change); compare median
  and p95 (95th percentile) durations.
- Minimum improvement to adopt: <agreed with the user and recorded
  here BEFORE the runs>.
- Rollback: <exact setting/code to restore>.
- Cost vs runtime: <e.g., more executors may finish faster but cost
  more — state the trade>.
- Scale: prod-like data volume, or record the caveat that it was not.

## Confidence
<High | Medium | Low> — <what additional evidence would raise it>

## Runtime-state caveat
<where the advice depends on deployed config, schedule, or cluster
state: "This assumes <X> — verify the live value before acting.">
```

## References (load on demand)

- `references/SOURCES.md` — source manifest (always present).
- `references/evidence-gathering.md` — load at step 4; Spark UI
  tab-by-tab, History Server for finished jobs, YARN logs, what to
  bring back.
- `references/physical-plan-reading.md` — load at step 5; how to get
  and read a physical plan, operator vocabulary, red flags.
- `references/diagnosis-playbooks.md` — load at step 6; playbooks for
  skew, spill, partition count, join strategy, small files, pushdown.
- `references/config-table.md` — load at step 7; parameter → plain
  meaning → when to change → version notes → scope.

## Checklist

- [ ] Triage done: job confirmed slow, not failed (failed → user told
      to invoke etl-assistant, no automatic handoff).
- [ ] Safe-to-share checklist was the FIRST response to any pasted
      artifact, before analysis.
- [ ] Exact Spark 3.x minor version recorded before any config advice.
- [ ] Every Spark term defined in parentheses on first use.
- [ ] Every conclusion cites the user's own evidence and carries a
      confidence level; insufficient evidence said out loud with what
      is missing and how to get it.
- [ ] Fix is SQL/code-first; every config is job-scoped or flagged
      "requires cluster admin"; job-owner approval stated.
- [ ] Minimum-improvement threshold agreed and recorded BEFORE runs;
      rollback step and cost-vs-runtime note present.
- [ ] Runtime-state caveat present where advice depends on deployed
      config or schedule.
- [ ] Output follows the template above.
