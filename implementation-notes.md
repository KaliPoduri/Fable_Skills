# implementation-notes.md — Fable Skills

Log kept per PLAN.md implementing-agent instructions. Decisions as made; every
deviation under "Deviations" with a one-line reason.

---

# Spark suite (PROJECT 2)

## Decisions

- 2026-07-10 (session 2) [USER-DIRECTED] User cannot reach the org network
  and directed: "go with your expert decisions and defaults wherever
  necessary." Authoring of M1/M2/M3 skills proceeds WITHOUT the in-org M0
  run. m0/ kit stays intact for later execution; all in-org acceptance
  gates (M0 spike, M1 experiment, M2 owner sampling, M3 incident set)
  remain OPEN. Defaults policy: no org fact is guessed — skills are
  authored VERSION-ADAPTIVE and ask for facts at intake instead:
  - U1 Spark minor version: Skill C requires the exact version as intake
    input before any config advice (PLAN §6 already mandates this);
    config reference annotated per-version 3.0-3.5, AQE default-on ≥3.2.
  - U5 history server/retention: reference teaches standard fetch paths
    (History Server UI, `yarn logs -applicationId`, event-log dirs) with
    "confirm access/retention with your admin" caveats.
  - U9 scheduler: Skill A is scheduler-agnostic with a detect-and-confirm
    step (Airflow/Oozie/cron/Control-M/custom) against the job seed.
  - A10 config scope: advice defaults to job-scoped (`spark-submit
    --conf`/job config); cluster-scope flagged as admin-approval territory.
  - Ask-mode wording: conservative branch of PLAN §1 — "agent mode
    required" until M0 says otherwise.
  - U8 session depth: Skill A ships resumable small build steps (R4
    mitigation) regardless of observed depth.
  - KB home: dedicated repo (PLAN §3 preferred default); Skill A carries
    bootstrap instructions.
  - Budget (R1): Skill A instructs confirming a HARD-stop budget before
    builds; cannot be set from here.
  - NOT defaultable (org facts/people): baseline incidents, adoption
    owner, governance names — m0/ sheets stay blank for the user.

- 2026-07-10 M0 kit built under a throwaway `m0/` directory (NOT `skills/`) —
  keeps the 23 real library skills and both validators untouched; cleanup is
  `rm -r m0/` after the M0 gate. Kit = README, M0-CHECKLIST, m0-canary skill,
  FACT-LOCK, BASELINE, ADOPTION-ONE-PAGER, PLAYBOOK-GOVERNANCE (PLAN §8 M0).
- 2026-07-10 Canary named `m0-canary`, pure markdown (no script) — Spark-suite
  library policy is no-scripts, and M0 needs no Python. Proofs: trigger →
  reference-load → file-write → git; ask mode expected to block write/git.
- 2026-07-10 Continuing on `master` (standing repo decision, solo private repo);
  M0 kit is documentation/templates only.
- 2026-07-10 [OPEN] items (U1, U5, U9, A5-A11, KB home, names, owners) left as
  blanks in the templates for the USER to resolve during the in-org spike —
  not guessed. M1 entry gates (U1/U5/A10) flagged in FACT-LOCK.md.

## Verifications

- 2026-07-10 (session 2) Three skills authored by 3 parallel subagents;
  ALL Spark facts web-verified at authoring against official docs —
  Spark 3.5.8 (live site hosts only the newest patch per minor; older
  minors via archive.apache.org: 3.1.3/3.3.4/3.4.4 used to bound
  version-dependent claims — AQE default flip at 3.2.0, shuffleTracking
  default flip at 3.4). Non-Spark claims verified against official
  Hadoop/Oracle Java/GNU/POSIX sources. Subagents dropped (not shipped)
  every claim they could not verify; zero [Unverified] entries.
- 2026-07-10 (session 2) Full sweep after authoring + routing hardening:
  `python tools/validate_skills.py` → 26/26 PASS, 0 errors;
  `agentskills validate` → Valid on all 5 touched skills
  (etl-knowledge-builder, etl-assistant, spark-performance-advisor,
  sql-optimizer, systematic-debugger); both edited triggers.json parse.
- 2026-07-10 `agentskills validate m0/m0-canary` → "Valid skill" (exit 0) —
  the canary will actually load in the in-org test.
- 2026-07-10 `python tools/validate_skills.py` → 23/23 PASS, 0 errors; grep
  confirms `m0/` is NOT scanned — the throwaway kit stays out of CI.
- 2026-07-10 Retrieved the deleted `phase0-canary` from git `66fc68f` as the
  reference pattern (it was removed in `b630598` when Phase 0 was waived).

## Deviations

- 2026-07-10 (session 2) [USER-DIRECTED DEVIATION] PLAN §8 gate order
  (M0 blocking before M1-M3) not followed for AUTHORING: user offline
  from org network, directed expert defaults. All three skills authored
  in one session (M1+M2+M3 authoring scope); every in-org gate remains
  OPEN and un-attempted — authored ≠ accepted. m0/ kit untouched.
- 2026-07-10 (session 2) [DEVIATION] AUTHORING-GUIDE §11 definition of
  done item "evals authored AND run" — evals authored only; the headless
  proxy runner is still not stood up (same standing gap as the 23
  library skills). Acceptance for the Spark suite is the in-org matrix
  anyway (PLAN §7).
- 2026-07-10 (session 2) [DECISION] Routing hardening (PLAN §2/R9)
  applied bidirectionally: sql-optimizer + systematic-debugger
  descriptions gained one Spark-suite boundary line each + one
  cross-trigger near-miss eval case each (their primary boundaries stay
  within the first 250 chars; the Spark line lands after — secondary).
- 2026-07-10 (session 2) [DECISION] Regeneration preserves errors/ and
  glossary byte-for-byte (human-curated per §5 governance, not
  code-derived) — subagent's conservative reading of "reviewable diff,
  never silent overwrite"; adopted.
- 2026-07-10 (session 2) [DECISION] repo-instructions routing snippet
  (§2, [CANDIDATE mechanism]) ships as
  skills/etl-assistant/assets/repo-instructions-snippet.md — single
  durable home; mechanism itself still verified at M0.
- 2026-07-10 [DEVIATION] Handoff said "adapt skills/phase0-canary"; that skill
  no longer exists (deleted with the Phase-0 waiver, commit b630598). Rebuilt
  as a new pure-markdown `m0-canary` with file-write + git proofs. Reason: M0
  verifies skill loading + agent-mode file/git + ask-mode + session depth, not
  script execution or `gh skill install` (distribution is manual-copy-only,
  already locked). Old canary's gh-install/Python-script proofs are obsolete.

---

# Skills library (PROJECT 1)

## Decisions

- 2026-07-06 Work continues on `master` — matches repo convention (all planning
  commits are on master; solo-user private repo). No feature branch created.
- 2026-07-06 Phase 0 not yet run (user-only, in-org). Per user direction this
  session: build the Phase 0 test kit AND start Phase-0-independent Phase A
  work. Everything depending on Phase 0 results stays open and is marked
  "pending Phase 0" in the affected docs (gh skill vs manual-only install,
  python-pptx/docx, org Python version).
- 2026-07-06 Phase 0 kit split: checklist in `phase0/` (throwaway, deleted
  after the gate); the canary skill itself at `skills/phase0-canary/` because
  flow 2 (`gh skill install`) only auto-discovers `skills/*/SKILL.md` — it
  could not be tested from any other path. Canary is marked THROWAWAY in its
  own files and is deleted together with `phase0/` once the gate closes.
- 2026-07-06 CI validator placed at `tools/validate_skills.py`. PLAN.md tree is
  silent on the CI script's location; `tools/` is the conservative choice (does
  not pollute `skills/` or `docs/`).
- 2026-07-06 skills-ref installed into `.venv/` (gitignored) — build-machine
  only; consumers never need it.

## Verifications

- 2026-07-06 `skills-ref` EXISTS on PyPI: versions 0.1.0, 0.1.1
  (`pip index versions skills-ref`). PLAN §4 [CONFIRMED] upheld.
- 2026-07-06 `skills-ref` 0.1.1 PROVEN functionally: installed into `.venv`,
  ships an `agentskills` CLI (author: Anthropic / agentskills.io);
  `agentskills validate skills/phase0-canary` → "Valid skill". Division of
  labor: `agentskills` = spec validator; `tools/validate_skills.py` = library
  policy (500-char description, README/SOURCES/evals presence, body lines,
  script --self-test). CI = run both. Template folder correctly fails
  spec validation (placeholder name) — template/ is excluded from CI scans.
- 2026-07-06 `tools/validate_skills.py --run-scripts` PASS on phase0-canary,
  including Windows script invocation (canary.py --self-test, exit 0).
- 2026-07-06 Build machine: Python 3.13.7, pip 26.0.1 (command output this
  session).

- 2026-07-06 Tier 1 (21) + meta (2) authored by 10 parallel subagents; all
  sources web-verified at authoring time (results in VERIFICATION-LOG.md).
  Session-limit interruption mid-run: 4 agents resumed via their
  transcripts; resumes completed partial folders without re-verification.
- 2026-07-06 BUG FOUND by spec validator: 3 skills (cicd-pipeline-designer,
  postmortem-writer, release-manager) had unquoted `description:` values
  containing ": " — valid to our minimal parser, invalid YAML to real
  parsers. Fixed by quoting; validator hardened with a SPEC-YAML check so
  the library validator now catches this class itself.
- 2026-07-06 Notable verification findings: DORA is now a five-metric
  model (four keys historical); Mermaid C4 syntax is experimental (skills
  carry a flowchart fallback); istqb.org 403s bot fetches (noted in that
  skill's SOURCES.md).
- 2026-07-06 Consistency reviewer pass (read-only subagent) over all 23:
  library-wide PASS on constraints line, description formula, namespaces
  (REV-/SEC-/PERF-/SQL-/TM-), eval JSON, zero cross-skill trigger
  collisions. 6 findings, all fixed same session: 3 missing sibling
  call-outs (threat-modeler→api-designer, sql-optimizer→code-reviewer,
  adr-writer↔c4-diagrammer), literal <skill-name> placeholders in 3
  architecture READMEs, 3 descriptions with the boundary landing past char
  250 (trimmed), adr-writer sentence order. Post-fix: boundary ends ≤248
  on all edited skills; both validators green (23/23, 0 spec failures).

## Deviations

- 2026-07-06 [USER-DIRECTED] Phase 0 gate WAIVED — user declined to run the
  in-org go/no-go; kit (phase0/ + skills/phase0-canary) deleted. Risk
  accepted: in-org triggering/script execution remains unproven until the
  team first uses a skill (was risk R2's mitigation).
- 2026-07-06 [USER-DIRECTED] Distribution simplified to MANUAL COPY ONLY —
  all `gh skill install` documentation removed (README, PER-HARNESS-SETUP,
  COMPATIBILITY). Version pinning falls back to git tags + CHANGELOG only.
- 2026-07-06 [USER-DIRECTED] "Create the skills" ⇒ authoring full Tier 1
  (21) + meta (2) in one pass; the first-5 gate becomes a post-hoc user
  review of the authored set rather than a pre-production checkpoint.
- 2026-07-06 Consequence of no Phase 0: org Python version and pptx/docx
  permissibility unknown ⇒ Tier 1 skills ship with NO scripts at all
  (Markdown/HTML output only, which PLAN §2.3 already made primary).

## Open items raised with user

- 2026-07-06 Phase 0 status asked at session start; user chose "build kit +
  start Phase A prep". Phase 0 remains a hard gate before Phase B.
