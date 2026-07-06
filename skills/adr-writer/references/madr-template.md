# MADR 4.0.0 — template and field semantics

Source: MADR 4.0.0 (released 2024-09-17), https://adr.github.io/madr/ and
https://github.com/adr/madr/blob/main/template/adr-template.md (verified
2026-07-06). Template reproduced verbatim below, then annotated.

## Verbatim template (adr-template.md)

```markdown
---
status: "{proposed | rejected | accepted | deprecated | … | superseded by ADR-0123}"
date: {YYYY-MM-DD when the decision was last updated}
decision-makers: {list everyone involved in the decision}
consulted: {list everyone whose opinions are sought (typically subject-matter experts); and with whom there is a two-way communication}
informed: {list everyone who is kept up-to-date on progress; and with whom there is a one-way communication}
---

# {short title, representative of solved problem and found solution}

## Context and Problem Statement

{Describe the context and problem statement, e.g., in free form using two to three sentences or in the form of an illustrative story. You may want to articulate the problem in form of a question. Consider adding links to collaboration boards or issue management systems. Make the scope of the decision explicit, for instance, by calling out or pointing at structural architecture elements (components, connectors, ...).}

<!-- This is an optional element. Feel free to remove. -->
## Decision Drivers

* {decision driver 1, for instance, a desired software quality, faced concern, constraint or force}
* {decision driver 2}

## Considered Options

* {title of option 1}
* {title of option 2}
* {title of option 3}

## Decision Outcome

Chosen option: "{title of option 1}", because {justification. e.g., only option, which meets k.o. criterion decision driver | which resolves force {force} | … | comes out best (see below)}.

<!-- This is an optional element. Feel free to remove. -->
### Consequences

* Good, because {positive consequence, e.g., improvement of one or more desired qualities, …}
* Bad, because {negative consequence, e.g., compromising one or more desired qualities, …}

<!-- This is an optional element. Feel free to remove. -->
### Confirmation

{Describe how the implementation / compliance of the ADR can/will be confirmed. Is there any automated or manual fitness function? If so, list it and explain how it is applied. Is the chosen design and its implementation in line with the decision? E.g., a design/code review or a test with a library such as ArchUnit can help validate this. Note that although we classify this element as optional, it is included in many ADRs.}

<!-- This is an optional element. Feel free to remove. -->
## Pros and Cons of the Options

### {title of option 1}

{example | description | pointer to more information | …}

* Good, because {argument a}
* Good, because {argument b}
<!-- use "neutral" if the given argument weights neither for good nor bad -->
* Neutral, because {argument c}
* Bad, because {argument d}

### {title of other option}

{example | description | pointer to more information | …}

* Good, because {argument a}
* Neutral, because {argument b}
* Bad, because {argument c}

<!-- This is an optional element. Feel free to remove. -->
## More Information

{You might want to provide additional evidence/confidence for the decision outcome here and/or document the team agreement on the decision and/or define when/how this decision the decision should be realized and if/when it should be re-visited. Links to other decisions and resources might appear here as well.}
```

## Field semantics

- `status`: current lifecycle state; quoted string. `superseded by
  ADR-0123` names the replacing record explicitly.
- `date`: when the decision was LAST UPDATED, not first drafted.
- `decision-makers`: everyone involved in making the decision
  (accountable). Required in practice — an ADR without owners cannot be
  re-litigated properly.
- `consulted`: two-way communication — subject-matter experts whose
  opinions were sought.
- `informed`: one-way communication — kept up to date, no veto.
- Frontmatter is optional in MADR; keep it — harnesses and tools sort
  logs by it.

Mandatory sections in practice: title, Context and Problem Statement,
Considered Options, Decision Outcome. Everything marked optional above
may be removed — remove rather than pad.

## Filled example (condensed)

```markdown
---
status: "accepted"
date: 2026-07-06
decision-makers: A. Backend lead, B. Platform architect
consulted: DBA team
informed: Frontend guild
---

# Use PostgreSQL for transactional order storage

## Context and Problem Statement

The order service needs ACID transactions across order and payment
records, moderate write volume (~200 TPS peak), and rich ad-hoc
reporting. Which datastore should own transactional order data?

## Decision Drivers

* Strong consistency across order + payment rows
* Ops familiarity: team already runs two PostgreSQL clusters
* License cost must be zero

## Considered Options

* PostgreSQL
* MongoDB
* MySQL

## Decision Outcome

Chosen option: "PostgreSQL", because it is the only option meeting the
consistency driver without new operational surface; the team's existing
clusters cover the ops driver.

### Consequences

* Good, because reporting can reuse existing read replicas
* Bad, because document-shaped order payloads need JSONB mapping

### Confirmation

Schema review by DBA team; ArchUnit-style test asserting no service
bypasses the repository layer.

## Pros and Cons of the Options

### PostgreSQL

* Good, because ACID + JSONB covers both relational and document needs
* Good, because zero new infrastructure
* Bad, because horizontal write scaling needs future work

### MongoDB

* Good, because order documents map naturally
* Bad, because multi-document transactions add operational complexity
* Bad, because no in-house production experience

### MySQL

* Good, because ACID and familiar SQL
* Neutral, because ops experience exists but tooling is Postgres-centric
* Bad, because weaker JSON querying for reporting

## More Information

Revisit if sustained write volume exceeds 1,000 TPS. Related: ADR-0007
(event sourcing rejected).
```
