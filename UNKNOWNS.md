# UNKNOWNS.md — Spark Tooling Plan (PlanGenie register)

Plan for: (1) codebase deep-understanding analyzer, (2) Spark log/plan performance advisor.
Previous plan (skills library) archived at `archive/2026-06-skills-library-plan/`.
Status: FINAL — PLAN.md v5. Council complete after 3 rounds, unanimous closure (both seats: 10/10 majors CLOSED, no new majors). 18 refinements accepted, 1 rejected (native-context trial). Remaining opens are deliberately parked at M0: U1, U5, U8, U9, U10 and assumptions A5–A11 (see PLAN §10–§11).
2026-07-10 update: user offline from org network; per user directive the three skills were authored VERSION-ADAPTIVE (they ask for U1/U5/A10 facts at intake instead of assuming them — see implementation-notes.md). All opens above remain OPEN until the M0 spike locks them; m0/ kit unchanged.
Fact updates from round 2 (both seats verified): Copilot billing is usage-based since 2026-06-01 (premium-request model legacy); edit mode also writes files (agent mode = writes + terminal); gh skill CLI exists since Apr 2026 (public preview).
New opens from round 1: U9 scheduler type; U10 adoption plan; assumptions A5–A11 (agent-mode policy, multi-root discovery, repo visibility, scheduler-config completeness, history-server access, config-change scope, log sensitivity) — mostly resolved at M0 spike. U2/U3 note: resolved into PLAN §3 design (staleness stamps + scope statement; KB content = navigation/lineage/narrative, pointers not copies).

## Known knowns

Idea and scope:
- [USER] Two tools. Tool 1: analyzes one or more whole repos (scripts, SQL, everything) and generates a "deep understanding" file of the ecosystem.
- [USER] Tool 1's file must be efficient for LLM parsing — chunk-navigable, not one huge blob; the skill must tell the LLM how to manage chunks and parse efficiently.
- [USER] Tool 1 is multipurpose: (a) paste a job-failure error → root cause + solution; (b) explain how a functionality/process flow works; (c) advise on performance/efficiency improvements for SQL and scripts.
- [USER] Tool 2: reads Spark logs (e.g. physical plans), understands the ETL process, interacts back-and-forth asking relevant questions, then provides fixes: SQL optimization + specific config parameters for specific scenarios.
- [USER] Both tools: end user treated as a total newbie — no Spark infra/jargon/SQL/performance skills assumed.
- [USER] Packaging (skill vs agent vs other) delegated to planner; proposal goes in the draft plan for user approval. (echo-checked)

Builder:
- [USER] Codes a little; around the Spark/ETL problem area but not in it daily.

Environment and users (interview):
- [USER] Q1 Platform (CORRECTED after draft v1): GitHub Copilot Chat (VS Code, org) ONLY — org does not have Claude Code. (echo-checked)
- [USER] Packaging approved: three Agent Skills in the Fable Skills library. Ops deferred — dev team is the target. A non-prod environment exists for safe testing. (echo-checked)
- [USER] Q2 Privacy: org policy allows sending both source code and job logs to these AI tools.
- [USER] Q3 Repo contents: SQL files, shell scripts, Python/PySpark.
- [USER] Q3b Also: scheduler configs (job definitions/dependencies) and config/params files.
- [USER] Q4 Scale: 3–10 repos, hundreds to a couple thousand files.
- [USER] Q5 Platform: believed on-prem Hadoop/YARN — working assumption, NOT verified. (echo-checked)
- [USER] Q6 End users: support/ops team + dev team (no analysts).
- [USER] Q8 Access split: ops never need the repos — they do a high-level first-pass triage from the error log and hand off; devs (repos cloned) do the deep RCA. (echo-checked)
- [USER] Q7 Failure inputs available: scheduler alert + error snippet; full job log file obtainable.
- [USER] Q9 Freshness: understanding file regenerated on demand by a developer when things changed (no CI/schedule).
- [USER] Q10 Non-code causes: tool must diagnose "likely data/infra, not code", explain why, and guide step-by-step checks.
- [USER] Q11 Tool 2 inputs: physical plan text (copy-paste) + Spark UI access. (Full logs also exist per Q7.)
- [USER] Q12 Success, in priority order: #1 faster correct RCA (hours → minutes), #2 measurable job speedups from Tool 2 advice. Newbie self-sufficiency is secondary. (echo-checked)
- [USER] Q14 Constraints: no hard deadline; tools must NOT auto-change code (advise only); tools must NOT run anything against production themselves.
- [USER] Q15 Spark version: 3.x.

## Known unknowns

- [OPEN] U1 (was B3/B6): Verify the platform really is on-prem Hadoop/YARN, and which exact Spark 3.x minor version (affects which configs exist/default on). Tools should also detect/ask at runtime.
- [OPEN] U2 (was B1): "Regen on demand" accepted — but how will a user KNOW the file is stale? Mitigation to design in plan (e.g. stamp the git commit the file was built from and warn on mismatch).
- [OPEN] U3 (was B4): Exact content design of the understanding file — what must it hold that live repo search can't cheaply reconstruct (cross-repo job→script→SQL→table lineage). Planner proposes in draft.
- [OPEN] U4: Where do ops (no repos) run their triage and would they have access to a published copy of the understanding file (e.g. a shared analysis repo)?
- [OPEN] U5 (was B5): Whether ops/devs know HOW to fetch YARN logs / physical plans / Spark UI pages — tools should include fetch-instructions; exact steps depend on U1.
- [OPEN] U6 (was B6): Safe-verification convention for tuning advice (how a newbie tests a config change off-prod) — depends on what non-prod environments exist. Not asked; raise in plan.

## Unknown knowns (assumptions dug out)

- Resolved: org permits code+logs to LLM (Q2 — yes). Platform assumption surfaced (Q5 — flagged unverified). Harness assumption surfaced (Q1 — Copilot + Claude Code).
- [OPEN] U7: User may be assuming Copilot Chat and Claude Code can run the same artifacts identically — capability differences (subagents, scripts, context sizes) must be handled in the plan.

## Unknown unknowns

- Phase 1 teaching surfaced B1–B6 (now folded into U1–U6). Phase 4 council review pending.

## Topic checklist

| Topic | Status |
|---|---|
| Users | Answered (ops triage + dev deep-RCA; both Spark newbies) |
| Features | Answered (Tool 1: RCA/explain/perf-advice; Tool 2: interactive tuning) |
| Data | Answered (SQL, shell, PySpark, scheduler + param configs; 3–10 repos) |
| Integrations | Answered w/ opens (Copilot org + Claude Code; YARN unverified → U1) |
| Constraints | Answered (no deadline; advise-only; never touch prod) |
| Success criteria | Answered (#1 faster RCA, #2 real speedups) |
| Risks | Answered as U1–U7 opens |
