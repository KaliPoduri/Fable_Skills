# Round 2 Critique — Claude seat (verbatim)

## PART 1 — Cross-examination verdicts

**1. Skill A feasibility (authoritative seed + sample gate) — AGREE WITH CHANGE.**
The concern is accepted, but the mitigation covers the wrong half of the risk. The authoritative seed fixes *inventory completeness* (which jobs exist); it does nothing for *per-job tracing accuracy* (tables read/written, params, lineage) — which is where LLM omissions and false lineage actually occur. The M2 sample gate detects systematic error rates but not long-tail per-job errors, and a one-repo pilot doesn't transfer statistical confidence to the other 2–9 repos. Different fix, within the no-scripts constraint: the "no scripts inside skills" rule forbids *shipping* a parser, but Skill A runs in agent mode with terminal access — the SKILL.md can *instruct* mechanical cross-checks at build time (e.g., for every table the trace claims is written, grep the repos for that table name and confirm the write site; for every job, confirm the entry script exists at the claimed path). That converts pure-LLM tracing into LLM-tracing-with-mechanical-verification without violating the library rule. Also require every lineage claim to carry a `repo:path:line` pointer so a wrong claim is auditable, and repeat owner sampling per repo, not only at the M2 pilot.

**2. Staleness scope statement — AGREE WITH CHANGE.**
The concern stands; the fix is honest labeling rather than mitigation, and labeling buried in the KB (`meta/generation.md` scope statement) will never be seen by the Spark-newbie reading an answer. Different fix: push the disclosure to point-of-use — Skill B's and C's answer templates should emit a standing caveat whenever a diagnosis depends on runtime state ("KB covers code only; verify the actual deployed config/schedule/schema before acting"). Combined with the existing live-code verification step and the code/data/infra classification, the residual risk is acceptable for an advise-only tool.

**3. KB-first approach on its own terms — AGREE (it holds together), with two caveats.**
Given the native-indexing trial is settled by user decision, the design is internally coherent: authoritative seed → sharded chunks → pointers-not-copies → chunk protocol → staleness stamps → gated milestones. Caveats: (a) the whole KB's value is hostage to R1/R4 (build sessions completing) and to the M2 accuracy gate — if either fails, Skill B degrades to what native context would have given anyway; (b) chunk-protocol adherence is model-judgment, not enforceable — nothing stops Copilot from answering from its own retrieval and ignoring the KB, so the copilot-instructions routing note and cross-trigger evals are load-bearing, not nice-to-have.

## PART 2 — Fresh review

### Major concerns

1. **R1's cost model is stale — [CONFIRMED] basis has been superseded.** GitHub docs now label premium-request billing "(legacy)"; GitHub moved Copilot to usage-based billing starting June 1, 2026 (before today's date). "One agent-mode prompt = 1 premium request" was accurate when written but the org may now be on usage-based billing with different quota/stall behavior. Re-verify at M0 which billing model the org is on; U8 as phrased ("premium-request quota") may be the wrong question.
2. **The ask-mode fallback may be unenforceable.** The plan says skills load in "agent-capable surfaces" yet requires ask-mode skills to declare "staleness unchecked." If skills don't load in ask mode at all (likely — VS Code documents Agent Skills as an agent feature), that declaration can never execute. Verify at M0; if skills don't load in ask mode, drop the ask-mode language and state "agent mode required" in adoption material.
3. **Gate sets have no minimum sizes.** M3's "fixed set of past incidents" and M2's "random sample of jobs" are unquantified — "zero high-confidence wrong answers" over 3 incidents is near-meaningless. Specify N (e.g., M3: ≥10 incidents including ≥2 not-in-code causes and ≥2 designed insufficient-evidence cases; M2: sample ≥20% of jobs or ≥10 jobs, whichever is larger).
4. **Full-build effort is unestimated.** Hundreds of jobs × ~400-line chunks, generated in interactive agent sessions with per-command approvals, could mean days-to-weeks of supervised dev time across 3–10 repos. Add to M2: measure prompts/time per job on the pilot repo and extrapolate before committing to the full build — this may change the incremental-build strategy or the budget per chunk.
5. **KB home should bias toward a dedicated repo.** Left [OPEN] to M0, but one deciding factor is already known: a KB folder inside the primary workspace risks Copilot's implicit context pulling stale KB content into answers outside the chunk protocol, and complicates staleness stamping (KB commits interleaved with code commits). Note this bias in the plan.

### Minor concerns

6. `errors/<YYYY-MM>.md` is organized by date but retrieved by symptom — routing "error → this month's file" fails for recurring errors confirmed months ago. Add an error-pattern index (or organize by error family with dated entries).
7. Playbook PR governance names no reviewer. Who approves playbook PRs, and what stops a wrong "confirmed cause" from landing? U10 covers adoption, not review authority.
8. Redaction checklist ordering: newbies will paste first, read the checklist second. Skill B/C should be instructed that, on receiving an artifact, the *first* response re-runs the checklist and asks for confirmation before analysis — behavioral ordering, not just a pre-paste rule.
9. U9 (scheduler type) is slated for M0/M2, but Skill A's flow starts "read scheduler configs first" and A8 (are configs complete in repos?) can invalidate that step. Resolve U9 at M0, since Skill A's authoring depends on it.
10. Spark History Server event-log *retention* is a hidden dependency: finished-job evidence may already be purged when the user asks. Add retention to U5.
11. M1's measured improvement runs in non-prod; data volumes there may not reproduce the skew/spill that made the job slow in prod. Gate should require prod-like data scale or record the caveat.
12. The [CONFIRMED] wording "only agent mode writes files and runs terminal commands" is slightly wrong: edit mode also writes files (no terminal). Conclusion (Skill A needs agent mode) is unaffected; fix the wording.

### Fact-hunt

- `.agents/skills/`, `.github/skills/`, `.claude/skills/` discovery in VS Code Copilot — **verified** (VS Code docs; GitHub changelog Dec 18, 2025). "Recent/experimental" framing is accurate.
- `gh skill` public preview requiring GitHub CLI ≥ 2.90 — **verified** (GitHub changelog Apr 16, 2026). Plan doesn't rely on it; note it now exists as a future alternative to manual copy.
- "1 premium request per agent-mode prompt; tool calls not billed" — **was accurate, now legacy**: request-based billing docs are marked legacy; usage-based billing effective June 1, 2026. This is the one [CONFIRMED] claim the plan should re-open (major concern 1).
- AQE default-ON only since Spark 3.2 (`spark.sql.adaptive.enabled`) — **verified**; earlier 3.x default off. The minor-version-required logic in Skill C is sound.
- Spark History Server / event logs for finished jobs — real feature names; access/retention correctly left to U1/U5.
- `copilot-instructions.md` / `AGENTS.md` — both are real Copilot instruction mechanisms; plan correctly marks the exact behavior [CANDIDATE] for M0.
- "Copilot picks skills by model judgment, not deterministically" — consistent with documented behavior (skills load on demand from descriptions).
- Multi-root-workspace skill discovery (A6) — could not verify in docs either way; correctly held [OPEN] and tested at M0.
- "Only agent mode writes files and runs terminal commands" — **partially refuted** (edit mode writes files); see minor concern 12.

Sources: VS Code docs (agent skills); GitHub changelogs 2025-12-18 and 2026-04-16; gh skill manual; GitHub docs premium-requests (legacy) and copilot-requests; GitHub blog ask/edit/agent modes.

### Concrete refinements (most important first)

1. Re-verify the Copilot billing model at M0 (usage-based switch, June 2026); rewrite R1/U8 in terms of whatever model the org is actually on.
2. Add instructed mechanical cross-checks to Skill A's build flow (agent-mode grep per claimed table/entry-point to confirm read/write sites) — respects the no-scripts rule, directly attacks false lineage.
3. Move the runtime-state scope caveat into Skill B/C answer templates (point-of-use), keeping the KB scope statement as secondary.
4. Quantify M2 sample size and M3 incident-set size; include designed "insufficient evidence" and "cause not in code" cases in M3.
5. At M2, measure per-job build cost (prompts, wall time) on the pilot repo and extrapolate before green-lighting the full build.
6. Bias the KB-home decision toward a dedicated repo (context isolation + clean staleness stamping); record the rationale.
7. Add an error-pattern index over the dated `errors/` files.
8. Name the playbook-PR reviewer role and add it to U10's adoption ownership question.
