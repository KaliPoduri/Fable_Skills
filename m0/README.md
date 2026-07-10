# m0/ — Spark suite M0 kit (THROWAWAY)

The M0 feasibility spike + fact lock (PLAN.md §8). M0 is a **BLOCKING** gate:
M1/M2/M3 do not start until this is run in the org and judged GO. Delete the
whole `m0/` folder once the gate closes.

This kit is not part of the Fable Skills library — it lives under `m0/`, not
`skills/`, and the validators do not scan it.

## What to run (in order)

1. **`M0-CHECKLIST.md`** — the in-org spike. Run it on the org machine in a
   disposable test repo. Covers: agent/skills policy (A5), skill load from
   `.agents/skills/` incl. multi-root secondary root (A6), ask-mode load,
   file-write + git in agent mode, session-depth observation (U8/R4).
   Uses the canary skill `m0-canary/`.
2. **`FACT-LOCK.md`** — record verified facts: billing + HARD-stop budget,
   exact Spark minor version (U1), scheduler (U9), history-server access +
   retention (U5), config-change scope (A10), policies, KB home, names.
3. **`BASELINE.md`** — 3-5 recent incidents' time-to-root-cause.
4. **`ADOPTION-ONE-PAGER.md`** — owner, channel, "which skill?" guide, demo.
5. **`PLAYBOOK-GOVERNANCE.md`** — reviewer, approval criteria, disputed-cause
   handling, security owner.

## Gate

M1 entry requires U1, U5, A10 LOCKED in `FACT-LOCK.md`, plus the load/write
checks passing and adoption owner + governance complete. See the Gate
section of `M0-CHECKLIST.md`.

## Contents

```
m0/
├── README.md                 (this file)
├── M0-CHECKLIST.md           in-org spike procedure + results template
├── m0-canary/                throwaway pure-markdown canary skill
│   ├── SKILL.md
│   ├── references/proof.md
│   └── README.md
├── FACT-LOCK.md
├── BASELINE.md
├── ADOPTION-ONE-PAGER.md
└── PLAYBOOK-GOVERNANCE.md
```
