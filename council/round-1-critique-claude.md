# Council round 1 — Claude seat critique (verbatim)

## Major concerns

1. **The riskiest unknown (U8) sits under an already-[CONFIRMED] decision.** The whole architecture assumes Copilot Chat can run long agentic sessions that read scheduler configs, trace jobs across up to ~2000 files, and *write* a directory of KB files. That is untested until M1, yet packaging is locked. Also "Copilot Chat" is ambiguous: only **agent mode** writes files and runs terminal commands; ask mode cannot. Skill A is impossible outside agent mode and the plan never says so.

2. **The staleness-stamp mechanism may be unenforceable.** Comparing stored commit hashes to the live repo requires running `git` — an agent-mode terminal action needing user approval per session. In ask mode the "mandatory" staleness warning silently cannot happen. The plan's strongest safety claim (R2 mitigation) depends on an unstated harness capability.

3. **Skill routing is model-decided, and the plan assumes deterministic handoffs.** VS Code docs confirm the model chooses when a skill applies. Three overlapping skills (B's static perf advice vs C's runtime advice) invite mis-routing, and "hand off to Skill C" implies an inter-skill mechanism Copilot doesn't have — it's just telling the user to re-ask. Nothing tests cross-triggering.

4. **Wrong-KB risk is bigger than stale-KB risk, and it's under-mitigated.** LLM-traced lineage over templated SQL, shell indirection, and runtime-resolved params *will* contain errors. R3 covers wrong advice; nothing covers a wrong knowledge base, which poisons every downstream answer while carrying an aura of authority. The M1 gate — "builder eyeballs it" — is the weakest gate protecting the most consequential artifact.

5. **Size budgets contradict the stated scale.** INDEX.md at ~200 lines cannot hold a job inventory plus routing guide for up to 10 repos / hundreds of jobs. `lineage.md` and `errors/playbook.md` "grow" unbounded with no sharding or split rule — recreating exactly the "one huge file" problem the [USER] requirement forbids.

6. **The evals convention can't validate the target harness.** Library evals presumably run in Claude tooling; runtime is Copilot with user-selectable models. Green evals in one harness say little about behavior in the other, and model variance inside Copilot is unaddressed.

## Minor concerns

7. Scheduler type is an unregistered unknown. "Scheduler configs exist" is confirmed, but Skill A's tracing instructions differ radically between Airflow, Oozie, Control-M, and cron. Should be U-something.

8. KB governance is missing: concurrent dev appends to `errors/playbook.md` (merge conflicts, entry quality), and pasted logs may carry data values/PII that get *persisted to a repo* — org policy covered Copilot ingestion, not KB retention.

9. Org admin policy: Agent Skills in VS Code is a recent, recently-experimental feature; Copilot enterprise policies can disable such features. Verify with the org admin, not just format docs.

10. No adoption or baseline plan: how Spark newbies discover the skills, and no measurement of current time-to-root-cause, so "minutes not hours" (success #1) is untestable.

11. Multi-root workspace skill discovery: unverified whether VS Code loads `.agents/skills/` from a *secondary* workspace root. If the skills live in the KB repo, discovery may fail. [Unverified — test at M0/M1.]

12. Register hygiene: U2 and U3 are missing from the unknowns list with no note; M2's "majority correctly diagnosed" gate is unquantified; M3 measures one job once (n=1, confounded by cluster load).

## Fact-hunt

13. **`.agents/skills/` claim: VERIFIED.** VS Code docs list `.github/skills/`, `.claude/skills/`, and `.agents/skills/` as project skill directories; GitHub shipped Agent Skills support Dec 2025. Caveats: `.github/skills/` is the primary documented location, the feature was still labeled experimental in Jan 2026 coverage (validates R5), and the docs confirm the model decides when to load a skill (feeds concern 3).

14. **"Adaptive query engine": wrong name.** The Spark feature is **Adaptive Query Execution (AQE)**, and it is default-on only since Spark 3.2 — default-off in 3.0/3.1. This makes U1's "which 3.x minor" more load-bearing than the plan implies.

15. **R4 ("limits undocumented") is partially false and R1's cost model is off.** Copilot billing is documented: one agent-mode user prompt = 1 premium request; autonomous tool calls are free. So a long build costs prompts, not tool calls — but documented short-term rate limits and org premium-request quotas can still stall multi-hour builds. What's genuinely undocumented is per-session agentic depth.

16. No fabrications found in the Spark material: Spark UI, YARN logs, physical-plan operators (Exchange/shuffle, scans), skew, spill, partition count, join strategy, small files, filter pushdown are all real Spark 3.x concepts. The "docs/COMPATIBILITY.md read this session" basis is unverifiable from this packet, but claim 13 independently supports its conclusion.

## Concrete refinements

17. **Add an M0 half-day spike before locking the KB format:** in Copilot agent mode, run a mini Skill A against one repo — confirm skills load from the chosen path, the agent writes files, and observe real session depth. This resolves U8 *before* the format spec, not after.

18. Say "agent mode" explicitly wherever writes or git are needed; define ask-mode fallback (state "staleness unchecked" instead of silently skipping).

19. Shard growing files: `lineage/<table-or-domain>.md` and dated/indexed playbook files, each with a size budget and a split rule; replace the single 200-line INDEX with a thin root index plus per-repo indexes.

20. Strengthen the M1 gate: pipeline owner verifies a random sample of N jobs (inputs, outputs, lineage) against ground truth; record accuracy % and misses in `meta/generation.md`.

21. Route playbook appends through PR review with a redaction rule (strip data values from logs before persisting).

22. Put the chunk protocol in `copilot-instructions.md`/AGENTS.md too, so it holds even when skill auto-selection misses; write mutual disambiguation lines into B's and C's descriptions and eval cross-triggering.

23. Consider re-ordering: Skill C has zero KB dependency and the fastest verifiable payoff (M3-style measurement) — delivering it first de-risks the project while the KB approach is validated.

24. Fix the AQE naming; capture 3–5 recent incidents' actual time-to-root-cause now as the baseline for success #1.

Sources cited by the seat: VS Code docs (agent skills), GitHub changelog 2025-12-18, GitHub docs (about agent skills; Copilot requests billing), Visual Studio Magazine 2026-01-11, GitHub community discussion 165239.
