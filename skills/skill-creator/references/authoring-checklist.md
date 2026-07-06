# Condensed authoring checklist

Working summary of docs/AUTHORING-GUIDE.md and the Agent Skills spec
(agentskills.io/specification, verified 2026-07-06). READ THE LIVE
docs/AUTHORING-GUIDE.md AS THE AUTHORITY — if this summary and the guide
ever disagree, the guide wins and this file needs a fix via
library-maintainer.

## Folder contract (guide §1)

```
skills/<skill-name>/
├── SKILL.md            # required
├── README.md           # required
├── references/         # SOURCES.md required; ONE level deep
├── assets/             # optional
├── scripts/            # optional, exceptional (guide §7)
└── evals/              # required: triggers.json + output-cases.md
```

Always start from `template/`.

## Frontmatter (spec + guide §2)

| Rule | Limit | Enforced by |
|---|---|---|
| name: lowercase-hyphen, = folder name | ≤64 chars; no leading/trailing/consecutive hyphens | spec; both validators |
| description | ≤500 chars (library) inside ≤1024 bytes (spec; Codex counts BYTES) | validate_skills.py |
| metadata.version / metadata.last-verified | quoted strings, e.g. "1.0.0" / "2026-07-06" | validate_skills.py |
| other fields (argument-hint, user-invocable, disable-model-invocation, context) | only with a row in docs/COMPATIBILITY.md | review |
| allowed-tools | FORBIDDEN in this library (guide §8) | review |

## Description formula (guide §3)

`<Does X for Y.> Use this skill when <trigger phrases users type>. Do not
use for <adjacent case>; use <sibling-skill> instead.`

- Keywords AND the full negative boundary inside the FIRST 250 chars.
- Third person. No marketing adjectives, no "helps with".
- Every sibling named → a near-miss case in evals/triggers.json.

## Voice split (guide §4)

- description: third person.
- body: imperative to the executing agent. Never "the agent should".

## Depth model (guide §5)

- Body <500 lines (library target 150–300); workflow + output template +
  checklist live in the body.
- Deep content → references/*.md, one level deep, each with an explicit
  load condition in the body.
- Multi-step deliverables end with a checklist.

## Sources (guide §6)

- Every normative claim → SOURCES.md row: standard, exact version,
  official URL, last-verified date, offline fallback.
- Verify on the web at authoring time; never model memory (risk R6).
- Distill content INTO the skill; the URL is for re-verification only.
- Consumer skills never instruct agents to fetch URLs at runtime.

## Scripts (guide §7) — exceptional

Python stdlib-only, non-interactive, no network, bounded output,
forward-slash paths, `--dry-run` for destructive ops, `--self-test` exits
0. Any script triggers manual script review before rollout.

## Shared constraints (guide §9) — verbatim in every body

> Assume no external internet access, no paid tools, and English output.
> Never send project code or data to external services.

## Evals (guide §10)

- triggers.json: ~20 cases; ≥12 should-trigger (varied), ≥6 near-miss
  no-trigger; every named sibling covered. Provisional bars: TPR ≥90%,
  FPR ≤10%.
- output-cases.md: ≥3 cases, scored with-skill vs without-skill; rubric
  mean ≥4.0; skill ≥ baseline on every case, strictly better on ≥2 of 3.

## Definition of done (guide §11)

1. `python tools/validate_skills.py <name>` → PASS, 0 errors
   (`--run-scripts` if scripts exist).
2. `agentskills validate skills/<name>` → valid
   (Windows: `.venv/Scripts/agentskills.exe`; POSIX: `.venv/bin/agentskills`).
3. SOURCES.md complete, versions verified this session.
4. Evals authored (and run when the harness allows).
5. Script review done if scripts present.
6. README install table matches docs/PER-HARNESS-SETUP.md.
7. CHANGELOG.md entry under [Unreleased].
8. STOP — human reviews the diff before rollout (security gate R8).
