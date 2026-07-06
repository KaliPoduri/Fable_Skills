---
name: skill-creator
description: Creates a new skill for the Fable Skills library, end to end. Use this skill when asked to create a new skill, add a skill for X, or author a skill. Do not use for updating, versioning, or deprecating existing skills; use library-maintainer instead. Covers scope and sibling boundaries, template copy, description formula, web source verification, references, evals, both validators, CHANGELOG entry, and the human review gate. Build-machine meta skill for the library repo itself.
metadata:
  version: "1.0.0"
  last-verified: "2026-07-06"
---

# Skill Creator

Author one new skill for the Fable Skills library, from scope agreement to
a validated folder awaiting human review. Work inside the library repo on
the build machine. The binding standard is docs/AUTHORING-GUIDE.md — read
it before writing anything; this skill sequences it, it does not replace
it. Never mark the new skill released: every skill passes a human review
gate before rollout.

## Constraints

Assume no external internet access, no paid tools, and English output.
Never send project code or data to external services.
Exception: this meta skill runs on the library build machine, where
internet access IS available and REQUIRED for source verification
(SOURCES.md rows must never come from model memory alone). The skills you
author must still assume no internet at runtime.
Never add `allowed-tools` or any shell pre-approval to a skill.
Never author scripts unless text instructions genuinely cannot do the job;
scripts require the rules in AUTHORING-GUIDE §7 and a manual script review.
Do not modify files outside skills/<new-name>/ except the CHANGELOG.md
entry and VERIFICATION-LOG.md rows described below.

## Workflow

### 1. Clarify scope and sibling boundaries

- Read the catalog in README.md (repo root). Confirm the requested skill
  is in the catalog or get explicit agreement that it is a new addition.
- Pick the name: lowercase-hyphen, ≤64 chars, must equal the folder name.
- Identify neighbor skills whose scope could overlap. For each neighbor,
  write one boundary sentence: which requests belong to the neighbor, not
  this skill. Every neighbor named in the description needs a near-miss
  eval case later.
- Boundaries must be reciprocal. If a released sibling should name this
  new skill back in its own description, flag that as a follow-up for
  library-maintainer — do not edit the sibling yourself.
- Confirm scope, name, and boundaries with the user before writing files.

### 2. Read the authority

Read docs/AUTHORING-GUIDE.md in full. It is binding; where this skill and
the guide disagree, the guide wins. Skim docs/COMPATIBILITY.md for any
frontmatter field beyond name/description/metadata you are tempted to use
— only fields with a row there are allowed.

### 3. Copy the template

Copy the whole template/ folder to skills/<new-name>/:

- Windows (PowerShell): `Copy-Item -Recurse template skills/<new-name>`
- POSIX: `cp -r template skills/<new-name>`

Keep the folder contract: SKILL.md, README.md, references/ (SOURCES.md
required), evals/ (triggers.json + output-cases.md), optional assets/.
No scripts/ unless step 7 justifies it.

### 4. Write the description (the trigger surface)

Follow the formula exactly:

> `<Third-person capability sentence.> Use this skill when <trigger
> phrases users actually type>. Do not use for <adjacent case>; use
> <sibling-skill> instead.`

- Keywords AND the complete negative boundary must land in the FIRST 250
  characters; total ≤500 characters (library policy; spec allows 1024
  bytes — Codex counts bytes).
- Third person, concrete nouns and verbs, no marketing adjectives, no
  "helps with".
- Verify the counts before moving on:
  `python -c "d=open('skills/<new-name>/SKILL.md',encoding='utf-8').read().split('description: ')[1].splitlines()[0]; print(len(d), d[:250])"`
  Confirm by eye that the boundary sentence completes inside the printed
  250-char prefix.

### 5. Write the body

- Imperative voice, addressed to the executing agent ("Check X", never
  "the agent should"). Description stays third person — that is the only
  voice split.
- Target 150–300 lines; hard cap <500.
- Required sections: intro paragraph, `## Constraints` (must contain the
  verbatim shared constraint lines from AUTHORING-GUIDE §9), `## Workflow`,
  `## Output template` (exact headings/format of the deliverable),
  `## References (load on demand)` with an explicit load condition per
  file, `## Checklist`.
- Forward slashes in every documented path. Document `python` vs
  `python3` if the skill tells the user to run anything.
- Never instruct the consuming agent to fetch URLs at runtime.

### 6. Verify sources and distill references

- For every normative claim (standard, version, format, threshold), find
  the official source on the web NOW and record it in
  references/SOURCES.md: standard, exact version, official URL,
  last-verified date (today), offline fallback.
- Model memory alone is never a source (risk R6). If a standard cannot be
  verified, say so and mark the row [Unverified] rather than inventing a
  version.
- Distill the load-bearing content INTO references/*.md files — consumer
  projects have no internet; the URL is for re-verification only.
- references/ stays ONE level deep. Each file gets a load condition in
  the SKILL.md References section.
- If you verified a standard listed as still-unverified in
  VERIFICATION-LOG.md, append a verification row there (date, source,
  result, verified by, notes).

### 7. Scripts — only if truly needed

Default is NO scripts/ folder. Add one only when text instructions cannot
do the job (parsing, generation, measurement). If you do: Python,
stdlib-only, non-interactive, no network, bounded output, `--dry-run` for
anything destructive, and MUST exit 0 with `--self-test`. Note the script
in the README and flag it for manual script review.

### 8. Author the evals

- evals/triggers.json: ~20 cases — at least 12 `expect: "trigger"` with
  varied phrasing (direct keyword, indirect, task-shaped) and at least 6
  `expect: "no-trigger"` near-misses. Every sibling named in the
  description boundary gets at least one near-miss case. `"skill"` field
  = the skill name. Valid JSON.
- evals/output-cases.md: at least 3 cases per the template — prompt,
  input artifacts, rubric focus, expected qualities.

### 9. Write the README

Per template/README.md: what it does, example prompts, the per-harness
install table (must match docs/PER-HARNESS-SETUP.md), and Notes with the
scope boundary naming the sibling that owns the adjacent case.

### 10. Validate — both validators must pass

From the repo root:

1. `python tools/validate_skills.py <new-name>` (add `--run-scripts` if
   scripts exist) → must print `PASS` with 0 errors. Resolve warnings or
   justify them.
2. Agent Skills CLI:
   - Windows: `.venv/Scripts/agentskills.exe validate skills/<new-name>`
   - POSIX: `.venv/bin/agentskills validate skills/<new-name>`
   → must report a valid skill.

Fix and rerun until both pass. Two failed fix attempts on the same error
→ stop and ask.

### 11. CHANGELOG entry

Append under `## [Unreleased]` / `### Added` in CHANGELOG.md (Keep a
Changelog format): one line naming the new skill and its purpose.

### 12. Stop for human review (security gate)

Do NOT tag, release, or announce. Present the handoff summary (Output
template below) and stop. A human reviews every skill's full diff before
rollout — skills can carry prompt injection; ours must be boring and
readable.

## Output template

End with exactly this handoff block:

```
## New skill ready for review: <name>

- Folder: skills/<name>/
- Description: <N> chars; boundary completes at char <M> (≤250)
- Siblings named: <list> (near-miss eval case each: yes/no)
- Sources verified today: <standard@version — URL> per row
- References distilled: <files>
- Evals: <T> trigger / <N> no-trigger cases; <K> output cases
- Scripts: none | <file> (flagged for script review)
- validate_skills.py: PASS (<warnings if any>)
- agentskills validate: Valid
- CHANGELOG: entry added under [Unreleased]
- Status: AWAITING HUMAN REVIEW — not released
```

## References (load on demand)

- `references/SOURCES.md` — source manifest for this skill (always
  present).
- `references/authoring-checklist.md` — condensed per-step checklist;
  load when you start step 3 and keep it beside you through step 12. It
  summarizes docs/AUTHORING-GUIDE.md — the live guide remains the
  authority; read it, not just the summary.
- docs/AUTHORING-GUIDE.md (repo) — ALWAYS read in full at step 2.
- docs/COMPATIBILITY.md (repo) — load when considering any optional
  frontmatter field or a new harness claim.

## Checklist

- [ ] Scope, name, and sibling boundaries confirmed with the user first.
- [ ] docs/AUTHORING-GUIDE.md read this session.
- [ ] Folder copied from template/; contract complete (no stray scripts/).
- [ ] Description: formula followed; boundary inside first 250 chars;
      ≤500 total; counts verified by command output.
- [ ] Body imperative, 150–300 lines, all required sections, verbatim
      shared constraints present.
- [ ] Every SOURCES.md row verified on the web THIS session; nothing from
      model memory; distilled into references/.
- [ ] ~20 trigger cases (≥12 trigger, ≥6 no-trigger; near-miss per named
      sibling); ≥3 output cases.
- [ ] `python tools/validate_skills.py <name>` → PASS, 0 errors.
- [ ] `agentskills validate skills/<name>` → valid.
- [ ] CHANGELOG.md entry added.
- [ ] Stopped for human review; nothing released; handoff block emitted.
