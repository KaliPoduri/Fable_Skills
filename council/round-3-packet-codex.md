BEGIN COUNCIL REVIEW PACKET (round 3 — confirmation pass)

You are a critical reviewer of a software project plan. You have no other
context; everything you need is below. This is round 3, a CONFIRMATION pass:
rounds 1-2 raised concerns, the plan was revised twice, and every major
concern was mapped to an accepted refinement. Your job now is to verify
closure, not to re-open settled decisions.

PART 1 — CLOSURE CHECK. Below are the major concerns raised in round 2.
For EACH numbered item, give a verdict: CLOSED (the current plan resolves it)
or STILL OPEN (say precisely what is missing). Judge against the CURRENT
plan below.

1. Copilot cost model was stale (GitHub moved to usage-based billing
   2026-06-01). Plan now: R1 rewritten; M0 fact-lock verifies the org's
   billing plan and sets a budget cap; M2 measures per-job build cost and
   extrapolates before green-lighting the full build.
2. Adoption was missing/ownerless. Plan now: M0 names an adoption owner and
   delivers rollout channel, "which skill do I use?" one-pager with
   invocation examples, demo incident, support channel.
3. Wrong-KB poisoning from LLM tracing. Plan now: authoritative job seed +
   instructed mechanical cross-checks at build time (grep-confirm every
   claimed table/entry point) + repo:path:line pointers on claims +
   per-repo owner sampling (>=20% or >=10 jobs) with negative checks +
   second-reviewer signoff for high-value jobs + regeneration as reviewable
   diffs + failed checks marked unverified.
4. Skill-C-first was blocked by unresolved unknowns. Plan now: U1 (Spark
   minor version), U5 (history-server access + retention), A10 (config
   permissions) are explicit M1 entry criteria resolved at M0.
5. Performance measurement was under-specified. Plan now: fixed experiment
   protocol (same input snapshot, cache state + cluster load noted, >=3
   runs, median + p95, agreed threshold, rollback, cost-vs-runtime,
   prod-like data or recorded caveat), job-owner approval.
6. Security/compliance was checklist-only. Plan now: content-based redaction
   (not line counts), checklist-first behavior on artifact receipt, playbook
   PRs with named reviewer role, approval criteria, disputed-cause handling,
   named security owner.
7. Ask-mode fallback might be unenforceable. Plan now: conditional on the M0
   test of whether skills load in ask mode at all; otherwise "agent mode
   required" is stated in adoption material.
8. Gates were unquantified. Plan now: M3 >=10 incidents incl. >=2
   not-in-code and >=2 insufficient-evidence traps; acceptance = recorded
   matrix of fixed cases inside Copilot across enabled models/modes.
9. Full-build effort was unestimated. Plan now: M2 measures per-job cost and
   extrapolates; full build green-lit only if affordable.
10. KB home risked polluting Copilot's implicit context. Plan now: dedicated
    small repo preferred, rationale recorded, final call at M0.

PART 2 — FINAL SWEEP (brief). Any NEW major concern introduced by the v4
changes, and a fact-hunt limited to claims that changed since round 2
(billing wording, edit/agent mode capabilities, gh skill CLI, error-pattern
index, acceptance matrix). If nothing new: say "no new major concerns."
Do NOT re-propose replacing the generated knowledge base with Copilot native
indexing/Spaces — the user has settled that decision.

Background on tags: `[USER]` = requesting user said it in the planning
interview; `[CONFIRMED]` = user-approved or verified (basis noted);
`[CANDIDATE]` = planner proposal, verify before use; `[OPEN]` = unresolved.

--- PLAN BEGINS ---
# PLAN.md — Spark ETL Assistant Suite (draft v4, after council round 2)

Tags: `[USER]` = said in interview · `[CONFIRMED]` = user-approved or verified (basis noted) · `[CANDIDATE]` = proposal, verify before use · `[OPEN]` = unresolved.
Register: UNKNOWNS.md. Council log: council/LOG.md. Previous plan archived at `archive/2026-06-skills-library-plan/`.

## 1. What we're building

- [USER] Two capabilities for Apache-Spark-newbie users: (1) a codebase deep-understanding tool for root-cause analysis of job failures, how-it-works questions, and performance advice on repo artifacts; (2) an interactive Spark log/physical-plan performance advisor.
- [USER] Harness: GitHub Copilot in VS Code (org license) ONLY — the org does not have Claude Code. Org policy allows code and logs in it.
- [CONFIRMED] (both council seats, GitHub/VS Code docs; user approved R2/S8) Skills load in agent-capable Copilot surfaces. Skill A requires **agent mode** — the mode that combines file writes with terminal commands (edit mode writes files but has no terminal). Whether skills load in ask mode AT ALL is verified at M0; the "declare unchecked steps" fallback applies only if they do — otherwise adoption material simply states "agent mode required".
- [CANDIDATE] The org's Copilot policy controls that govern agent features/skills must permit this — the exact policy name/scope is unverified; confirmed at M0 with the Copilot admin.
- [USER] Ecosystem: 3–10 repos, hundreds to ~2000 files — SQL, shell scripts, Python/PySpark, scheduler configs, config/params files. Apache Spark 3.x ([OPEN] U1: exact minor version).
- [USER] Users: the dev team (repos cloned, Spark newbies). Support/ops deferred.
- [USER] Success: #1 correct root causes in minutes not hours; #2 measurable job speedups from the advisor.
- [CONFIRMED] (user approved R7) Baseline: at M0, record actual time-to-root-cause of 3–5 recent incidents.
- [USER] Constraints: advise-only, never touch production, no hard deadline. A non-prod environment exists for safe testing.
- [CONFIRMED] (user approved R11) "Advise-only" = never auto-change application code; KB/doc writes on user request are allowed.

## 2. Packaging

- [CONFIRMED] (user approved) **Three Agent Skills in the existing Fable Skills library** — SKILL.md conventions, validators, source-verified references, evals, manual-copy distribution:
  - Skill A `etl-knowledge-builder` — dev-run (agent mode) KB (re)generation. Batch, rare.
  - Skill B `etl-assistant` — everyday Q&A: error → root cause; explain flow X; improve this SQL/script (static).
  - Skill C `spark-performance-advisor` — interactive tuning over runtime evidence (physical plans, Spark UI).
  - Plus the **knowledge base** — a sharded directory of markdown files (§3).
- [CONFIRMED] (user approved R11) Names fixed unless the user renames by M0 exit.
- [CONFIRMED] (both seats, GitHub/VS Code docs) Copilot in VS Code reads project skills from `.agents/skills/` (also `.github/skills/`, `.claude/skills/`); feature is recent/experimental in places — re-verify on breakage (R5).
- [CONFIRMED] (user approved R8/S8) **Routing hardening:** disambiguation lines in every skill description; a routing + chunk-protocol note in each code repo's `copilot-instructions.md` / `AGENTS.md` [CANDIDATE mechanism — M0]; cross-trigger eval cases; explicit invocation examples for all three skills in adoption material; "handoff" = telling the user which skill to invoke next (no automatic mechanism exists).
- [CANDIDATE] Alternatives rejected in round 1 (user arbitrated): MCP server / RAG app; Claude-Code subagent; plain prompt doc. Codex's native repo indexing/Spaces trial REJECTED by user — the generated KB stands.
- [CONFIRMED] (user approved; S8 clarification) "No scripts inside skills" is THIS library's local policy, not a platform limit (Copilot supports scripts in skills) — all three skills are pure markdown by our choice.
- [CONFIRMED] (Claude seat, GitHub changelog 2026-04-16) `gh skill` CLI (public preview, GitHub CLI ≥2.90) now exists as a future install alternative; distribution stays manual-copy for now (library decision).

## 3. The knowledge base (sharded data model)

- [USER] Chunk-navigable, efficient for LLM parsing — never one huge file.
- [CONFIRMED] (user approved R3/S7) Sharded layout (directory `etl-knowledge/`, budgets [CANDIDATE] tuned at M2):

  | File | Contents | Budget |
  |---|---|---|
  | `INDEX.md` | THIN root: overview, repo table linking per-repo indexes, routing guide | ~100 lines |
  | `repos/<repo>-index.md` | Per-repo job inventory: job → schedule → entry script → purpose → chunk link; slug↔real-name map | ~150 lines each |
  | `jobs/<job>.md` | Per job: plain-language flow narrative, entry points, tables/files read & written (each claim with `repo:path:line` pointer), key params and where set, upstream/downstream, known failure points | ~400 lines each |
  | `lineage/<domain>.md` | Table lineage by data domain/prefix, split rule on budget overflow; claims carry pointers | ~300 lines each |
  | `glossary.md` | Org terms, job families, table naming, newbie language | ~150 lines |
  | `errors/index.md` | Error-pattern index: symptom/pattern → dated file + entry (errors are retrieved by symptom, not date) | ~150 lines |
  | `errors/<YYYY-MM>.md` | Dated entries: pattern → confirmed cause → fix (schema §5) | ~300 lines each |
  | `meta/generation.md` | Repos + commit hashes, generated when, coverage gaps, per-repo verification accuracy %, build-state checklist, per-job build-cost log | small |

- [CONFIRMED] (user approved R11) Filename safety: job slugs (lowercase alphanumeric + hyphens, numeric suffix on collision).
- [CANDIDATE] **Pointers, not copies:** chunks hold navigation/lineage/narrative; live repo is the code source of truth. [CONFIRMED] (user approved R11/S3) Excerpts ≤10 lines with pointers — a brevity rule, NOT a privacy control; privacy is handled by content-based redaction (§7).
- [CANDIDATE] **Staleness stamps:** generated files record source commits; Skill B compares to live repo (agent mode) and warns. [CONFIRMED] (user approved R11/S3) Scope: stamps cover CODE only — runtime scheduler state, deployed configs, schemas/stats, out-of-repo params are NOT covered; this caveat is emitted at point-of-use in answers (§5/§6), not only in metadata.
- [CANDIDATE] **Chunk protocol** (in Skill B + copilot-instructions note): read root INDEX first; open ≤3 routed files; verify in live code before concluding; never bulk-read the KB.
- [USER] Regeneration: on demand, by a developer.
- [CONFIRMED] (user approved S7) Home: **dedicated small repo preferred** — keeps stale KB text out of Copilot's implicit context in code repos and keeps KB stamping/diffing clean; final call recorded at M0.

## 4. Skill A — `etl-knowledge-builder` (generator; agent mode required)

- [CONFIRMED] (user approved R4) **Authoritative job seed:** scheduler export or human-maintained job list is the inventory of record; LLM tracing fills per-job detail. If neither exists, the builder creates the list interactively and marks it human-confirmed.
- [CONFIRMED] (user approved S2) **Mechanical cross-checks during build** (instructions in SKILL.md, executed via agent-mode terminal — no shipped scripts): every claimed table read/write is grep-confirmed at the cited site; every entry script's existence is path-confirmed; claims that fail the check are marked unverified in the chunk, never stated as fact.
- [CANDIDATE] Flow per repo: scheduler configs first → confirm inventory against seed → trace each job → cross-check claims → write `jobs/` chunks → `lineage/` → per-repo index → root `INDEX.md` last → stamp commits; record coverage gaps, accuracy findings, and per-job build cost (prompts/tokens/time) in `meta/generation.md`.
- [CONFIRMED] (user approved S2) **Regeneration produces a reviewable diff** (KB lives in git; regen lands as a PR/diff, not a silent overwrite).
- [CANDIDATE] **Resumable builds:** build-state checklist in `meta/generation.md`; sessions may be cut short by limits (R1/R4).
- [CANDIDATE] Incremental mode: regenerate one changed repo's chunks + its index + affected lineage + root index.
- [CANDIDATE] Generation is LLM-driven (library policy: no scripts); accuracy risk mitigated by seed + cross-checks + per-repo owner sampling (§8 M2).

## 5. Skill B — `etl-assistant` (everyday Q&A + RCA)

- [USER] Three jobs: error → root cause + solution; explain a flow; improve this SQL/script.
- [CONFIRMED] (user approved S3) **Artifact-receipt behavior:** when the user pastes/points to a log, plan, or screenshot, the FIRST response runs the safe-to-share checklist and asks confirmation before analysis — newbies paste first and read warnings second.
- [CANDIDATE] **RCA flow:** (1) error (+job name/full log); (2) route via root INDEX → per-repo index → job chunk → LIVE code via pointers; (3) staleness check (agent mode; otherwise declare unchecked, per §1); (4) classify code / data / infra; (5) template: Root cause (plain language) → Evidence (file:line, excerpts ≤10 lines) → Category → Proposed fix (advise-only) → How to verify safely → Confidence + what would raise it → [CONFIRMED] (user approved S3) runtime-state caveat whenever the diagnosis depends on deployed config/schedule/schema ("KB covers code only — verify the live value before acting").
- [CONFIRMED] (user approved R7) **"Insufficient evidence" is required behavior** — say so and list what's missing; guessing is a gate-failing defect.
- [USER] Cause NOT in code: say so plainly, explain why, give step-by-step checks.
- [CONFIRMED] (user approved R5/S5) **Playbook governance:** after user-confirmed root cause, the skill drafts an entry — schema: date, job, symptom/error pattern, confirmed cause, fix, verification evidence, redaction-check done — landing via PR only. Governance completed at M0: named reviewer role, approval criteria, disputed-cause handling (disputed entries stay out or land marked contested), and a named security owner for anything persisted.
- [CANDIDATE] **Explain flow:** route to chunk(s), narrate plainly, cite pointers.
- [CANDIDATE] **Perf-advice flow (static):** artifact + KB context; users with runtime evidence are explicitly told to invoke `spark-performance-advisor`. Boundary: B advises from code, C from runtime evidence.
- [USER] Ops triage mode: deferred.

## 6. Skill C — `spark-performance-advisor` (interactive tuning)

- [USER] Inputs: physical plan text, Spark UI access; full YARN logs exist. Platform believed on-prem YARN [OPEN U1].
- [CONFIRMED] (user approved R11) Intake separates "job failed" (→ Skill B) from "job slow" (this skill).
- [USER] Interview back-and-forth in plain language, then SQL optimization + specific config parameters for the specific scenario.
- [CONFIRMED] (user approved S3) Artifact-receipt behavior as in §5 (checklist first, then analysis).
- [CANDIDATE] Intake teaches fetching missing evidence — including for FINISHED jobs (Spark History Server / event logs; access AND retention are [OPEN] U5) — exact steps depend on U1.
- [CONFIRMED] (both seats, Apache Spark docs) The Spark 3 optimizer is **Adaptive Query Execution (AQE)**, default-ON only since Spark 3.2 (`spark.sql.adaptive.enabled`). Exact minor version is REQUIRED input before config advice.
- [CANDIDATE] Reference files (source-verified against Apache Spark docs for the org's minor version at authoring): physical-plan reading guide; diagnosis playbooks (skew, spill, partition count, join strategy, small files, filter pushdown); config table (parameter → plain meaning → when to change → version notes → job-scoped vs cluster-scoped).
- [CONFIRMED] (user approved R7/S4) **Output template with experiment protocol:** Diagnosis → Why (their evidence) → Fix → Try it in non-prod under the protocol (same input snapshot; cache state and cluster load noted; ≥3 runs; median + p95; agreed minimum-improvement threshold; rollback step; cost-vs-runtime noted; prod-like data scale or the caveat recorded) → Confidence → runtime-state caveat where relevant. Config changes need job-owner approval.
- [USER] Advise-only; never executes against clusters.

## 7. Cross-cutting conventions (all three skills)

- [USER] Newbie contract: no unexplained jargon; terms defined in parentheses on first use; steps assume zero Spark knowledge.
- [CANDIDATE] Honesty contract: evidence + confidence on every conclusion; "I cannot tell from what I have" instead of guessing; staleness/runtime caveats at point-of-use.
- [CONFIRMED] (user approved R5/S3) **Redaction is content-based:** the safe-to-share checklist names content types (secrets, tokens, customer identifiers, raw row values); anything persisted to the KB is stripped of data values regardless of length. Line caps are brevity rules only.
- [CANDIDATE] Library conventions: SKILL.md + references/ + evals/ + SOURCES.md + README, both validators green.
- [CONFIRMED] (user approved R7/S4) Library evals are authoring checks only; **acceptance = a recorded matrix of fixed test cases run inside Copilot across the models and modes the org enables**, with failures logged, at every milestone gate.

## 8. Milestones (no deadline — quality gates)

- [CONFIRMED] (user approved R1/S1/S5/S6/S7/S8) **M0 — feasibility spike + fact lock (blocking):**
  - Verify in org Copilot: agent-feature/skills policy enabled; skills load from `.agents/skills/` (incl. secondary root of a multi-root workspace); whether skills load in ask mode; agent writes files + runs git; observe session depth.
  - **Fact-lock table** recorded in the repo: org billing plan (usage-based vs legacy — GitHub switched to usage-based 2026-06-01) + budget cap; exact Apache Spark minor version; scheduler type (U9); relevant org policies; history-server access + event-log retention (U5); dev config-change permissions (A10).
  - Capture success baseline (3–5 recent incidents' time-to-root-cause). Decide KB home (dedicated repo preferred). Name the adoption owner; adoption deliverables: rollout channel, "which skill do I use?" one-pager with invocation examples, one demo incident, support channel. Complete playbook governance (reviewer role, approval criteria, disputed-cause handling, security owner).
  - Gate: all checks pass or §2 is revisited. **M1 entry criteria: U1, U5, A10 resolved.**
- [CONFIRMED] (user approved R9/S4) **M1 — Skill C first:** one genuinely slow job end-to-end in non-prod under the §6 experiment protocol, owner-approved. Gate: improvement above the agreed threshold, or an honest "no safe improvement found"; rollback documented.
- [CONFIRMED] (user approved R4/S2/S4/S1) **M2 — KB format + Skill A pilot:** one repo, seeded + cross-checked. Owner verifies a random sample — ≥20% of the repo's jobs or ≥10 jobs, whichever is larger — including negative checks (claims that should NOT be there); second-reviewer signoff for high-value jobs; accuracy % and misses recorded. Per-job build cost measured and extrapolated to the full estate — full build green-lit only if affordable. Gate: no undetected wrong lineage in the sample; budgets confirmed/adjusted.
- [CONFIRMED] (user approved R7/S4) **M3 — Skill B:** fixed test set of ≥10 past incidents with known causes, including ≥2 whose cause is NOT in the code and ≥2 designed insufficient-evidence traps. Gate: zero high-confidence wrong answers; every answer cites evidence; traps produce correct "insufficient evidence" responses.
- [USER] Ops triage milestone: deferred.

## 9. Challenges & Risks

- [CONFIRMED] (both round-2 seats, GitHub docs; user approved S1) R1 Cost: GitHub moved Copilot to usage-based (token/AI-credit) billing effective 2026-06-01; the old "1 prompt = 1 premium request" model is legacy. Long, token-heavy KB builds can cost real money. Mitigation: M0 verifies the org's plan + sets a budget cap; M2 measures and extrapolates before the full build; per-repo incremental + resumable builds.
- [CANDIDATE] R2 Staleness: regen-on-demand lags. Mitigation: stamps + point-of-use caveats + live-code verification.
- [CANDIDATE] R3 Confidently-wrong advice: evidence + confidence labels, advise-only, non-prod protocol, owner approval, gates test for it.
- [CANDIDATE] R4 Copilot per-session agentic depth undocumented; builds may cut short. Mitigation: resumable builds; M0 observes limits.
- [CONFIRMED] (docs/COMPATIBILITY.md + both seats) R5 Skills format preview-era churn; re-verify on breakage.
- [CANDIDATE] R6 Oversized inputs: teach extracting relevant sections; accept workspace files.
- [CANDIDATE] R7 KB degenerating into stale code copy: pointers-not-copies + excerpt cap as hard authoring rules.
- [CANDIDATE] R8 Wrong-KB poisoning (the central KB risk): authoritative seed + build-time mechanical cross-checks + per-repo owner sampling with negative checks + regen diffs + declared coverage gaps.
- [CANDIDATE] R9 Skill mis-routing (model-decided): disambiguation descriptions, instructions-file note, cross-trigger evals, invocation examples.

## 10. Remaining Unknowns

- [OPEN] U1 Platform + exact Apache Spark 3.x minor version — M0 fact lock; M1 entry criterion.
- [OPEN] U5 Fetch instructions incl. history-server access AND event-log retention — M0; M1 entry criterion.
- [OPEN] U8 Copilot per-session agentic depth + org billing plan/quota — observed/locked at M0.
- [OPEN] U9 Scheduler type — M0 fact lock (Skill A authoring depends on it).
- [OPEN] U10 Adoption ownership — owner NAMED at M0; deliverables defined in §8.

## 11. Assumptions register (all [OPEN], resolved by M0 unless noted)

- [OPEN] A5 Do the org's Copilot policy controls permit agent features/skills (exact policy name unverified)?
- [OPEN] A6 Does skill discovery work from a secondary folder of a multi-root VS Code workspace?
- [OPEN] A7 Can every dev see/clone all 3–10 repos?
- [OPEN] A8 Are the scheduler configs in the repos COMPLETE (no jobs defined only in the scheduler UI)?
- [OPEN] A9 Do devs have Spark History Server / event-log access for finished jobs (and how long are logs retained)?
- [OPEN] A10 May devs change Spark configs at job scope (vs cluster scope)? — M1 entry criterion.
- [OPEN] A11 Do pasted logs ever contain customer data/secrets (drives redaction strictness)?
--- PLAN ENDS ---

END COUNCIL REVIEW PACKET
