# Output eval cases (≥3)

Each case is run twice — WITH the skill installed and WITHOUT (raw
assistant) — and scored against the rubric in
docs/AUTHORING-GUIDE.md §Eval thresholds. The skill must beat raw output.

## Case 1

- Prompt: "Write an ADR: we chose PostgreSQL over MongoDB and MySQL for
  order storage because of transactions and existing ops experience."
- Input artifacts (if any): empty repo, no decision log yet.
- Rubric focus: template compliance, completeness.
- Expected qualities: MADR 4.0.0 structure with frontmatter (status,
  date, decision-makers); file path `docs/decisions/0001-...` (or 0000
  bootstrap offered); all three options under Considered Options AND
  Pros and Cons with Good/Neutral/Bad bullets — losing options' pros
  present; Decision Outcome justification references the stated drivers;
  no invented rationale beyond the prompt without asking.

## Case 2

- Prompt: "Our ADR 0004 about in-process caching is obsolete now that we
  moved to Redis. Handle it."
- Input artifacts (if any): docs/decisions/ with records 0001-0006,
  including 0004-use-in-process-caching.md (status: accepted).
- Rubric focus: source accuracy (lifecycle), actionability.
- Expected qualities: NEW record 0007 for the Redis decision; 0004
  substance untouched except status changed to "superseded by ADR-0007"
  and date updated; two-way cross-links in More Information; does not
  renumber or delete anything.

## Case 3

- Prompt: "Record our decision to adopt trunk-based development. The
  existing log uses Nygard-style ADRs in doc/arch/."
- Input artifacts (if any): doc/arch/ with adr-001.md..adr-009.md in
  Nygard format (Status/Context/Decision/Consequences).
- Rubric focus: actionability, judgment (consistency over convention).
- Expected qualities: matches the EXISTING log's format, location, and
  numbering (adr-010) instead of imposing MADR/docs/decisions; optionally
  offers a migration decision as a separate record; decision content
  still covers context, options considered, and consequences.
