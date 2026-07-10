# Council LOG — Spark ETL Assistant Suite plan

## Round 1 (packet: round-1-packet.md; critiques: round-1-critique-claude.md, round-1-critique-codex.md)

Seats: Claude (general-purpose subagent, model fable) + Codex (task-mrex7lqb-31z0ye, session 019f4c08-6acd-7011-b619-407f8e543ff8). Both returned full critiques; both fact-checked against GitHub/VS Code and Apache Spark docs.

Merged into 11 refinements; user verdicts:

| # | Refinement | Raised by | Verdict |
|---|---|---|---|
| R1 | M0 feasibility spike (agent mode, .agents/skills loading, multi-root, write/git, session depth) | both | ACCEPTED |
| R2 | State agent-mode requirement + ask-mode fallbacks ("staleness unchecked") | both | ACCEPTED |
| R3 | Shard KB: thin root index, per-repo indexes, lineage by domain, dated playbook files | both | ACCEPTED |
| R4 | Authoritative job inventory seed + owner sample-verification M-gate with recorded accuracy % | both | ACCEPTED |
| R5 | Redaction: safe-to-share checklist, strip data values, playbook via PR with fixed schema | both | ACCEPTED |
| R6 | Fact fixes: AQE naming + default-on only since Spark 3.2 (minor version now blocking); Copilot billing/limits wording | both | ACCEPTED |
| R7 | Measurable gates: fixed incident test set, zero high-confidence wrong, insufficient-evidence behavior, baseline capture, repeated-run measurement + rollback; smoke tests inside Copilot | both | ACCEPTED |
| R8 | Routing hardening: disambiguation descriptions, copilot-instructions note, cross-trigger evals, explicit re-ask handoff | Claude | ACCEPTED |
| R9 | Reorder: Skill C first, then KB pilot, then Skill B | Claude | ACCEPTED |
| R10 | Trial Copilot native repo indexing/Spaces vs generated KB | Codex | REJECTED (user: keep the generated-KB approach; no comparison trial) |
| R11 | Small fixes: staleness scope statement, filename slugs, excerpt cap, failed-vs-slow intake split, history-server fetch steps, advise-only clarification, stable names, restored assumptions register | both | ACCEPTED |

Applied to PLAN.md v3. New opens: U9 (scheduler type), U10 (adoption); assumptions A5–A11 registered.

## Round 2 (packets: round-2-packet-claude.md / round-2-packet-codex.md; critiques: round-2-critique-claude.md / round-2-critique-codex.md)

Cross-examination tally — all 6 carried points SETTLED, none disputed:
- Claude on Codex's points: (1) Skill A feasibility — AGREE WITH CHANGE (add build-time mechanical cross-checks, pointers on lineage claims, per-repo sampling → S2); (2) staleness scope — AGREE WITH CHANGE (point-of-use caveats → S3); (3) KB-first holds — AGREE (caveats noted).
- Codex on Claude's points: (1) smoke tests — AGREE WITH CHANGE (acceptance matrix by model/mode → S4); (2) adoption — AGREE (plan now → S5); (3) routing — AGREE WITH CHANGE (invocation examples + fail-closed tests → S8/S5).

Fresh-review merge → 8 refinements; user verdicts (all ACCEPTED):

| # | Refinement | Raised by | Verdict |
|---|---|---|---|
| S1 | Cost model refresh: usage-based billing since 2026-06-01 (verified both seats); M0 billing check + budget cap; M2 per-job cost extrapolation | both | ACCEPTED |
| S2 | KB build cross-checks: instructed grep verification, pointers on claims, per-repo sampling, regen diffs | both | ACCEPTED |
| S3 | Point-of-use safety: runtime caveat in answers; content-based redaction; checklist-first on artifact receipt | both | ACCEPTED |
| S4 | Quantified gates: M3 ≥10 incidents (+traps), M2 ≥20%/≥10 jobs + negative checks + 2nd reviewer, M1 experiment protocol, acceptance matrix | both | ACCEPTED |
| S5 | Adoption at M0: owner, channel, one-pager, demo, support; playbook governance completed | both | ACCEPTED |
| S6 | M1 entry criteria: U1/U5/A10 resolved before Skill C build | Codex | ACCEPTED |
| S7 | KB tweaks: dedicated-repo bias, error-pattern index, U9 at M0 | Claude | ACCEPTED |
| S8 | Wording/fact fixes: ask-mode conditional, edit-mode correction, Apache Spark naming, no-scripts=local policy, policy-name softened, M0 fact-lock table, gh skill note | both | ACCEPTED |

Applied to PLAN.md v4. User chose ROUND 3 (confirmation pass): both seats verify their round-2 majors are closed in v4; no cross-exam points remain open.

Round 1 carry-over record (was): 
- To Claude seat (from Codex): (1) Skill A as pure-LLM work still infeasible even with authoritative seed + owner sample gate? (2) staleness-scope statement sufficient for the "stamps are insufficient" concern? (3) user rejected the native-context trial — does the KB-first approach stand without that comparison?
- To Codex seat (from Claude): (1) smoke-tests-inside-Copilot sufficient for the "evals don't validate the harness" concern? (2) adoption/discovery only registered as [OPEN] U10 — acceptable? (3) routing mitigations (descriptions + instructions-file note + cross-trigger evals) sufficient for model-decided routing?
