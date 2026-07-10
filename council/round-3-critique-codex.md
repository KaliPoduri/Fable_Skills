# Council Round 3 — Confirmation Pass (Codex seat, verbatim)

**Part 1 — Closure Check**

1. CLOSED — Cost is now treated as usage-based, M0 fact-locks the org plan and budget cap, and M2 measures per-job build cost before scaling.

2. CLOSED — Adoption is now owned by M0 deliverables: owner, rollout channel, one-pager, invocation examples, demo incident, and support channel.

3. CLOSED — The wrong-KB poisoning controls are materially complete: seeded inventory, grep/path checks, repo:path:line evidence, sampling with negative checks, second-reviewer signoff for high-value jobs, reviewable diffs, and unverified marking.

4. CLOSED — Skill C first is now gated by M0 resolution of U1, U5, and A10 before M1.

5. CLOSED — The performance protocol is now specific enough: same input snapshot, cache/load notes, repeated runs, median/p95, threshold, rollback, cost/runtime, data-scale caveat, and job-owner approval.

6. CLOSED — Security/compliance moved beyond checklist-only: content-based redaction, checklist-first artifact handling, playbook PR governance, reviewer role, approval criteria, disputed-cause handling, and security owner.

7. CLOSED — Ask-mode fallback is conditional on M0 proving skills load in Ask; otherwise adoption states agent mode required.

8. CLOSED — Gates are quantified: M3 has >=10 incidents, >=2 not-in-code cases, >=2 insufficient-evidence traps, and acceptance is a recorded Copilot matrix across enabled models/modes.

9. CLOSED — Full-build effort is now measured in M2 through per-job cost extrapolation, with full build blocked unless affordable.

10. CLOSED — KB home risk is handled by preferring a dedicated small repo and making the final M0 decision explicit.

**Part 2 — Final Sweep**

No new major concerns.

Brief fact-hunt: billing wording checks out. GitHub docs say request-based billing was replaced as of June 1, 2026, and current usage is token-priced into AI credits; budget controls also exist, but M0 should ensure the cap is a hard stop, since some budget controls can allow charges past limits unless configured that way. (docs.github.com: what-changed-with-billing; models-and-pricing; budgets-for-usage-based-billing)

Edit/agent mode wording is mostly safe but slightly stale. Current VS Code docs frame this as Agent, Plan, and Ask; Agent can edit and run terminal/tool workflows, while Edit mode is deprecated. The plan's "agent mode required" conclusion remains correct. (code.visualstudio.com: local-agents; chat-tools)

`gh skill` is confirmed as public preview with GitHub CLI 2.90.0+. Error-pattern index and acceptance matrix changes are internally coherent and do not introduce a new blocker. (docs.github.com: add-skills)

Codex session ID: 019f4c26-ea85-7c40-8520-717a67450464
