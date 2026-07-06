# arc42 v9 — per-section guidance

Source: arc42 template v9, https://arc42.org/overview and
https://docs.arc42.org/home/ (verified 2026-07-06). Distilled for offline
use; wording condensed, section names and order are normative.

arc42 answers two questions: WHAT to document about an architecture and
HOW to communicate it. v9 change vs v8: section 10 (Quality Requirements)
was restructured into 10.1 overview + 10.2 details.

## 1. Introduction and Goals

Purpose: why the system exists and what "good" means for it.

- 1.1 Requirements overview: the 3-7 driving functional requirements in
  one table or short list; link to the full requirements source. Do NOT
  paste the whole backlog.
- 1.2 Quality goals: the TOP 3-5 quality attributes for the architecture,
  ranked, each with a concrete motivating scenario ("p95 search response
  under 500 ms at 1,000 concurrent users"). Vague words ("fast",
  "scalable") without a measure are an anti-pattern.
- 1.3 Stakeholders: who must know/approve the architecture — role,
  contact, expectation. Missing stakeholders cause rework later.

## 2. Architecture Constraints

Anything that limits freedom of design decisions, split into:
technical (mandated OS, middleware, languages), organizational
(team, budget, schedule, process, legal/compliance), and conventions
(coding standards, naming, documentation rules). One table per group;
give the reason for each constraint. Anti-pattern: listing choices the
team made freely — those belong in section 4 or 9.

## 3. Context and Scope

Separates the system from ALL external partners (users, neighboring
systems, hardware). Defines the external interfaces.

- 3.1 Business context: partners and the business data/events exchanged.
  Table: Partner | Input | Output. Add a C4 system context diagram.
- 3.2 Technical context: channels, protocols, hardware links (HTTPS,
  message queue, file share) and the mapping business I/O -> channel.
  Only needed where it differs meaningfully from 3.1.

Anti-pattern: showing internal building blocks here — the system is ONE
black box in this section.

## 4. Solution Strategy

Short summary (under one page) of the fundamental decisions and solution
approaches: technology choices, top-level decomposition pattern
(e.g. layers, hexagonal, microservices), and the approach for reaching
each top quality goal. Best form: table Quality goal | Approach |
Details in section. Everything here is expanded elsewhere — keep it dense.

## 5. Building Block View

Static decomposition of the system into modules/containers/components,
as a hierarchy of white boxes and black boxes.

- Level 1 (whitebox overall system): the containers/subsystems and their
  relationships. Embed a C4 container diagram. For EVERY block shown, add
  a blackbox description: name, responsibility (1-2 sentences),
  interfaces. Undocumented boxes on a diagram are an anti-pattern.
- Level 2: zoom into the 1-2 most important or riskiest containers
  (C4 component diagram). Stop decomposing when a block is obvious to
  its implementers — arc42 explicitly allows pruning depth.

## 6. Runtime View

Behavior: how building blocks interact at runtime in a FEW architecturally
significant scenarios (main use case, startup/initialization, error and
failure handling, scaling events). 3-5 scenarios is normal. Numbered step
list per scenario; add a sequence/dynamic diagram only where prose is
unclear. Anti-pattern: documenting every use case — pick the ones that
show the architecture working.

## 7. Deployment View

Technical infrastructure: environments, nodes, processors, channels, and
the mapping of building blocks to infrastructure. Diagram plus a table:
Node | Technology | Deployed artifacts. Document each environment that
differs (prod vs staging) but avoid duplicating identical ones.

## 8. Crosscutting Concepts

Overall regulations and solution ideas relevant in MULTIPLE building
blocks: domain model, persistence, security, logging/monitoring, error
handling, i18n, configuration, session handling, build/deploy conventions.
Document only concepts that are actually decided and span blocks — an
empty section is better than generic textbook content. One `###` heading
per concept, a few sentences each; link to code where the concept lives.

## 9. Architecture Decisions

Important, expensive, critical, or risky decisions including rationale.
Keep full decision records OUTSIDE this document as ADRs (see the
adr-writer skill; MADR format, files under docs/decisions/). Here: a table
ID | Title | Status | Link. If key decisions are undocumented, list them
as gaps rather than reconstructing rationale from memory.

## 10. Quality Requirements

The full quality tree/overview beyond the top goals of 1.2.

- 10.1 Quality overview: the quality attributes that matter, e.g. as a
  mind-map/tree or table, prioritized.
- 10.2 Quality scenarios: concrete, testable scenarios per attribute —
  stimulus, environment, expected response, measure. Usage scenarios
  (runtime behavior) and change scenarios (modifiability) both count.

v9 note: this overview/details split (10.1/10.2) is the v9 restructuring.

## 11. Risks and Technical Debt

Known risks and accumulated debt, ordered by priority. Table: Risk/Debt |
Probability | Impact | Mitigation/Plan. Be honest — this section is for
the team and its future self, not for marketing. Suggested scan areas:
single points of failure, outdated dependencies, missing tests around
core flows, knowledge concentrated in one person.

## 12. Glossary

Domain and technical terms that readers might interpret differently, as a
Term | Definition table, alphabetized. Include translations if the team
works in more than one language. Anti-pattern: defining common industry
terms nobody disputes.

## Tailoring guidance

arc42 is intentionally tailorable: every section is optional except that
the numbering/order never changes. For small systems produce sections
1-5 fully and 6-12 as short stubs with a one-line "nothing notable"
statement rather than deleting the heading — readers rely on the stable
structure.
