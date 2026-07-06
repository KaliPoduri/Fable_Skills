---
name: adr-writer
description: Writes Architecture Decision Records in MADR 4.0.0 format. Use this skill when asked to write an ADR or to record or log a design decision. Do not use for whole-architecture docs or design proposals; use architecture-doc-writer or rfc-writer. Diagram-only requests go to c4-diagrammer. Covers the status lifecycle (proposed, accepted, deprecated, superseded), numbering and filename conventions, options with pros and cons, decision outcome, and consequences.
metadata:
  version: "1.0.0"
  last-verified: "2026-07-06"
---

# ADR Writer

Write one Architecture Decision Record per architecturally significant
decision, in MADR 4.0.0 format (adr.github.io/madr): a numbered Markdown
file capturing the problem, the options honestly compared, the chosen
option with justification, and its consequences — so future readers
understand WHY, not just what.

## Constraints

Assume no external internet access, no paid tools, and English output.
Never send project code or data to external services.
One decision per ADR; if the user bundles several decisions, split them
into separate records and say so.
ADRs are immutable history: never rewrite an accepted ADR's substance —
supersede it with a new one and update the old status line.
Never invent rationale. If the user cannot state why an option won, ask;
record honest drivers (including "team familiarity" or "deadline").

## Workflow

1. Confirm the decision is ADR-worthy: architecturally significant
   (affects structure, non-functional characteristics, dependencies,
   interfaces, or construction techniques). Trivial choices get a polite
   pushback and, if the user insists, a short ADR anyway.
2. Locate the decision log. Look for an existing directory (conventional:
   `docs/decisions/`, also common: `docs/adr/`, `adr/`). Match the
   existing numbering and template style; only introduce MADR conventions
   wholesale in a fresh log. If no log exists, create
   `docs/decisions/` and add `0000-use-madr-for-adrs.md` as the first
   record (offer this; do not force it).
3. Assign ID and filename: next consecutive four-digit number, then
   `NNNN-short-title-with-dashes.md` (lowercase, dashes, `.md`). The `#`
   title inside the file states problem + solution, e.g. "Use PostgreSQL
   for transactional storage".
4. Gather in one batch of questions (only what is missing): the problem
   and its scope; decision drivers (qualities, constraints, forces); the
   options actually considered (aim for 2-4; a single-option ADR must say
   why alternatives were not viable); who decided, who was consulted, who
   is informed; current status.
5. Fill the MADR template — load `references/madr-template.md` for the
   verbatim template and field semantics. Options get parallel treatment:
   the losing options' pros must survive in writing (that is the record's
   value). Use "Good, because / Neutral, because / Bad, because" bullets.
6. Set status per the lifecycle — load `references/adr-lifecycle.md` when
   status transitions, supersession, or log hygiene are involved:
   `proposed` until the deciders agree, `accepted` once they do; later
   `deprecated` (no replacement) or `superseded by ADR-NNNN` (with
   replacement). Rejected decisions stay in the log as `rejected`.
7. On supersession: write the new ADR, set the old record's status to
   `superseded by ADR-<new>`, and cross-link both ways in More
   Information. Touch nothing else in the old file.
8. Trim optional sections honestly: Decision Drivers, Consequences,
   Confirmation, Pros and Cons, More Information are optional in MADR —
   drop what adds nothing rather than padding. Context and Problem
   Statement, Considered Options, and Decision Outcome are the core.
9. Deliver the complete file content plus the exact target path, and (if
   an index/README of the log exists) the one-line entry to append.

## Output template

Deliver each ADR as a complete file in exactly this structure
(MADR 4.0.0; comments show what is optional):

```markdown
---
status: "{proposed | rejected | accepted | deprecated | superseded by ADR-0123}"
date: {YYYY-MM-DD}
decision-makers: {names/roles}
consulted: {names/roles}   # optional
informed: {names/roles}    # optional
---

# {Short title reflecting problem and solution}

## Context and Problem Statement

{2-3 sentences or a short story; may end in a question.}

## Decision Drivers   <!-- optional -->

* {driver 1}
* {driver 2}

## Considered Options

* {option 1}
* {option 2}
* {option 3}

## Decision Outcome

Chosen option: "{option 1}", because {justification tied to drivers}.

### Consequences   <!-- optional -->

* Good, because {positive consequence}
* Bad, because {negative consequence}

### Confirmation   <!-- optional -->

{How compliance is checked: review, test, fitness function.}

## Pros and Cons of the Options   <!-- optional -->

### {option 1}

* Good, because {argument}
* Neutral, because {argument}
* Bad, because {argument}

### {option 2}

...

## More Information   <!-- optional -->

{Links: superseded/superseding ADRs, related ADRs, evidence, revisit date.}
```

Precede the file content with one line: `Path: docs/decisions/NNNN-title.md`.

## Edge cases

- Existing non-MADR log (e.g. Nygard-style Status/Context/Decision/
  Consequences): match the existing format, numbering, and directory.
  Consistency inside a log beats template purity; offer a separate
  migration ADR if the team wants to move to MADR.
- Retroactive ADR (decision made long ago, never recorded): write it
  with status `accepted`, date = today, and note in More Information
  that it documents an existing decision after the fact.
- Decision reversed before acceptance: keep the record, set status
  `rejected`, and state in Decision Outcome what was rejected and why —
  rejected records prevent re-litigating the same debate.
- "Just one option" ADRs: require a sentence per discarded alternative
  explaining why it never reached the table (license, mandate,
  incompatibility). No comparison means no record of due diligence.
- Bundled decisions ("we chose Postgres, Kafka, and React"): three ADRs,
  consecutive numbers, cross-linked in More Information if genuinely
  coupled.
- Team disagreement: status stays `proposed`; record the open drivers
  and both camps' arguments in Pros and Cons — the ADR then becomes the
  agenda for the decision meeting, not its minutes.

## Pitfalls

- Advocacy writing: pros listed only for the winner. Losing options get
  their genuine pros; the record must show the choice was real.
- Consequences section with only "Good" bullets — every real decision
  costs something; ask what got harder.
- Editing an accepted ADR's rationale instead of superseding it.
- Renumbering or deleting superseded records — numbers are permanent.
- Status set to `accepted` while deciders have not confirmed — default
  to `proposed` unless the user states the decision is final.

## References (load on demand)

- `references/SOURCES.md` — source manifest (always present).
- `references/madr-template.md` — load in step 5: verbatim MADR 4.0.0
  template, field semantics, and filled example.
- `references/adr-lifecycle.md` — load in step 6 or when managing an
  existing log: status lifecycle, supersession mechanics, numbering,
  directory conventions, and what counts as architecturally significant.

## Checklist

- [ ] Exactly one decision in this ADR.
- [ ] Filename `NNNN-title-with-dashes.md` with the next free number in
      the project's decision log.
- [ ] Status is one of: proposed, rejected, accepted, deprecated,
      superseded by ADR-NNNN; date is the last-updated date.
- [ ] At least two options considered, or an explicit statement why only
      one was viable; losing options' pros recorded.
- [ ] Decision outcome justification references the decision drivers.
- [ ] On supersession, the old ADR's status line updated and both records
      cross-linked.
- [ ] Output follows the template above.
