# Story splitting patterns

Distilled from: Mike Cohn, "Five Simple but Powerful Ways to Split User
Stories" (SPIDR), Mountain Goat Software,
https://www.mountaingoatsoftware.com/blog/five-simple-but-powerful-ways-to-split-user-stories
(verified 2026-07-06); and Richard Lawrence & Peter Green, "The Humanizing
Work Guide to Splitting User Stories",
https://www.humanizingwork.com/the-humanizing-work-guide-to-splitting-user-stories/
(verified 2026-07-06).

Goal of every split: smaller pieces that each still deliver observable
value, not horizontal technical layers. A "front-end story" plus a
"database story" is a slice through architecture, not a split.

## SPIDR (Cohn)

Five techniques; the acronym is the working set to try on any stuck story.

| Letter | Technique | Split by | Example |
|---|---|---|---|
| S | Spike | Extracting a research activity when uncertainty, not size, blocks the story | "Investigate how invoice tax rules vary by region" precedes the invoicing story |
| P | Path | Alternate routes a user can take through the story | Pay by card / pay by saved card / pay by voucher become separate stories |
| I | Interface | Browser, device, hardware, or UI variation | Ship the Chrome-only version first; other browsers as later stories; plain form before rich editor |
| D | Data | Restricting or simplifying the data handled first | Support one currency, one locale, or clean data first; edge-case data later |
| R | Rules | Temporarily relaxing business rules | Ignore fraud limits in the first story; enforce them in a follow-up story |

Usage notes:
- Spike is the fallback: use it when no other technique applies because the
  team cannot see into the story. Timebox it; its output is knowledge, not
  product.
- Path splits often hide inside a single sentence ("user checks out") —
  draw or list the paths to find them.
- Rules splits must be visibly flagged so the relaxed rule is never
  mistaken for done.

## Humanizing Work patterns (Lawrence & Green)

Nine patterns; the first three below are named explicitly in the SKILL.md
workflow, the rest are close variants to reach for when the first three
fail.

1. **Workflow steps** — Break a multi-step business process into a thin
   end-to-end slice first (the simplest walk through the whole workflow),
   then add stories that enrich individual steps. Do not build step 1
   completely before step 2 exists.
2. **Operations (CRUD)** — "Manage X" almost always hides Create, Read,
   Update, Delete. Split into one story per operation; Create + Read
   usually form the earliest valuable pair.
3. **Business rule variations** — Each rule or rule cluster becomes its
   own story ("flag weekend transactions", "flag transactions over limit").
4. **Data variations** — Same behavior, different data shapes: start with
   one data type, locale, or format; add variations as separate stories.
   (Overlaps SPIDR-D.)
5. **Data entry methods** — Split simple UI from elaborate UI: plain date
   field first, calendar picker later.
6. **Major effort** — When one path carries most of the implementation
   cost, do it first ("pay with one card type"), then add the cheap
   variations.
7. **Simple/complex** — Extract the simple core ("search flights between
   two cities") and push each complication ("flexible dates", "nearby
   airports") into its own story.
8. **Defer performance** — Make it work, then make it fast: functional
   story first, performance target as a separate story with a measurable
   threshold.
9. **Break out a spike** — Same as SPIDR-S: when the team cannot estimate
   or split, extract a timeboxed learning story. (Last resort.)

Meta-pattern (Lawrence & Green): find what varies in the story — steps,
rules, data, interfaces, effort — and reduce the variation in the first
slice. Every pattern above is an instance of this.

## Choosing a pattern

1. Try workflow steps for anything process-shaped.
2. Try SPIDR Path/Interface/Data/Rules for anything option-shaped.
3. Try CRUD for anything "manage"-shaped.
4. Try business-rule / data variations when the story is policy-heavy.
5. Spike only when uncertainty is the blocker.

Evaluate the result: after a split, every piece should be roughly
Sprint-sized, roughly equally valuable to a user or stakeholder, and not a
technical layer. If one piece got all the value, re-split with a different
pattern.
