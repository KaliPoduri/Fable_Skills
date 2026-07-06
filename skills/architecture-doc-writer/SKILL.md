---
name: architecture-doc-writer
description: Writes arc42 v9 architecture docs with embedded C4 model views. Use this skill when asked to write an architecture document or arc42 doc. Do not use for a standalone diagram or a single decision record; use c4-diagrammer or adr-writer instead. Covers quality goals, constraints, context and scope, solution strategy, building blocks, runtime and deployment views, crosscutting concepts, decisions, risks, and glossary.
metadata:
  version: "1.0.0"
  last-verified: "2026-07-06"
---

# Architecture Doc Writer

Produce a complete software architecture document structured by the arc42
template version 9 (arc42.org), with C4 model views (c4model.com) embedded
in the sections where they belong: context diagram in section 3, container
and component diagrams in section 5, dynamic diagrams in section 6, and a
deployment diagram in section 7. The result is a single Markdown document
a new team member can read end to end to understand the system.

## Constraints

Assume no external internet access, no paid tools, and English output.
Never send project code or data to external services.
Stay technology-agnostic: describe the stack the project actually uses;
never recommend replacing it unless asked.
Write diagrams as Mermaid text blocks so they render offline; keep each
diagram to one abstraction level.
Base every statement on project evidence (code, configs, existing docs,
user answers). Mark anything you could not confirm as `[assumption]`.

## Workflow

1. Gather evidence. Read existing docs (README, wikis, ADRs), build and
   deployment configs, and the top-level code structure. List what you
   found and what is missing.
2. Ask before inventing. If quality goals, stakeholders, or constraints
   are unknown, ask the user 3-7 focused questions in one batch (e.g.
   "top 3 quality goals?", "hard deadlines or mandated tech?",
   "who reads this document?"). Do not fabricate business context.
3. Confirm scope and depth. Agree which arc42 sections get full treatment
   and which get a one-paragraph stub. Small systems: sections 1-5 full,
   6-12 brief. Load `references/arc42-sections.md` now for per-section
   intent and anti-patterns.
4. Draft sections 1-2: quality goals as a ranked top-3-to-5 table with
   measurable scenarios; constraints split into technical, organizational,
   and conventions.
5. Draft section 3 (context and scope): business context table (partner,
   input, output) plus a C4 system context diagram. Load
   `references/c4-embedding.md` before writing any diagram.
6. Draft section 4 (solution strategy): a short table mapping each quality
   goal to the architectural approach that achieves it.
7. Draft section 5 (building block view): level-1 container diagram plus a
   blackbox table (name, responsibility, interfaces) per building block.
   Add level-2 component decomposition only for the 1-2 most important
   containers.
8. Draft section 6 (runtime view): pick 3-5 architecturally significant
   scenarios (main use case, startup, failure path) and describe each with
   a short numbered walkthrough; add a C4 dynamic or Mermaid sequence
   diagram for the most complex one.
9. Draft section 7 (deployment view): infrastructure diagram plus a table
   of nodes, their technology, and what runs where.
10. Draft sections 8-12: crosscutting concepts (only ones that actually
    span building blocks); architectural decisions as links to ADRs — if
    key decisions are unrecorded, list them and suggest the adr-writer
    skill rather than inlining full ADRs; quality requirements as concrete
    scenarios (stimulus, environment, response, measure); top 5-10 risks
    and technical debt items with mitigation; glossary of domain and
    technical terms.
11. Self-review against the Checklist below, fix gaps, then deliver the
    document plus a short list of open `[assumption]` items for the user
    to confirm.

## Output template

Produce one Markdown document with exactly these top-level headings
(arc42 v9 section names and order):

```markdown
# <System name> — Architecture Documentation

> Based on arc42 template v9 (arc42.org). Status: <draft|reviewed>.
> Last updated: <YYYY-MM-DD>.

## 1. Introduction and Goals
### 1.1 Requirements Overview
### 1.2 Quality Goals
### 1.3 Stakeholders

## 2. Architecture Constraints

## 3. Context and Scope
### 3.1 Business Context
### 3.2 Technical Context

## 4. Solution Strategy

## 5. Building Block View
### 5.1 Level 1 — Whitebox Overall System
### 5.2 Level 2 — <important container(s)>

## 6. Runtime View

## 7. Deployment View

## 8. Crosscutting Concepts

## 9. Architecture Decisions

## 10. Quality Requirements
### 10.1 Quality Overview
### 10.2 Quality Scenarios

## 11. Risks and Technical Debt

## 12. Glossary
```

Formatting rules:

- Quality goals (1.2): table with Priority, Quality Goal, Concrete Scenario.
- Stakeholders (1.3): table with Role, Contact/Team, Expectation.
- Context (3): C4 system context diagram + table of neighbors (Partner,
  Input, Output, Protocol/Channel).
- Building blocks (5): container diagram + one blackbox table per block
  (Name, Responsibility, Interfaces).
- Runtime (6): one `### Scenario: <name>` per scenario with a numbered
  step list; diagram only where steps alone are unclear.
- Deployment (7): deployment diagram + node table (Node, Technology,
  Deployed artifacts).
- Decisions (9): table with ID, Title, Status, Link (to `docs/decisions/`).
- Risks (11): table with Risk/Debt, Probability, Impact, Mitigation.
- Glossary (12): two-column Term/Definition table.

## Sizing and tailoring

Match document depth to system size and audience; arc42 is explicitly
tailorable, but the 12 headings and their order never change.

| System | Full sections | Stubbed sections | Diagrams |
|---|---|---|---|
| Small tool / single service | 1, 2, 3, 5 | 4, 6-12 one-liners | context + container |
| Typical product (3-10 containers) | 1-7, 9, 11 | 8, 10, 12 brief | context, container, 1 dynamic, deployment |
| Platform / many teams | all 12 | none | full set + level-2 components for risky containers |

Stub format for a section with nothing notable:
`_Nothing architecturally significant. <one sentence why>._` — keep the
heading so readers can trust the structure.

When updating an EXISTING architecture document:

- Keep its section structure if it is already arc42; map content into
  arc42 v9 order only when the user asks for a restructure.
- Diff reality against the doc first (containers in deploy configs vs
  section 5) and lead with a "drift found" list before rewriting prose.
- Never silently delete sections someone else wrote; move outdated
  content to an appendix or flag it for removal.

## Pitfalls

- Backlog dump in 1.1 — link the requirements source, list only the
  architecture-driving ones.
- Unmeasurable quality goals ("fast", "secure") — force a number or a
  concrete scenario per goal.
- Internal detail in section 3 — the system stays one black box there.
- Diagram-table drift in section 5 — every box in the container diagram
  needs a blackbox table entry, and vice versa.
- Restating ADRs in section 9 — link them; write new ones via adr-writer.
- Textbook filler in section 8 — only concepts this team actually
  decided and applies across blocks.
- Empty risk section 11 — every real system has risks; ask the team
  what keeps them up at night rather than writing "none known".

## References (load on demand)

- `references/SOURCES.md` — source manifest (always present).
- `references/arc42-sections.md` — load in step 3: per-section purpose,
  minimum content, and anti-patterns for all 12 arc42 v9 sections.
- `references/c4-embedding.md` — load in step 5 before writing any
  diagram: which C4 view goes in which arc42 section, plus minimal
  Mermaid patterns for context, container, dynamic, and deployment views.

## Checklist

- [ ] All 12 arc42 v9 sections present, in order, none renamed.
- [ ] Quality goals: 3-5, ranked, each with a measurable scenario.
- [ ] Section 3 has a C4 context diagram; section 5 a container diagram;
      section 7 a deployment view; each diagram has a title and shows one
      abstraction level.
- [ ] Every building block in a diagram also appears in a blackbox table.
- [ ] Section 9 links out to ADRs instead of restating them; missing ADRs
      are flagged for adr-writer.
- [ ] No fabricated facts: every unconfirmed statement is tagged
      `[assumption]` and listed at the end.
- [ ] Output follows the template above.
