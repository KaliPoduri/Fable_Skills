# ADR lifecycle, numbering, and log conventions

Sources: https://adr.github.io/ (ADR overview; references Michael
Nygard's 2011 "Documenting Architecture Decisions") and MADR 4.0.0 docs,
https://adr.github.io/madr/ (both verified 2026-07-06). Distilled for
offline use.

## What an ADR is

An Architectural Decision Record captures ONE architecturally significant
decision and its rationale — trade-offs and consequences included. The
collection of a project's ADRs is its decision log. The log's value is
historical: readers learn why the system is the way it is and which
alternatives were already examined (and why they lost).

## Architecturally significant?

A decision is ADR-worthy when it affects one or more of:

- structure (introducing/removing/splitting components or services),
- non-functional characteristics (performance, security, availability,
  maintainability targets),
- dependencies (new framework, library, external service),
- interfaces (public APIs, contracts, protocols),
- construction techniques (build, test, deployment approach).

Not ADR-worthy: reversible local choices with no cross-team impact
(variable naming, one internal helper library among equals). When in
doubt, a short ADR is cheaper than a forgotten rationale.

## Status lifecycle

```
            +-> rejected (kept in the log)
proposed ---+
            +-> accepted --+--> deprecated              (no replacement)
                           +--> superseded by ADR-NNNN  (replacement exists)
```

- `proposed`: drafted, deciders have not agreed yet.
- `rejected`: deciders said no. Keep the file — a rejected option
  resurfaces every 18 months without it.
- `accepted`: in force. Substance is now frozen.
- `deprecated`: no longer in force, nothing replaces it.
- `superseded by ADR-NNNN`: replaced by a newer decision.

Rules:

- ADRs are immutable after acceptance: fix typos freely, but changed
  circumstances produce a NEW ADR, never an edit of the old rationale.
- Supersession is two-sided: new ADR links the old one in More
  Information ("Supersedes ADR-0042"); old ADR's status becomes
  `superseded by ADR-NNNN`. Date on the old record updates (date = last
  updated).
- A superseded ADR may itself supersede others — chains are normal.

## Numbering and filenames (MADR convention)

- Directory: `docs/decisions/` (MADR default). Respect an existing log's
  location (`docs/adr/`, `adr/`, `doc/arch/`) — consistency beats
  convention.
- Filename: `NNNN-title-with-dashes.md` — consecutive four-digit number,
  lowercase title words joined by dashes, `.md`.
  Example: `0005-use-postgresql-for-order-storage.md`.
- Numbers are never reused, even for rejected or superseded records.
- Large projects may use subdirectories per area (`decisions/backend/`,
  `decisions/ui/`); numbering then runs per subdirectory or globally —
  match whatever the log already does.
- A conventional first record in a fresh log:
  `0000-use-madr-for-adrs.md` — the decision to record decisions, which
  fixes template, directory, and numbering in writing.

## Joining an existing log

1. List the existing records; find the highest number and the template
   actually in use (frontmatter or inline "Status:" line, section names).
2. Match the existing style even if it is Nygard-style (Status/Context/
   Decision/Consequences) rather than MADR — a mixed log is worse than an
   older template. Offer a migration ADR if the team wants to switch.
3. If an index file (README/index.md) lists records, append the new one.

## Relationship to other documents

- The architecture document (arc42 section 9 — see the
  architecture-doc-writer skill) links to ADRs; it never restates them.
- Proposals still under open-ended discussion belong in an RFC
  (rfc-writer skill, future); when the discussion converges, the outcome
  is condensed into an ADR.
