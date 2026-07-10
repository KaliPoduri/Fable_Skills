# M0 — Feasibility spike + fact lock (BLOCKING gate)

Run this on your ORG machine, in VS Code with GitHub Copilot, inside a
**disposable test repo** (any small repo — do NOT use real org code with
the canary; it never needs it). Record every result in the template at the
bottom, plus fill the four companion sheets in this folder. This is a hard
gate: nothing downstream (M1/M2/M3) starts until the results are in and the
gate is judged.

**M1 entry criteria (must be resolved here):** U1 (exact Spark minor
version), U5 (history-server access + event-log retention), A10 (dev
config-change scope). See `FACT-LOCK.md`.

Everything you need is in this folder: the canary skill is `m0/m0-canary/`
(SKILL.md + one reference file — pure markdown, no scripts).

---

## Before you start (5 min)

- [ ] Open a disposable test repo in VS Code on the org machine (make it a
      git repo: `git init` if needed — flows 3 and 4 use git).
- [ ] Confirm Copilot works at all (ask it anything).
- [ ] Note versions: VS Code (`Help > About`), GitHub Copilot / Copilot
      Chat extension (Extensions panel), `git --version`.
- [ ] **Admin policy (A5):** ask your Copilot admin whether the
      agent-feature / skills capability is enabled for the org, and record
      the exact policy name + scope. If it is off, flows 1-4 will not
      trigger and this is the first thing to fix.

## Flow 1 — Agent-mode load from `.agents/skills/` (primary)

1. Copy the whole folder `m0/m0-canary/` into the test repo at
   `<test-repo>/.agents/skills/m0-canary/` (create `.agents/skills/` if it
   does not exist).
2. Reload VS Code (`Developer: Reload Window`).
3. Put Copilot in **Agent mode**. Type exactly: **run the m0 canary check**
4. Expected in agent mode: `M0-CANARY-TRIGGERED`, then `FABLE-M0-REF-4820`,
   then `M0-WRITE-OK` (and a real `m0-canary-proof.txt` appears on disk),
   then the `git status` output, then `M0 CANARY COMPLETE: 4/4 proofs
   passed`.
5. Also try an indirect prompt: **can you verify skill installation and
   file writes work here?** — it should trigger too.
6. If nothing triggers: re-check the admin policy (Before-you-start), then
   try `.github/skills/` and `.claude/skills/` as fallback copy targets —
   record which path (if any) worked.

Partial results matter. Record the EXACT tokens seen — triggered-but-no-git
(3/4) is a different outcome than not-triggering at all.

## Flow 2 — Ask-mode load test

1. Switch Copilot to **Ask mode** (leave the canary where flow 1 left it).
2. Repeat the trigger: **run the m0 canary check**
3. Record: does the skill trigger AT ALL in ask mode? How many proofs pass?
   (File-write and git are expected to be blocked → `M0-WRITE-BLOCKED` /
   `M0-GIT-BLOCKED`.)
4. This decides adoption wording (PLAN §1): if skills do NOT load in ask
   mode, adoption material simply says "agent mode required"; if they load
   but cannot act, the "declare unchecked steps" fallback applies.

## Flow 3 — Multi-root secondary root (A6)

1. Open a **multi-root workspace**: folder A = the test repo, plus add a
   second folder B (`File > Add Folder to Workspace`).
2. Put the canary ONLY in folder B's `.agents/skills/m0-canary/` (remove it
   from folder A first to avoid a duplicate).
3. Reload, Agent mode, trigger again.
4. Record whether the skill is discovered from the **secondary** root.

## Flow 4 — File-write + git confirmation (agent mode)

Flow 1 already exercises this via proofs 3-4. Confirm the physical effects:

- [ ] `m0-canary-proof.txt` actually exists on disk with content
      `M0-WRITE-OK`.
- [ ] `git status --short` in the terminal shows it staged.
- [ ] Note any permission prompt / approval the agent needed before writing
      or running git (this shapes how Skill A's builds feel in practice).

## Flow 5 — Session-depth observation (U8 / R4)

1. In agent mode, give a longer multi-step task, e.g. **read every file in
   this test repo and summarize each in one line**.
2. Observe how many tool calls / file reads the agent chains in a single
   turn before it stops, asks to continue, or hits a limit.
3. Record the approximate agentic depth (rough count of steps per turn).
   This is the input for whether Skill A needs resumable builds and how
   small each build step must be.

## Then, off-machine data (fill the companion sheets)

- [ ] `FACT-LOCK.md` — billing plan + HARD-stop budget, exact Spark minor
      version (U1), scheduler type (U9), org policies, history-server
      access + event-log retention (U5), dev config-change scope (A10),
      plus platform/repo-visibility/scheduler-completeness/log-sensitivity.
- [ ] `BASELINE.md` — 3-5 recent incidents' time-to-root-cause.
- [ ] `ADOPTION-ONE-PAGER.md` — name the adoption owner; fill rollout
      channel, "which skill?" guide, one demo incident, support channel.
- [ ] `PLAYBOOK-GOVERNANCE.md` — reviewer role, approval criteria,
      disputed-cause handling, named security owner.
- [ ] KB home decision (dedicated repo preferred — PLAN §3).
- [ ] Confirm or rename the three skills (names fixed at M0 exit — PLAN §2).

## Cleanup

- [ ] Delete `.agents/skills/m0-canary/` (and folder B's copy) and the
      `m0-canary-proof.txt` from the test repo.

---

## Gate

- [ ] Skills load in at least one supported mode/path (record which).
- [ ] Agent mode can write files and run git.
- [ ] Fact-lock table complete; **U1, U5, A10 resolved** (M1 entry).
- [ ] Budget cap set as a HARD stop covering builds AND eval runs.
- [ ] Adoption owner named; playbook governance complete.
- [ ] KB home + skill names decided.

If any load check fails, revisit PLAN §2 (packaging) before proceeding.

---

## Results template (fill in and bring back)

```
M0 RESULTS — date: ____
Versions: VS Code ____ / Copilot ext ____ / git ____
Admin policy (A5): agent/skills enabled? __  policy name/scope: ____

Flow 1 agent-mode load:  PASS / PARTIAL / FAIL
  Path that worked:      .agents/skills/ | .github/skills/ | .claude/skills/ | none
  Tokens seen:           TRIGGERED? __  REF? __  WRITE? __  GIT? __
  Indirect prompt triggered? __
  Approval prompt needed to write/git? __
  Notes:

Flow 2 ask-mode load:    LOADS / DOES-NOT-LOAD
  Proofs passed in ask mode: __ /4
  Adoption wording implied: "agent mode required" | "declare unchecked steps"
  Notes:

Flow 3 multi-root (A6):  DISCOVERED / NOT-DISCOVERED from secondary root
  Notes:

Flow 5 session depth:    ~____ tool calls/reads per turn before stop
  Hit a limit / asked to continue? __
  Notes:

Gate judgement:          GO / NO-GO / REVISIT-PACKAGING
  Reason:
```
