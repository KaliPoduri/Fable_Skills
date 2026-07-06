---
name: phase0-canary
description: Verifies that Agent Skills load and run in this environment. Use this skill when the user says "run the fable canary check" or asks to verify that skill installation works. Do not use this skill for any real software engineering task; it only proves the skill mechanism itself.
metadata:
  version: "0.1.0"
  last-verified: "2026-07-06"
---

# Phase 0 Canary (THROWAWAY — delete after the Phase 0 gate)

Prove three mechanics in order. Print each proof token on its own line
exactly as written, then stop.

## 1. Trigger proof

Print this token first:

```
FABLE-CANARY-TRIGGERED
```

## 2. Reference-loading proof

Read the file `references/proof.md` in this skill's folder and print the
token found inside it. If the file cannot be read, print
`FABLE-REF-FAILED` instead.

## 3. Script proof

Run the script (try `python` first, then `python3`):

```
python scripts/canary.py
```

Print the script's full output verbatim. If the script cannot be run,
print `FABLE-SCRIPT-FAILED` and the exact error.

## 4. Summary

End with one line: `CANARY COMPLETE: <n>/3 proofs passed`.
