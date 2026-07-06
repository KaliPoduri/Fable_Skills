---
name: epic-story-breakdown
description: Breaks a PRD or feature into epics and a story backlog using SPIDR and other splitting patterns. Use this skill when asked to break a PRD into stories, split an epic, or create a backlog. Do not use to write one story; use user-story-writer instead. Produces one-liner story candidates with dependencies and sizing hints; hand each to user-story-writer for INVEST and Gherkin criteria. For authoring the upstream requirements doc, use prd-writer instead.
metadata:
  version: "1.0.0"
  last-verified: "2026-07-06"
---

# Epic & Story Breakdown

Decompose a PRD, feature description, or oversized epic into an ordered set
of epics and a backlog of story candidates. Each story candidate is a
one-liner — this skill deliberately stops before full story writing. Story
quality (INVEST, role–goal–benefit narrative, Gherkin acceptance criteria)
is owned by the sibling skill `user-story-writer`; the upstream requirements
document is owned by `prd-writer`. The output of this skill is the input to
`user-story-writer`.

## Constraints

Assume no external internet access, no paid tools, and English output.
Never send project code or data to external services.
Scrum is assumed (Sprint-sized stories); where Kanban differs, note it
inline rather than restructuring the output.
Stay technology-agnostic: split by user-visible behavior, never by
architecture layer, component, or team unless the input forces it.
Do not invent requirements. Every epic and story candidate must trace to a
statement in the input document; gaps go under Open questions.

## Workflow

1. Ingest the input. Accept a PRD, feature description, epic text, or a
   pasted requirements excerpt. If no input document exists yet, say so and
   point the user to `prd-writer` — do not fabricate requirements from a
   title alone.
2. Extract outcomes. List the distinct user or business outcomes the input
   promises. Ignore implementation detail at this stage.
3. Form epics. Group outcomes into 3–9 epics. Name each epic as an outcome
   ("Customer can pay by invoice"), not a component ("Billing service").
   Give each epic a one-sentence outcome statement and, if the input states
   it, a priority.
4. Split each epic into story candidates. Load
   `references/splitting-patterns.md` and try patterns in this order until
   the pieces feel Sprint-sized:
   - Workflow steps — thin end-to-end slice first, then enrich steps.
   - SPIDR: Spike, Path, Interface, Data, Rules.
   - Operations (CRUD) — separate create, read, update, delete.
   - Business-rule variations — one story per rule cluster.
   Prefer splits where every piece still delivers user-visible value; a
   spike is the fallback when uncertainty, not size, is the problem.
5. Write each story candidate as a one-liner: an active-voice capability
   statement from the user's point of view (a title, not a full story).
   Tag it with the splitting pattern used.
6. Check size. Per the Scrum Guide 2020, a Product Backlog item is ready
   for selection when the team can get it Done within one Sprint. Flag any
   candidate that plausibly exceeds a Sprint and split it again. (Kanban:
   substitute the team's target cycle time or WIP-friendly item size for
   "one Sprint".)
7. Map dependencies. Note only real sequencing constraints (data must
   exist before it can be edited; authentication before per-user features).
   Keep the list short — most stories should be independent.
8. Add sizing hints. Mark each candidate S / M / L relative to the others.
   These are refinement hints, not estimates; per the Scrum Guide, the
   Developers who will do the work are responsible for sizing.
9. Record open questions. Anything the input leaves ambiguous becomes an
   explicit question, never a silent assumption.
10. Hand off. Close with the handoff note pointing each candidate to
    `user-story-writer` for narrative, INVEST check, and Gherkin
    acceptance criteria.
11. Run the Checklist below before presenting the result.

## Output template

Produce exactly this structure:

```markdown
# Story breakdown: <feature or PRD title>

## Input summary
<2–4 sentences: what the input document promises, for whom.>

## Epics
| # | Epic (outcome phrasing) | Outcome statement | Priority |
|---|---|---|---|

## Story candidates
### Epic 1: <name>
| ID | Story candidate (one-liner) | Split pattern | Size hint |
|---|---|---|---|
<Repeat the subsection per epic. IDs like E1-S1, E1-S2, E2-S1.>

## Dependencies
- <E2-S1 depends on E1-S3 — reason.> (or "None identified.")

## Open questions
- <Ambiguity in the input that blocks or reshapes a split.>

## Handoff
Run each story candidate through `user-story-writer` to add the
role–goal–benefit narrative, INVEST check, and Gherkin acceptance
criteria before Sprint Planning.
```

### Filled micro-example (style anchor)

For a one-paragraph feature "Customers can leave product reviews":

```markdown
## Epics
| # | Epic (outcome phrasing) | Outcome statement | Priority |
|---|---|---|---|
| 1 | Customer can publish a review | Shoppers share a rating and text on a purchased product | High |
| 2 | Shopper can use reviews to decide | Ratings and reviews are visible and sortable on product pages | High |
| 3 | Staff can moderate reviews | Abusive or off-policy reviews are caught before or shortly after publishing | Medium |

## Story candidates
### Epic 1: Customer can publish a review
| ID | Story candidate (one-liner) | Split pattern | Size hint |
|---|---|---|---|
| E1-S1 | Customer submits a star rating on a purchased product | Workflow steps (thin slice) | S |
| E1-S2 | Customer adds review text to a rating | Workflow steps (enrich) | S |
| E1-S3 | Customer edits their own review | CRUD (update) | M |
| E1-S4 | Only verified purchasers can review | SPIDR-Rules | M |

## Dependencies
- E1-S2 depends on E1-S1 — text attaches to an existing rating.
- E3-* depends on E1-S1 — nothing to moderate until reviews exist.
```

Note the style: outcome-phrased epics, one-liners with no narrative or
criteria, pattern named per row, sizes relative.

Scale the output to the input: a one-paragraph feature may need only 2–3
epics, a full PRD closer to the upper bound. If the input is a single
already-small epic, skip the Epics table (one section of story candidates
suffices) but keep every other section, including the Handoff.

## References (load on demand)

- `references/SOURCES.md` — source manifest (always present).
- `references/splitting-patterns.md` — load in step 4, whenever choosing
  how to split an epic or an oversized story candidate.
- `references/backlog-structure.md` — load when structuring the epic list,
  judging Sprint-sized readiness, or explaining refinement and sizing
  roles (steps 3, 6, 8), and for Kanban differences.

## Checklist

- [ ] Every epic is phrased as a user or business outcome, not a component.
- [ ] Every story candidate traces to the input document; nothing invented.
- [ ] Every story candidate is a one-liner tagged with its split pattern —
      no narratives or acceptance criteria (that is `user-story-writer`).
- [ ] No candidate obviously exceeds one Sprint; oversized ones re-split.
- [ ] Dependencies listed only where real; open questions listed instead
      of assumptions.
- [ ] Output follows the template above, including the Handoff section.
