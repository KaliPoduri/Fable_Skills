BEGIN COUNCIL REVIEW PACKET

You are a critical reviewer of a software project plan. You have no other
context; everything you need is below.

Critique this plan on: (1) feasibility, (2) completeness — what unknowns did
the planner miss?, (3) risks, (4) simpler alternatives, (5) fact-hunt:
actively try to refute every named tool, library, API, version, price,
product capability, or legal/compliance claim — flag anything you cannot
verify or suspect is made up.

Reply as a numbered list of major concerns, then minor concerns, then
concrete refinements — most important first. Be specific and brief.

Background for tags used in the plan: `[USER]` = the requesting user said it
in a planning interview; `[CONFIRMED]` = user-approved or verified (basis
noted); `[CANDIDATE]` = planner proposal, must be verified before use;
`[OPEN]` = unresolved question. Untagged lines are headings/formatting.

--- PLAN BEGINS ---

# PLAN.md — Spark ETL Assistant Suite (draft v2, entering council review)

Tags: `[USER]` = said in interview · `[CONFIRMED]` = user-approved or verified (basis noted) · `[CANDIDATE]` = proposal, verify before use · `[OPEN]` = unresolved.
Register: UNKNOWNS.md. Previous plan archived at `archive/2026-06-skills-library-plan/`.

## 1. What we're building

- [USER] Two capabilities for Spark-newbie users: (1) a codebase deep-understanding tool for root-cause analysis of job failures, how-it-works questions, and performance advice on repo artifacts; (2) an interactive Spark log/physical-plan performance advisor.
- [USER] Harness: GitHub Copilot Chat (VS Code, org license) ONLY — the org does not have Claude Code. Org policy allows code and logs in it.
- [USER] Ecosystem: 3–10 repos, hundreds to ~2000 files — SQL, shell scripts, Python/PySpark, scheduler configs, config/params files. Spark 3.x.
- [USER] Users: the dev team (repos cloned, Spark newbies). Support/ops are out of scope for now (deferred by user).
- [USER] Success: #1 correct root causes in minutes not hours; #2 measurable job speedups from the advisor.
- [USER] Constraints: advise-only (never auto-change code), never touch production, no hard deadline. A non-prod environment exists for safe testing.

## 2. Packaging decision

- [CONFIRMED] (user approved) **Three Agent Skills in the existing Fable Skills library** — same repo, SKILL.md conventions, validators, source-verified references, evals, manual-copy distribution:
  - Skill A `etl-knowledge-builder` — a developer runs it to (re)generate the knowledge base from the repos. Batch task, run rarely.
  - Skill B `etl-assistant` — the everyday Q&A skill: paste an error → root cause; ask how a flow works; ask how to improve a repo's SQL/script. Reads the knowledge base.
  - Skill C `spark-performance-advisor` — interactive tuning interview over physical plans / Spark UI evidence.
  - Plus the **knowledge base** — the "deep understanding file", actually a small directory of markdown files (§3). Skill names are placeholders — rename freely.
- [CONFIRMED] (verified against docs/COMPATIBILITY.md, read this session; source-verified 2026-07-06) GitHub Copilot in VS Code reads skills from `.agents/skills/` — the format runs natively in the org's only harness.
- [CANDIDATE] Alternatives rejected: an MCP server or RAG app needs hosting, auth, and daily-coder maintenance the builder doesn't want; a Claude-Code subagent fails the Copilot-only requirement; a plain prompt document can't carry the reference files and chunking protocol these tools need.
- [CANDIDATE] Rationale for splitting "Tool 1" into Skills A+B: generation and consumption have different audiences, triggers, and instructions; one skill doing both would bloat every invocation.
- [CONFIRMED] (per repo handoff notes read this session) Library convention "no scripts inside skills" applies — all three are pure markdown; the LLM does the work at runtime.

## 3. The knowledge base (data model — hardest to change, decided first)

- [USER] Must be chunk-navigable and efficient for LLM parsing — not one huge file; the consuming skill must know how to manage chunks.
- [CANDIDATE] Layout (a directory, proposed name `etl-knowledge/`):

  | File | Contents | Size budget |
  |---|---|---|
  | `INDEX.md` | Ecosystem overview; repo table; job inventory (job → schedule → entry script → repo → 1-line purpose → chunk link); routing guide ("error mentions table T → lineage.md; job J → jobs/J.md") | ~200 lines max |
  | `jobs/<job>.md` | One per job/pipeline: plain-language flow narrative, entry points, tables/files read & written, key params and where set, upstream/downstream jobs, known failure points, `repo:path` pointers | ~400 lines max each |
  | `lineage.md` | Table-level lineage: each table → producing jobs → consuming jobs | grows with tables |
  | `glossary.md` | Org-specific terms, job families, table naming conventions, in newbie language | ~150 lines |
  | `errors/playbook.md` | Error-pattern → confirmed root cause → fix, appended after each resolved incident (with user consent) — the tool's accumulating memory | grows over time |
  | `meta/generation.md` | Which repos at which git commits, when generated, explicit coverage gaps ("could not trace X"), build-state checklist for resumable builds | small |

- [CANDIDATE] **Pointers, not copies:** chunk files hold navigation, lineage, and narrative — never pasted code. The live repo stays the single source of truth for code; this is what makes the knowledge base BETTER than live grep (it holds cross-repo flow knowledge grep can't cheaply reconstruct) instead of a stale copy of what grep already does.
- [CANDIDATE] **Staleness stamps:** every generated file records source commit hashes; the consuming skill compares stamps to the live repo and warns the user when the knowledge base is behind.
- [CANDIDATE] **Chunk protocol** (written into Skill B): (1) always read `INDEX.md` first, nothing else; (2) open at most the 1–3 chunk files the routing guide points to; (3) follow pointers into live code before stating any conclusion about code; (4) never bulk-read the whole knowledge base.
- [USER] Regeneration: on demand, by a developer, when they know things changed.
- [CANDIDATE] Home: a dedicated small repo (or a folder in the primary workspace) that devs clone alongside the code repos — VS Code multi-root workspace makes both visible to Copilot. Decide at M1.

## 4. Skill A — `etl-knowledge-builder` (generator)

- [CANDIDATE] Flow: (1) confirm with the runner which repos and where cloned; (2) per repo, read scheduler configs FIRST to enumerate jobs and dependencies (the interview confirmed these exist in the repos), then trace each job: entry script → SQL/Python it calls → tables read/written → params consumed; (3) write `jobs/` chunks, then `lineage.md`, `glossary.md`, `INDEX.md` last; (4) stamp commits and list coverage gaps honestly in `meta/generation.md`.
- [USER] Builds run in GitHub Copilot Chat — the org's only harness.
- [CANDIDATE] **Resumable builds:** Copilot Chat sessions may be too short for a full 10-repo build in one sitting — `meta/generation.md` keeps a build-state checklist (repo/job done or pending) so a build continues across sessions instead of restarting.
- [CANDIDATE] Incremental mode: regenerate only the chunks belonging to one changed repo, refresh `INDEX.md`/`lineage.md`; keeps on-demand regen cheap.
- [CANDIDATE] Generation is LLM-driven (the agent reads and traces; no parser program to maintain) — fits a builder who codes a little; cost is long agent sessions per full build (risk R1, mitigated by per-repo batches + resumable builds).

## 5. Skill B — `etl-assistant` (everyday Q&A + RCA)

- [USER] Three jobs in one skill (from original request): error → root cause + solution; how does functionality/flow X work; how to improve this SQL/script.
- [CANDIDATE] **RCA flow:** (1) take the pasted error (and job name if known; full log file if available — the interview confirmed both exist); (2) route via `INDEX.md` → job chunk → follow pointers into LIVE code; (3) check staleness stamp, warn if behind; (4) classify cause as code / data / infra; (5) answer in a fixed template: Root cause (plain language) → Evidence (file:line) → Category → Proposed fix (advise-only) → How to verify safely → Confidence (high/medium/low) and what would raise it.
- [USER] When the cause is NOT in the code: say so plainly, explain why, and give step-by-step checks the user can run (data file, upstream job, cluster).
- [CANDIDATE] After a root cause is CONFIRMED by the user, offer to append the case to `errors/playbook.md` — future incidents with matching patterns resolve faster.
- [CANDIDATE] **Explain flow:** route to job chunk(s), narrate the flow in plain language, cite file pointers for the curious.
- [CANDIDATE] **Perf-advice flow (static):** for "make this SQL/script better" questions, analyze the artifact plus its context from the knowledge base (data volumes unknown → ask), and hand off to Skill C when the user has runtime evidence (a plan, UI timings). Boundary: Skill B advises from code, Skill C from runtime evidence.
- [USER] Ops triage mode: deferred — out of scope for now.

## 6. Skill C — `spark-performance-advisor` (interactive tuning)

- [USER] Inputs users can obtain: physical plan text (copy-paste) and Spark UI access; full YARN logs also exist. Platform believed on-prem YARN [OPEN U1]; Spark 3.x confirmed.
- [USER] Must interview the user back-and-forth in plain language before prescribing, then deliver: SQL optimization + specific config parameters for the specific scenario.
- [CANDIDATE] **Intake interview** (one question at a time, newbie-phrased): which job, what symptom (slow / failing / out-of-memory), what evidence they have; if they lack it, TEACH how to fetch it (where the Spark UI is, how to get a plan) — fetch steps depend on platform verification [OPEN U1, U5].
- [CANDIDATE] **Reference files** (each source-verified against official Spark 3.x docs at authoring time, per library convention): how to read a physical plan (what the common operators mean in plain words — joins, shuffles/Exchange, scans); diagnosis playbooks for the classic problems (data skew, memory spill, too many/too few partitions, wrong join strategy, small-files, missing filter pushdown); a config reference table (parameter → what it does in plain language → when to change → Spark 3.x notes, e.g. the adaptive query engine) — every named parameter and capability is [CANDIDATE] verify-before-use until authored against docs.
- [CANDIDATE] **Output template:** Diagnosis (plain language, jargon defined on first use) → Why (evidence from their plan/UI) → Fix: SQL rewrite and/or config change → How to try it in the non-prod environment → How to measure the improvement → Confidence.
- [USER] A non-prod environment exists — "try it safely" steps target it.
- [USER] Advise-only; never executes anything against clusters.

## 7. Cross-cutting conventions (all three skills)

- [USER] Newbie contract: no unexplained jargon; every technical term defined in parentheses on first use; step-by-step instructions assume zero Spark knowledge.
- [CANDIDATE] Honesty contract: every conclusion carries evidence and a confidence label; the skill says "I cannot tell from what I have" instead of guessing; staleness warnings are mandatory, not optional.
- [CANDIDATE] Library conventions: SKILL.md + references/ + evals/ structure, both validators green, source-verified references with SOURCES.md, README per skill — as the existing 23 skills do.

## 8. Build order (no deadline — quality gates instead)

- [CANDIDATE] M1: knowledge-base format spec + Skill A; generate the knowledge base for ONE pilot repo in Copilot Chat; builder eyeballs it for accuracy. Gate: pilot INDEX + chunks judged accurate by someone who knows the pipeline; knowledge-base home decided.
- [CANDIDATE] M2: Skill B; test against a handful of PAST failures whose true root cause is known. Gate: majority correctly diagnosed, zero confidently-wrong answers.
- [CANDIDATE] M3: Skill C; test on one genuinely slow job end-to-end (advice applied by a human in the non-prod environment, effect measured). Gate: measured improvement or an honest "no safe improvement found".
- [USER] Ops triage milestone: deferred (out of scope for now).

## 9. Challenges & Risks

- [CANDIDATE] R1 Generation cost/length: a full build over up to 10 repos spans multiple long Copilot Chat sessions. Mitigation: per-repo incremental builds, scheduler-configs-first tracing, resumable build-state checklist.
- [CANDIDATE] R2 Staleness: regen-on-demand means the knowledge base WILL lag the repos. Mitigation: commit stamps + mandatory warnings + Skill B must verify in live code before concluding.
- [CANDIDATE] R3 Confidently-wrong advice applied by newbies. Mitigation: evidence + confidence labels, advise-only, non-prod testing, M2/M3 gates test for it.
- [CANDIDATE] R4 Copilot Chat agent limits: session length, context size, and per-session file-reading depth are undocumented — flows must assume short sessions and small context; chunk budgets and resumable builds exist for this.
- [CONFIRMED] (compatibility doc read this session) R5 Skills format is preview-era and churns; paths and limits re-verified on breakage per library process.
- [CANDIDATE] R6 Oversized inputs: physical plans and logs can exceed what a user can paste. Mitigation: skills teach extracting the relevant section; accept files placed in the workspace.
- [CANDIDATE] R7 Knowledge base degenerating into a stale code copy. Mitigation: pointers-not-copies rule is a hard authoring rule for Skill A.

## 10. Remaining Unknowns

- [OPEN] U1 Platform verification: is it really on-prem Hadoop/YARN, and which Spark 3.x minor version? (Affects config advice and every fetch-instruction.)
- [OPEN] U5 Exact log/plan/UI fetch instructions — blocked on U1.
- [OPEN] U8 Copilot Chat practical limits (session length, context, agentic depth) — discovered empirically at M1; shapes chunk budgets.
- Resolved this round: U4 (ops deferred), U6 (non-prod env exists), U7 (single harness now).

## 11. Assumptions register

- All previous assumptions resolved: A1 no — Copilot Chat only (org has no Claude Code); A2 ops deferred, dev team targeted; A3 yes — non-prod env exists; A4 yes — Fable Skills library (packaging approved).
- No unconfirmed assumptions currently registered.

--- PLAN ENDS ---

END COUNCIL REVIEW PACKET
