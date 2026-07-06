# Backlog structure, readiness, and sizing

Distilled from: Ken Schwaber & Jeff Sutherland, The Scrum Guide, November
2020, https://scrumguides.org/scrum-guide.html (verified 2026-07-06).
Kanban notes are library guidance for teams not running Sprints.

## What the Product Backlog is

- "An emergent, ordered list of what is needed to improve the product."
- It is "the single source of work undertaken by the Scrum Team" — epics
  and story candidates produced by this skill are Product Backlog items
  (PBIs) in different states of refinement; the Scrum Guide itself does
  not prescribe the terms "epic" or "story", they are conventions layered
  on top of PBIs.
- The Product Owner is accountable for the Product Backlog and its
  ordering; this skill proposes structure, it does not decide priority.
  Carry priority over from the input document where stated; otherwise
  leave the Priority column for the Product Owner.

## Refinement

- "Product Backlog refinement is the act of breaking down and further
  defining Product Backlog items into smaller more precise items." That
  act is exactly what this skill performs on a PRD or epic.
- Refinement is ongoing, not a one-shot: expect the breakdown produced
  here to be revisited as the team learns. Mark uncertainty as Open
  questions rather than freezing guesses into the backlog.

## Readiness and the one-Sprint rule

- "Product Backlog items that can be Done by the Scrum Team within one
  Sprint are deemed ready for selection" in Sprint Planning.
- Practical test for step 6 of the workflow: if the team could plausibly
  finish the candidate — including testing and meeting the Definition of
  Done — inside one Sprint, it is small enough. If not, split again using
  references/splitting-patterns.md.
- Epics are, by this definition, never ready: they exist to be split.

## Sizing

- "The Developers who will be doing the work are responsible for the
  sizing." The Product Owner may influence by clarifying and negotiating.
- Therefore the S/M/L size hints this skill emits are conversation
  starters for refinement, not estimates. Never present them as
  commitments, and never sum them into a forecast.
- Keep hints relative (S/M/L against the other candidates in the same
  breakdown), not absolute (days, points).

## Kanban differences

Where the SKILL.md workflow says "one Sprint", Kanban teams substitute:

- Size gate: items sized so they flow within the team's target cycle time
  (or an agreed maximum item age), instead of fitting a Sprint.
- Cadence: refinement happens on demand as items approach the commitment
  point, not toward a Sprint Planning event.
- Ordering: still a single ordered backlog; WIP limits, not Sprint
  capacity, constrain how much gets pulled.

The epic/story structure, splitting patterns, dependency notes, and
relative size hints are unchanged under Kanban.
