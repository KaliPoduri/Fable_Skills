# PLAN.md — Spark ETL Assistant Suite (draft v3, after council round 1)

Tags: `[USER]` = said in interview · `[CONFIRMED]` = user-approved or verified (basis noted) · `[CANDIDATE]` = proposal, verify before use · `[OPEN]` = unresolved.
Register: UNKNOWNS.md. Council log: council/LOG.md. Previous plan archived at `archive/2026-06-skills-library-plan/`.

## 1. What we're building

- [USER] Two capabilities for Spark-newbie users: (1) a codebase deep-understanding tool for root-cause analysis of job failures, how-it-works questions, and performance advice on repo artifacts; (2) an interactive Spark log/physical-plan performance advisor.
- [USER] Harness: GitHub Copilot in VS Code (org license) ONLY — the org does not have Claude Code. Org policy allows code and logs in it.
- [CONFIRMED] (both council seats verified against GitHub/VS Code docs; user approved R2) Skills load in agent-capable Copilot surfaces; Skill A additionally REQUIRES Copilot **agent mode** (only agent mode writes files and runs terminal commands) and that the org's Copilot policy has Agent Skills enabled. In ask mode, skills must state which checks they could not run (e.g. "staleness unchecked") instead of silently skipping them.
- [USER] Ecosystem: 3–10 repos, hundreds to ~2000 files — SQL, shell scripts, Python/PySpark, scheduler configs, config/params files. Spark 3.x ([OPEN] U1: exact minor version).
- [USER] Users: the dev team (repos cloned, Spark newbies). Support/ops are out of scope for now (deferred by user).
- [USER] Success: #1 correct root causes in minutes not hours; #2 measurable job speedups from the advisor.
- [CONFIRMED] (user approved R7) Baseline: at M0, record the actual time-to-root-cause of 3–5 recent incidents, so success #1 is measurable against something real.
- [USER] Constraints: advise-only, never touch production, no hard deadline. A non-prod environment exists for safe testing.
- [CONFIRMED] (user approved R11) "Advise-only" clarified: never auto-change application code; writing knowledge-base/doc files when the user asks for it is allowed.

## 2. Packaging

- [CONFIRMED] (user approved) **Three Agent Skills in the existing Fable Skills library** — same repo, SKILL.md conventions, validators, source-verified references, evals, manual-copy distribution:
  - Skill A `etl-knowledge-builder` — a developer runs it (agent mode) to (re)generate the knowledge base. Batch task, run rarely.
  - Skill B `etl-assistant` — everyday Q&A: paste an error → root cause; how does flow X work; improve this SQL/script (static analysis).
  - Skill C `spark-performance-advisor` — interactive tuning interview over runtime evidence (physical plans, Spark UI).
  - Plus the **knowledge base** — a sharded directory of markdown files (§3).
- [CONFIRMED] (user approved R11) Skill names above are fixed unless the user renames them by M0 exit — stable names before any evals are written.
- [CONFIRMED] (both seats verified against GitHub/VS Code docs) Copilot in VS Code reads project skills from `.agents/skills/` (also `.github/skills/`, `.claude/skills/`); the feature is recent and still marked experimental in places — re-verify on breakage (risk R5).
- [CONFIRMED] (user approved R8) **Routing hardening** (Copilot picks skills by model judgment, not deterministically): each skill description carries a disambiguation line naming when to use the OTHER skills; a short routing + chunk-protocol note is added to each code repo's `copilot-instructions.md` / `AGENTS.md` [CANDIDATE mechanism — verify file name/behavior at M0]; evals include cross-trigger cases; "handoff" between skills means explicitly telling the user which skill to invoke next — no automatic handoff exists.
- [CANDIDATE] Alternatives rejected in round 1 (user arbitrated): MCP server / RAG app (hosting + maintenance burden), Claude-Code subagent (wrong harness), plain prompt doc (can't carry references/protocol). The Codex seat's "use Copilot's native repo indexing / Spaces instead of a generated KB" was REJECTED by the user — no native-context trial; the generated KB stands.
- [CONFIRMED] (per repo handoff notes read this session) Library convention "no scripts inside skills" applies — all three are pure markdown.
- [CANDIDATE] Distribution stays manual-copy (library decision); GitHub's `gh skill` CLI install path exists but is public preview (requires GitHub CLI ≥2.90) — not relied on.

## 3. The knowledge base (sharded data model)

- [USER] Must be chunk-navigable and efficient for LLM parsing — never one huge file.
- [CONFIRMED] (user approved R3) Sharded layout (directory `etl-knowledge/`, all budgets [CANDIDATE] to tune at M2):

  | File | Contents | Budget |
  |---|---|---|
  | `INDEX.md` | THIN root: ecosystem overview, repo table with links to per-repo indexes, routing guide ("error names table T → lineage/<domain>.md; job J → jobs/<job>.md") | ~100 lines |
  | `repos/<repo>-index.md` | Per-repo job inventory: job → schedule → entry script → 1-line purpose → chunk link | ~150 lines each |
  | `jobs/<job>.md` | Per job: plain-language flow narrative, entry points, tables/files read & written, key params and where set, upstream/downstream jobs, known failure points, `repo:path` pointers | ~400 lines each |
  | `lineage/<domain>.md` | Table lineage split by data domain / table prefix, with a split rule when a file exceeds budget | ~300 lines each |
  | `glossary.md` | Org terms, job families, table naming, newbie language | ~150 lines |
  | `errors/<YYYY-MM>.md` | Error-pattern → confirmed cause → fix, dated files, split monthly | ~300 lines each |
  | `meta/generation.md` | Repos + commit hashes, when generated, coverage gaps, sample-verification accuracy %, build-state checklist (resumable builds) | small |

- [CONFIRMED] (user approved R11) Filename safety: job chunk files use a slug (lowercase alphanumeric + hyphens); collisions get a numeric suffix; slug↔real-name mapping lives in the per-repo index.
- [CANDIDATE] **Pointers, not copies:** chunks hold navigation, lineage, and narrative — the live repo stays the source of truth. [CONFIRMED] (user approved R11) Evidence excerpts are allowed but capped (~10 lines, always with a `repo:path:line` pointer, never whole files).
- [CANDIDATE] **Staleness stamps:** every generated file records source commit hashes; Skill B compares them to the live repo (agent mode) and warns when behind. [CONFIRMED] (user approved R11) Scope statement inside the KB: stamps cover CODE at those commits only — runtime scheduler state, deployed configs, table schemas/stats, and out-of-repo parameters are NOT covered.
- [CANDIDATE] **Chunk protocol** (in Skill B, and summarized in `copilot-instructions.md` per R8): (1) read root `INDEX.md` first, nothing else; (2) open at most the 1–3 files the routing guide points to; (3) follow pointers into live code before any conclusion about code; (4) never bulk-read the KB.
- [USER] Regeneration: on demand, by a developer, when they know things changed.
- [CANDIDATE] Home: dedicated small repo or a folder in the primary workspace, cloned alongside code repos (multi-root workspace) — decided at M0 after the discovery test.

## 4. Skill A — `etl-knowledge-builder` (generator; agent mode required)

- [CONFIRMED] (user approved R4) **The job inventory is seeded from authority, not inferred:** a scheduler export or a human-maintained job list is the input of record; LLM tracing fills in details per job. If neither exists, the builder creates the list interactively with the runner and marks it human-confirmed.
- [CANDIDATE] Flow per repo: read scheduler configs first → confirm inventory against the authoritative seed → trace each job (entry script → SQL/Python called → tables read/written → params consumed) → write `jobs/` chunks → `lineage/` → per-repo index → root `INDEX.md` last → stamp commits, record coverage gaps and accuracy findings in `meta/generation.md`.
- [CANDIDATE] **Resumable builds:** `meta/generation.md` keeps a build-state checklist (repo/job done or pending) so a build continues across sessions instead of restarting; sessions may be cut short by quota or session limits (risk R1/R4).
- [CANDIDATE] Incremental mode: regenerate only one changed repo's chunks; refresh its per-repo index, affected lineage files, and the root index.
- [CANDIDATE] Generation is LLM-driven (no parser program to maintain — library forbids scripts in skills); the accuracy risk this creates is mitigated by the authoritative seed (above) and the M2 sample-verification gate (§8).

## 5. Skill B — `etl-assistant` (everyday Q&A + RCA)

- [USER] Three jobs in one skill: error → root cause + solution; explain a functionality/flow; improve this SQL/script.
- [CANDIDATE] **RCA flow:** (1) take the pasted error (plus job name / full log if available); (2) run the safe-to-share checklist (§7) before the user pastes logs; (3) route via root INDEX → per-repo index → job chunk → follow pointers into LIVE code; (4) check staleness stamps (agent mode; in ask mode say "staleness unchecked"); (5) classify cause code / data / infra; (6) fixed answer template: Root cause (plain language) → Evidence (file:line, excerpts ≤10 lines) → Category → Proposed fix (advise-only) → How to verify safely → Confidence (high/medium/low) and what would raise it.
- [CONFIRMED] (user approved R7) **"Insufficient evidence" is a required behavior:** when the inputs don't support a conclusion, the skill must say so and list what's missing — guessing is a gate-failing defect.
- [USER] When the cause is NOT in the code: say so plainly, explain why, give step-by-step checks (data file, upstream job, cluster).
- [CONFIRMED] (user approved R5) **Playbook governance:** after the user confirms a root cause, the skill drafts an entry — fixed schema: date, job, symptom/error pattern, confirmed cause, fix, verification evidence, redaction-check done — and the entry lands via a pull request, never a direct append. Data values are stripped before anything persists.
- [CANDIDATE] **Explain flow:** route to job chunk(s), narrate in plain language, cite pointers.
- [CANDIDATE] **Perf-advice flow (static):** analyze the artifact plus KB context; when the user has runtime evidence (plan, UI timings), explicitly tell them to invoke `spark-performance-advisor` (no automatic handoff — R8). Boundary: B advises from code, C from runtime evidence.
- [USER] Ops triage mode: deferred.

## 6. Skill C — `spark-performance-advisor` (interactive tuning)

- [USER] Inputs users can obtain: physical plan text and Spark UI access; full YARN logs also exist. Platform believed on-prem YARN [OPEN U1].
- [CONFIRMED] (user approved R11) **Intake separates "job failed" from "job slow"** — different evidence, different flow; failed-job root-causing is Skill B's territory (the intake says so and points there).
- [USER] Interview back-and-forth in plain language before prescribing; then deliver SQL optimization + specific config parameters for the specific scenario.
- [CANDIDATE] Intake (one question at a time, newbie-phrased): which job, symptom, what evidence they have; TEACH how to fetch missing evidence — including for FINISHED jobs (Spark History Server / event logs [CANDIDATE verify names and access at M0/U1]) — exact steps depend on platform [OPEN U1, U5].
- [CONFIRMED] (verified by both council seats against Apache Spark docs) The Spark 3 auto-optimizer is **Adaptive Query Execution (AQE)** and it is default-ON only since Spark 3.2 — earlier 3.x has it off by default. The exact minor version is therefore a REQUIRED input for config advice: the skill asks for it (or how to find it) before prescribing configs.
- [CANDIDATE] Reference files (each source-verified against official Spark docs for the org's minor version at authoring time): physical-plan reading guide (operators in plain words); diagnosis playbooks (skew, spill, partition count, join strategy, small files, filter pushdown); config reference table (parameter → plain-language meaning → when to change → version notes; job-scoped vs cluster-scoped flagged per parameter).
- [CONFIRMED] (user approved R7) **Output template with measurement:** Diagnosis → Why (their evidence) → Fix (SQL and/or config) → How to try it in non-prod (baseline = repeated runs, not one) → Minimum improvement worth keeping + rollback step → Confidence. Config changes need the job owner's approval before applying anywhere.
- [CONFIRMED] (user approved R5) Safe-to-share checklist runs before the user pastes plans/logs/screenshots.
- [USER] Advise-only; never executes anything against clusters.

## 7. Cross-cutting conventions (all three skills)

- [USER] Newbie contract: no unexplained jargon; every technical term defined in parentheses on first use; steps assume zero Spark knowledge.
- [CANDIDATE] Honesty contract: every conclusion carries evidence and a confidence label; "I cannot tell from what I have" instead of guessing; staleness warnings mandatory (or "unchecked" declared in ask mode).
- [CONFIRMED] (user approved R5) **Redaction rules:** a safe-to-share checklist (does this log/plan contain customer identifiers, secrets, tokens, data values?) runs before users paste artifacts; data values are stripped before ANY content persists to the KB.
- [CANDIDATE] Library conventions: SKILL.md + references/ + evals/ structure, both validators green, SOURCES.md per skill, README per skill — as the existing 23 skills.
- [CONFIRMED] (user approved R7) Library evals do not validate the target harness — every milestone gate includes smoke tests run INSIDE Copilot (across the models the org actually enables).

## 8. Milestones (reordered per R9 — no deadline, quality gates instead)

- [CONFIRMED] (user approved R1) **M0 — feasibility spike (blocking, ~half a day):** in org Copilot agent mode verify: Agent Skills enabled by org policy; skills load from `.agents/skills/` (including from a secondary folder of a multi-root workspace); the agent can write files and run git; observe real session depth/limits. Also capture the success baseline (3–5 recent incidents' time-to-root-cause) and decide the KB home. Gate: all checks pass, or the plan's packaging section is revisited.
- [CONFIRMED] (user approved R9) **M1 — Skill C first** (no KB dependency, fastest measurable win). Gate [CANDIDATE thresholds]: one genuinely slow job tested end-to-end in non-prod — baseline from repeated runs, advice applied by a human with owner approval, measured improvement above an agreed threshold, or an honest "no safe improvement found"; rollback documented.
- [CONFIRMED] (user approved R4) **M2 — KB format + Skill A pilot:** one repo, seeded from the authoritative job list; a pipeline owner verifies a random sample of jobs (inputs, outputs, lineage) against ground truth; accuracy % and misses recorded in `meta/generation.md`. Gate [CANDIDATE threshold]: no undetected wrong lineage in the sample; format budgets confirmed or adjusted.
- [CONFIRMED] (user approved R7) **M3 — Skill B:** tested against a FIXED set of past incidents with known root causes. Gate: zero high-confidence wrong answers; every answer cites evidence; incidents the tool can't resolve produce a correct "insufficient evidence" response.
- [USER] Ops triage milestone: deferred.

## 9. Challenges & Risks

- [CONFIRMED] (Claude seat, GitHub billing docs; user approved R6) R1 Build cost model: one agent-mode user prompt = 1 premium request (tool calls within it are not billed separately), but org premium-request quotas and short-term rate limits can stall multi-session builds. Mitigation: per-repo incremental builds, resumable build-state checklist.
- [CANDIDATE] R2 Staleness: regen-on-demand means the KB WILL lag. Mitigation: stamps + mandatory warnings + live-code verification + explicit scope statement (stamps cover code only).
- [CANDIDATE] R3 Confidently-wrong advice applied by newbies. Mitigation: evidence + confidence labels, advise-only, non-prod testing, owner approval for configs, M1–M3 gates test for it.
- [CANDIDATE] R4 Copilot per-session agentic depth is genuinely undocumented; sessions may cut builds short. Mitigation: resumable builds; M0 observes real limits.
- [CONFIRMED] (docs/COMPATIBILITY.md + both seats) R5 Skills format is preview-era/experimental and churns; re-verify on breakage.
- [CANDIDATE] R6 Oversized inputs (plans/logs exceed paste limits). Mitigation: teach extracting the relevant section; accept files placed in the workspace.
- [CANDIDATE] R7 KB degenerating into a stale code copy. Mitigation: pointers-not-copies + excerpt cap are hard authoring rules.
- [CANDIDATE] R8 Wrong-KB poisoning (bigger than staleness): LLM tracing errors mislead every later answer. Mitigation: authoritative job seed, owner sample-verification at M2, coverage gaps declared, accuracy % recorded.
- [CANDIDATE] R9 Skill mis-routing (model-decided): mitigated by disambiguation descriptions, copilot-instructions note, cross-trigger evals.

## 10. Remaining Unknowns

- [OPEN] U1 Platform + exact Spark 3.x minor version (blocking for Skill C's config table; AQE default flipped at 3.2). Verify with the platform team.
- [OPEN] U5 Exact log/plan/UI fetch instructions, incl. history server access for finished jobs — blocked on U1.
- [OPEN] U8 Copilot per-session agentic depth + org premium-request quota — observed at M0.
- [OPEN] U9 Which scheduler (the tracing instructions differ by scheduler type) — determined at M0/M2 from the repos themselves.
- [OPEN] U10 Adoption: how the dev team discovers/learns the skills; owner and channel undecided.

## 11. Assumptions register (all [OPEN], phrased as questions, mostly resolved by M0)

- [OPEN] A5 Is Copilot agent mode (and the Agent Skills feature) enabled by the org's Copilot policy?
- [OPEN] A6 Does skill discovery work from a secondary folder of a multi-root VS Code workspace?
- [OPEN] A7 Can every dev see/clone all 3–10 repos?
- [OPEN] A8 Are the scheduler configs in the repos COMPLETE (no jobs defined only inside the scheduler UI)?
- [OPEN] A9 Do devs have Spark History Server / event-log access for finished jobs?
- [OPEN] A10 May devs change Spark configs at job scope (vs cluster scope, which needs admins)?
- [OPEN] A11 Do pasted logs ever contain customer data/secrets (drives how strict the redaction checklist must be)?
