# Round 2 Critique — Codex seat (verbatim)

**Part 1 Verdicts**

1. **AGREE WITH CHANGE** — Inside-Copilot smoke tests are necessary, but not sufficient if they remain only "smoke." Milestone gates need fixed acceptance cases, model-by-model results, ask/agent permission coverage, and recorded failures. Library evals are still useful as authoring checks, not acceptance proof.

2. **AGREE** — Not acceptable. U10 must be planned now. Adoption is part of feasibility because Spark-newbie developers will not reliably discover or invoke skills by accident. Add an M0 owner, rollout channel, quickstart, and training loop.

3. **AGREE WITH CHANGE** — The revision is directionally right. GitHub docs confirm Copilot decides skill use from prompt + skill description, so disambiguation and cross-trigger tests matter. Still add explicit user-facing invocation examples and fail-closed routing tests; "handoff" should stay only as "tell the user which skill to invoke."

**Part 2 Fresh Review**

1. **Major: the Copilot cost model is stale.** Current GitHub docs say request-based billing became legacy after **June 1, 2026** and usage is now token/AI-credit based for current plans. The plan's R1 "one prompt = one premium request" model can understate cost for long KB/log/code interactions. Rework R1 around AI credits, model choice, token-heavy logs, and budget caps. Sources: GitHub models/pricing docs; legacy billing change docs.

2. **Major: adoption is a blocking missing workstream.** U10 cannot stay ownerless. The product is for newbies, and routing depends on users knowing which skill to invoke. Add M0 deliverables: owner, install/copy path, "which skill do I use?" one-pager, demo incident, office-hours or async support channel, and usage feedback.

3. **Major: LLM-generated KB poisoning remains the central risk.** The plan admits Skill A is LLM-driven and scriptless, but the mitigation is only seed + sample verification. For 3-10 repos and up to ~2000 files, one wrong lineage can poison many RCA answers. M2 needs a defined sample size, negative checks, second-reviewer signoff for high-value jobs, and regeneration diff review.

4. **Major: Skill C first may be blocked by unknowns.** M1 depends on Spark minor version, YARN/history-server access, job-scoped config permissions, non-prod reproducibility, and baseline stability. Those are U1/U5/A9/A10, but M1 is scheduled before resolving them. Make U1/U5/A10 explicit M1 entry criteria.

5. **Major: performance measurement is under-specified.** "Repeated runs" is not enough. Require same input snapshot, cache state noted, cluster load noted, median/p95 or agreed metric, minimum N runs, rollback, and cost-vs-runtime tradeoff. Otherwise speedups may be noise.

6. **Major: security/compliance is too checklist-based.** "Org policy allows code/logs" is user-provided, but persistence to KB/playbooks needs stricter controls: no secrets, no customer identifiers, no raw row values, retention rules, PR reviewer ownership, and secret scanning. GitHub's own skill docs warn skills may contain prompt injections or malicious scripts, so distribution governance matters even for internal manual-copy skills.

7. **Major fact-hunt result: most Copilot skill claims are broadly verified, but one policy claim is not.** Verified: project skills can live in `.github/skills`, `.claude/skills`, or `.agents/skills`; Copilot chooses relevant skills by prompt and description; `gh skill` is public preview and needs GitHub CLI 2.90.0+; VS Code agents can read/edit files and run terminal commands with permissions. I did not verify a specifically named "Agent Skills enabled" org policy separate from broader agent/CLI policy controls.

8. **Minor: Spark naming is ambiguous.** The plan mentions GitHub Spark docs in the same ecosystem where Apache Spark is the actual domain. Use "Apache Spark" everywhere except when referring to GitHub's product.

9. **Minor: "no scripts inside skills" is a local library convention, not a Copilot limitation.** GitHub supports scripts/resources in skills. Keep the convention if settled, but mark it as local policy so future reviewers do not infer a platform constraint.

10. **Minor: the 10-line excerpt cap is not a privacy control.** A single line can contain secrets, row values, or identifiers. Redaction must be content-based, not line-count-based.

11. **Minor: playbook PR governance is incomplete.** "Via PR" is good, but needs owner, reviewer role, branch/repo location, approval criteria, and what happens when the root cause is disputed.

12. **Concrete refinements:** update R1 to AI-credit/token billing; promote U10 into M0; add a Copilot-in-VS-Code acceptance matrix by model and mode; add explicit `/` or natural-language invocation examples for all three skills; define M1 performance experiment protocol; define M2 sample math and reviewer signoff; add a security owner for log persistence; and add a "fact lock" table at M0 for Copilot docs, Spark version, scheduler, policies, and billing.

Codex session ID: 019f4c1a-63ea-7c33-be16-4cb3ad9fbda8
