---
name: m0-canary
description: Verifies that Agent Skills load and that agent mode can write files and run git in this environment. Use this skill when the user says "run the m0 canary check" or asks to verify that skill installation and agent-mode file writes work here. Do not use for any real ETL, Spark, or software task; it only proves the skill mechanism itself.
metadata:
  version: "0.1.0"
  last-verified: "2026-07-10"
---

# M0 Canary (THROWAWAY — delete with the m0/ kit after the M0 gate)

Prove four mechanics in order. Print each proof token on its own line
exactly as written, then move to the next. Do NOT skip a proof if an
earlier one fails — record each independently so partial results are
visible (ask mode is expected to pass 1-2 and block 3-4).

## 1. Trigger proof

Print this token first:

```
M0-CANARY-TRIGGERED
```

## 2. Reference-loading proof

Read the file `references/proof.md` in this skill's folder and print the
token found inside it. If the file cannot be read, print
`M0-REF-FAILED` instead.

## 3. File-write proof (agent mode)

Create a file named `m0-canary-proof.txt` in the current workspace root
whose only content is the line `M0-WRITE-OK`. Then print `M0-WRITE-OK`.
If you cannot create files in this mode (for example, ask mode), print
`M0-WRITE-BLOCKED` and one line naming why.

## 4. Git proof (agent mode)

Run, in the terminal:

```
git status --short
git add m0-canary-proof.txt
git status --short
```

Print the combined output verbatim. If you cannot run terminal/git
commands in this mode, print `M0-GIT-BLOCKED` and one line naming why.

## 5. Summary

End with one line: `M0 CANARY COMPLETE: <n>/4 proofs passed`, where each
of TRIGGERED / REF / WRITE / GIT that succeeded counts as one.
