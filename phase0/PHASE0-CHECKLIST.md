# Phase 0 — In-org go/no-go checklist

Run this on your ORG machine, in VS Code with Copilot Chat, inside a
disposable test repo (any small repo works; do not use real org code with
the canary — it never needs it). Record results in the template at the
bottom and bring them back to the build machine. This is a hard gate:
Phase B (skill authoring at scale) does not start until these results are in.

Everything you need is in this repo: the canary skill lives at
`skills/phase0-canary/` (SKILL.md + one reference file + one stdlib-only
Python script — safe to copy anywhere).

---

## Before you start (5 min)

- [ ] Open a disposable test repo in VS Code on the org machine.
- [ ] Confirm Copilot Chat works at all (ask it anything).
- [ ] Note versions: VS Code (`Help > About`), Copilot Chat extension
      (Extensions panel), `gh --version`, `python --version` (or
      `python3 --version`).

## Flow 1 — Manual copy triggers in Copilot Chat

1. Copy the whole folder `skills/phase0-canary/` from this library into the
   test repo at: `<test-repo>/.agents/skills/phase0-canary/`
   (create the `.agents/skills/` path if it does not exist).
2. Reload VS Code (`Developer: Reload Window`).
3. In Copilot Chat (agent mode if offered), type exactly:
   **run the fable canary check**
4. Expected: the agent picks up the skill and prints
   `FABLE-CANARY-TRIGGERED`, then `FABLE-REF-LOADED-7391` (reference file
   loaded), then the `FABLE-SCRIPT-OK` block (script ran), then
   `CANARY COMPLETE: 3/3 proofs passed`.
5. Also try an indirect prompt: **can you verify that skill installation
   works here?** — it should trigger too.
6. If nothing triggers: check whether the org has Copilot skills enabled at
   all (admin policy), and try `.github/skills/` as the copy target as a
   fallback — record which path (if any) worked.

Partial results matter: triggered-but-no-script (2/3) is a different outcome
than not-triggering at all — record the exact tokens you saw.

## Flow 2 — `gh skill install`

Needs gh ≥ 2.90.0 (`gh skill` is public preview). Caveat: the org machine's
`gh` must be authenticated to an account that can see the private repo
`KaliPoduri/Fable_Skills` on github.com. If org policy or an enterprise gh
host blocks that, record flow 2 as UNAVAILABLE (that decides manual-only
distribution — it is a valid outcome, not a failure of the gate).

1. `gh --version` — if < 2.90.0, try `gh extension list` / upgrade, or
   record as unavailable.
2. In the test repo root:
   `gh skill install KaliPoduri/Fable_Skills phase0-canary`
3. Expected: the skill lands in `<test-repo>/.agents/skills/phase0-canary/`.
4. Remove the manually-copied version first if flow 1 left one there
   (avoid a duplicate), reload VS Code, and repeat the trigger prompt from
   flow 1 step 3.

## Flow 3 — Python script + pptx/docx permissibility

Flow 1 already runs `scripts/canary.py` for you and its output includes
`python-pptx=...` / `python-docx=...` lines. Additionally:

1. If the canary reported both as `not-installed`, try:
   `pip install python-pptx python-docx`
   (or the org-approved install channel). Blocked/no-permission is a valid
   result — record it; Markdown/HTML stays the primary output format either
   way.
2. If the install succeeded, run the script once more:
   `python .agents/skills/phase0-canary/scripts/canary.py`
   and confirm both report `importable`.

## Cleanup

- [ ] Delete `.agents/skills/phase0-canary/` from the test repo.

---

## Results template (fill in and bring back)

```
PHASE 0 RESULTS — date: ____
Versions: VS Code ____ / Copilot Chat ext ____ / gh ____ / python ____

Flow 1 manual copy:   PASS / PARTIAL / FAIL
  Path that worked:   .agents/skills/ | .github/skills/ | none
  Tokens seen:        TRIGGERED? __  REF-LOADED? __  SCRIPT-OK? __
  Indirect prompt triggered? __
  Notes:

Flow 2 gh skill:      PASS / UNAVAILABLE / FAIL
  gh version: ____   Auth to private repo possible? __
  Notes:

Flow 3 python:        PASS / PARTIAL / FAIL
  Python version in-org: ____
  python-pptx: importable / installable / blocked
  python-docx: importable / installable / blocked
  Notes:
```
