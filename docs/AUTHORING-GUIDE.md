# AUTHORING-GUIDE.md — standards for every Fable skill

Binding for all skills under `skills/`. CI (`tools/validate_skills.py` +
`agentskills validate`) enforces the mechanical parts; the rest is enforced
at review. PLAN.md §2.3 is the source of these rules.

## 1. Folder contract

```
skills/<skill-name>/
├── SKILL.md            # required — frontmatter + body
├── README.md           # required — usage + per-harness install
├── references/         # one level deep; SOURCES.md required
├── assets/             # optional — output templates
├── scripts/            # optional — Python, only where truly needed
└── evals/              # required — triggers.json + output-cases.md
```

Start every new skill from `template/` (copy, then fill). `skill-creator`
automates this.

## 2. Frontmatter recipe

- `name`: ≤64 chars, lowercase-hyphen, MUST equal the folder name (spec).
- `description`: see §3. Spec cap 1024 bytes (Codex counts bytes); library
  policy cap **500 chars** — CI reports which limit you broke.
- `metadata`: `version` and `last-verified` — always quoted strings, e.g.
  `version: "1.0.0"`, `last-verified: "2026-07-06"`.
- Optional per-surface fields (`argument-hint`, `user-invocable`,
  `disable-model-invocation`, `context`): only with a row in
  docs/COMPATIBILITY.md; unknown fields are ignored by spec, so they are
  safe but must not carry load-bearing behavior.

## 3. Description formula (the trigger surface)

Third-person, what-it-does first, then triggers, then the negative boundary.
**Keywords AND the negative boundary must land in the FIRST 250 chars** —
some harnesses truncate listings.

> `<Does X for Y.> Use this skill when <trigger phrases users actually
> type>. Do not use for <adjacent case>; that is owned by <sibling-skill>.`

Rules:
- Name the sibling skill for every boundary (overlap rules, PLAN.md §3).
- No marketing adjectives. No "helps with". Concrete nouns and verbs users
  type.
- Every sibling named here gets a near-miss case in `evals/triggers.json`.

## 4. Voice split

- **description**: third person ("Reviews SQL for index misuse…").
- **body**: imperative, addressed to the executing agent ("Check each
  query for…"). Never "the assistant/agent should".

## 5. Depth model

- SKILL.md body **<500 lines**: workflow, output template, checklist.
  Concise; the body is always in context once triggered.
- Deep content goes to `references/*.md`, ONE level deep, each listed in
  the body with an explicit load condition ("Load references/asvs.md when
  the review covers authentication").
- Output templates: exact headings/format in the body or `assets/`.
- Multi-step deliverables end with a checklist the agent must confirm.

## 6. Sources (risk R6: never model memory alone)

Every normative claim traces to `references/SOURCES.md`: standard, exact
version, official URL, last-verified date, offline fallback. Distill the
content INTO the skill (in-org there is no internet); the URL is for
re-verification, not runtime. Re-verification events go to
/VERIFICATION-LOG.md (owner: Kali; cadence [OPEN], quarterly proposed).

## 7. Script rules

Scripts are the exception, not the norm — only when text instructions
cannot do the job (parsing, generation, measurement).

- Python, **stdlib-only** preferred; any dependency needs explicit approval
  and a note in the skill README.
- Non-interactive; no network calls; bounded output; actionable errors.
- Forward slashes in all documented paths; document `python` vs `python3`.
- Destructive operations require `--dry-run`.
- Every script MUST exit 0 when invoked with `--self-test` (CI runs
  `validate_skills.py --run-scripts` on Windows).

## 8. Security gate (risk R8)

- NO `allowed-tools` / shell pre-approval in any skill.
- Every script-bearing skill is manually reviewed by the script reviewer
  (Kali, at launch) before rollout — GitHub itself warns skills can carry
  prompt injection or malicious scripts; ours must be boring and readable.
- Skills never instruct agents to fetch URLs at runtime.

## 9. Shared constraints (one line in every skill body)

Every skill body carries a Constraints section that includes at least:

> Assume no external internet access, no paid tools, and English output.
> Never send project code or data to external services.

Technology-agnostic by default; Scrum assumed for process skills (note
Kanban where it differs). `compliance-privacy-reviewer` additionally
carries the non-legal-advice + jurisdiction-assumptions note.

## 10. Evals & thresholds

Per skill: ~20 labeled trigger cases (`evals/triggers.json` — varied
should-trigger + near-miss should-NOT-trigger) and ≥3 output cases
(`evals/output-cases.md`, scored with-skill vs without-skill).

Runner: Claude Code headless on the build machine = automated PROXY (its
skill selector differs from Copilot's — R9); the AUTHORITATIVE check is a
manual smoke test in org VS Code Copilot Chat.

**PROVISIONAL thresholds** (set before the first-5 gate; finalized in
Phase A review with the user — PLAN.md §4):

| Metric | Provisional pass bar |
|---|---|
| Trigger TPR (should-trigger cases) | ≥ 90% |
| Near-miss FPR (should-NOT-trigger cases) | ≤ 10% |
| Output rubric (1–5: source accuracy, template compliance, completeness, actionability) | mean ≥ 4.0 |
| With-vs-without comparison | skill ≥ baseline on every case; strictly better on ≥ 2 of 3 |

## 11. Definition of done (per skill)

- [ ] `agentskills validate skills/<name>` → Valid skill
- [ ] `python tools/validate_skills.py --run-scripts <name>` → PASS
- [ ] SOURCES.md complete; every claim traceable; versions verified (not
      from model memory) — [OPEN]-listed standards verified at authoring
- [ ] Evals authored AND run against provisional thresholds
- [ ] Script review done (if scripts present)
- [ ] README per-harness table correct; links to docs/ resolve
- [ ] CHANGELOG.md entry
