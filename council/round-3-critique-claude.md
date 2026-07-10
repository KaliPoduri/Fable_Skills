# Council Round 3 — Confirmation Pass (Claude seat, verbatim)

## Part 1 — Closure check

**1. Copilot cost model — CLOSED.** §9 R1 now states the 2026-06-01 usage-based switch with the legacy model explicitly marked legacy; §8 M0 fact-locks the org's actual plan (usage-based vs legacy) and sets a budget cap; §4/§8 M2 records per-job build cost in `meta/generation.md`, extrapolates to the full estate, and green-lights only if affordable. Resumable/incremental builds back it up. The concern is resolved as promised.

**2. Adoption — CLOSED.** §8 M0 names the adoption owner (U10) and lists the four concrete deliverables: rollout channel, "which skill do I use?" one-pager with invocation examples, demo incident, support channel. Invocation examples are also wired into §2 routing hardening. Minor residual (not blocking): there is no post-rollout adoption *measurement*, only launch artifacts — but that goes beyond what round 2 asked for.

**3. Wrong-KB poisoning — CLOSED.** Every element of the promised fix is present in the plan text: authoritative job seed (§4, with an interactive human-confirmed fallback), build-time grep-confirmation of claimed table reads/writes and path-confirmation of entry scripts with failures marked unverified (§4), `repo:path:line` pointers on claims (§3 jobs/lineage tables), owner sampling ≥20% or ≥10 jobs including negative checks plus second-reviewer signoff for high-value jobs (§8 M2), regen as reviewable PR/diff (§4), and the M2 gate "no undetected wrong lineage in the sample." Note (minor): mechanical checks cover tables and entry scripts only — params, schedules, and upstream/downstream claims rely on pointers + sampling. Acceptable layering, worth remembering at M2.

**4. Skill-C-first blockers — CLOSED.** §8 M0 states "M1 entry criteria: U1, U5, A10 resolved," and each is individually tagged as an M1 entry criterion in §10/§11. §6 additionally makes exact minor version a required input before any config advice, so the dependency is enforced at answer time as well as at the gate.

**5. Performance measurement — CLOSED.** §6's output template embeds the full protocol (same input snapshot; cache state and cluster load noted; ≥3 runs; median + p95; agreed minimum-improvement threshold; rollback step; cost-vs-runtime; prod-like scale or recorded caveat) plus job-owner approval, and §8 M1's gate consumes it. The improvement threshold is "agreed" per-experiment rather than a fixed number in the plan — reasonable, since it is job-specific, but M1 should record the agreed number before the runs, not after.

**6. Security/compliance — CLOSED.** §7 makes redaction content-based with named content types and applies it to anything persisted regardless of length, explicitly demoting line caps to brevity rules; §5/§6 mandate checklist-first behavior on artifact receipt (before analysis); §5 playbook entries land via PR only with governance (reviewer role, approval criteria, disputed-cause handling, named security owner) completed at M0. A11 (whether pasted logs contain customer data) correctly stays open to calibrate strictness at M0.

**7. Ask-mode fallback — CLOSED.** §1 makes the fallback conditional on the M0 test of whether skills load in ask mode at all; if not, adoption material states "agent mode required." §8 M0 includes the test. The unenforceability trap is defused by not promising the fallback until it is proven possible.

**8. Unquantified gates — CLOSED.** §8 M3: ≥10 incidents including ≥2 not-in-code and ≥2 insufficient-evidence traps; gate = zero high-confidence wrong answers, evidence cited on every answer, traps answered correctly. §7 fixes acceptance as a recorded matrix of fixed test cases run inside Copilot across the org's enabled models/modes at every gate, with failures logged. M2 is likewise quantified (≥20%/≥10 jobs).

**9. Full-build effort — CLOSED.** Same mechanism as item 1: M2 measures per-job cost (prompts/tokens/time), extrapolates, and the full build is gated on affordability. Duplicative with item 1 but both are genuinely satisfied by the same text.

**10. KB home — CLOSED.** §3 records the preference (dedicated small repo) *and* the rationale (keeps stale KB text out of Copilot's implicit context in code repos; keeps stamping/diffing clean), with the final call recorded at M0 (§8).

**Verdict: 10/10 CLOSED.**

## Part 2 — Final sweep

**Scoped fact-hunt (claims changed since round 2):**

- **Billing wording — VERIFIED.** GitHub replaced request-based billing with usage-based (model + tokens, GitHub AI Credits) effective 2026-06-01; premium requests are now documented as "legacy," and some annual Pro/Pro+ plans remain on legacy until expiry. The plan's "verify the org's plan (usage-based vs legacy)" wording is exactly right, since legacy persistence is real.
- **`gh skill` CLI — VERIFIED.** Changelog dated 2026-04-16, public preview, requires GitHub CLI ≥ v2.90.0, five subcommands (install/preview/search/update/publish), cross-host per the open Agent Skills spec. The plan's §2 claim is accurate, including the "public preview / subject to change" caveat implicit in "distribution stays manual-copy for now."
- **Edit/agent mode capabilities — VERIFIED.** Agent mode autonomously edits files *and* runs terminal commands; edit mode applies multi-file edits without terminal execution. The plan's §1 characterization is correct, and Skill A's agent-mode requirement (terminal grep/path checks) follows.
- **Skills directories — CONSISTENT.** Current docs confirm `.agents/skills`-style locations (and `~/.copilot/skills` for personal skills) plus cross-compatibility with `.claude/skills`; the feature is still preview-era, which the plan already handles via R5 ("re-verify on breakage") and the M0 load test including multi-root workspaces (A6).
- **Error-pattern index / acceptance matrix — internally consistent.** `errors/index.md` (symptom → dated file) matches the §5 playbook schema and retrieval-by-symptom intent; the §7 acceptance matrix is consumed at every §8 gate, and M3's fixed test set instantiates it.

**New major concerns from v4: none.** Two minor notes, neither gate-blocking:

1. **Eval-run cost under usage-based billing.** The acceptance matrix (fixed cases × enabled models × modes, at every gate) is itself token spend. The M0 budget cap should explicitly cover evaluation runs, not only KB builds — one line in the fact-lock table suffices.
2. **`errors/index.md` has no overflow rule.** Lineage files have a split rule on budget overflow; the error index (~150 lines) will grow monotonically as playbook entries accumulate and has none. Trivial to add when it matters.

No new major concerns.

Sources: GitHub blog (usage-based billing move); GitHub docs (what changed with billing, legacy); GitHub changelog 2026-04-16 (gh skill); gh CLI manual; GitHub blog (ask/edit/agent modes); VS Code docs (agent skills); GitHub docs (about agent skills).
