---
name: prd-writer
description: "Writes a Product Requirements Document (PRD): problem, goals, scope, requirements, metrics. Use this skill when asked to write a PRD or requirements doc for a feature. Do not use to split work into epics or stories; use epic-story-breakdown instead. Do not use for product vision or roadmap docs; use product-vision-writer or product-roadmap-writer instead. PRD output feeds user-story-mapper, then epic-story-breakdown, then user-story-writer."
metadata:
  version: "1.0.0"
  last-verified: "2026-07-06"
---

# PRD Writer

Write a Product Requirements Document that gives a team shared understanding
of WHAT to build and WHY — problem statement, goals and non-goals, target
users, scope, functional and non-functional requirements, success metrics,
risks, and open questions. Describe the problem and required outcomes, not
the implementation. This skill is the top of the story chain: its output is
consumed by user-story-mapper, then epic-story-breakdown, then
user-story-writer.

## Constraints

Assume no external internet access, no paid tools, and English output.
Never send project code or data to external services.
Technology-agnostic: name capabilities and qualities, not frameworks or
vendors, unless the user's context already fixes them.
State requirements as problems and outcomes, never as implementation
designs (Cagan: requirements are not design).
A PRD is a living document — mark unknowns as open questions instead of
inventing answers.

## Workflow

1. Collect context. Read any material the user points to (feature briefs,
   tickets, notes, existing docs in the repo). List what you know about:
   the problem, who has it, evidence it matters, business goal it serves,
   and any hard constraints (deadline, platform, compliance).
2. Ask before inventing. If the problem statement, target users, or the
   primary business goal are missing, ask the user 3–6 focused questions in
   one batch. Do not fabricate market data, user research, or metrics
   baselines. Anything still unknown after asking goes into Open questions.
3. Frame the problem. Write 2–4 sentences: who is affected, what they
   cannot do today, why it matters now, and the cost of doing nothing.
   No solution language in this section.
4. Set goals and non-goals. 2–5 measurable goals tied to the business
   objective. List explicit non-goals ("Not doing") — scope you are
   deliberately excluding this release. Every stakeholder debate you can
   settle here saves a scope fight later (Atlassian: out-of-scope items are
   a core PRD element).
5. Define target users. For each user type: who they are, their goal, the
   key tasks they perform, and their environment. Use the user types the
   organization already names; otherwise define 1–3 and mark them as
   assumptions.
6. Record assumptions. User, technical, and business assumptions, each
   phrased so it can be proven false. Question them: which, if wrong,
   invalidates the product? Flag those as validation risks.
7. Write functional requirements. Number them FR-1, FR-2, … Each states a
   required capability from the user's perspective, is testable, and has a
   priority (Must / Should / Could). Group related requirements under the
   scenario or user goal they serve. Load references/prd-structure.md for
   the quality bar per section.
8. Write non-functional requirements and release criteria. Number them
   NFR-1, NFR-2, … Cover, at minimum, a decision (requirement or explicit
   "not a constraint for this release") for: performance, scalability,
   reliability, usability, supportability, security/privacy, and
   localizability. Load references/requirements-quality.md when writing or
   reviewing FRs/NFRs.
9. Define success metrics. For each goal: metric, current baseline (or
   "baseline unknown — measure first"), target value, and when/how it is
   measured. A goal without a metric is a wish — either add one or demote
   the goal.
10. List risks and mitigations. Product risks (nobody wants it), delivery
    risks (cannot build it in time), and dependency risks (waiting on
    another team/system). One-line mitigation or escalation owner each.
11. Collect open questions. Table of question / owner / needed-by date.
    Every invented fact you avoided in step 2 must appear here.
12. Assemble the document using the Output template below, run the
    Checklist, then present the PRD and point the user to the next step in
    the chain (user-story-mapper or epic-story-breakdown).

## Output template

Produce a Markdown document with exactly these headings, in this order:

```markdown
# PRD: <feature or product name>

| Field | Value |
|---|---|
| Author | <name> |
| Status | Draft / In review / Approved |
| Target release | <release or date, or TBD> |
| Stakeholders | <names/roles> |
| Last updated | <YYYY-MM-DD> |

## 1. Problem statement
<2–4 sentences: who, what they cannot do, why now, cost of doing nothing.>

## 2. Goals
- G1: <measurable goal>
### Non-goals (not doing)
- <explicitly excluded scope, with one-line reason>

## 3. Target users
### <User type 1>
- Who: … | Goal: … | Key tasks: … | Environment: …

## 4. Assumptions
- A1 (user/technical/business): <falsifiable statement>

## 5. Scope
### In scope
### Out of scope
<Out of scope = deferred; Non-goals = deliberately never.>

## 6. Functional requirements
| ID | Requirement | Priority | Rationale / linked goal |
|---|---|---|---|
| FR-1 | <capability, testable> | Must | G1 |

## 7. Non-functional requirements & release criteria
| ID | Category | Requirement | Priority |
|---|---|---|---|
| NFR-1 | Performance | <measurable> | Must |

## 8. Success metrics
| Goal | Metric | Baseline | Target | Measured how/when |
|---|---|---|---|---|

## 9. Risks & mitigations
| Risk | Type (product/delivery/dependency) | Mitigation / owner |
|---|---|---|

## 10. Open questions
| Question | Owner | Needed by |
|---|---|---|

## 11. Next steps
<Hand-off note: run user-story-mapper / epic-story-breakdown on sections 3–6.>
```

Keep the whole PRD readable in one sitting; link out to research or design
artifacts rather than pasting them in.

## References (load on demand)

- `references/SOURCES.md` — source manifest (always present).
- `references/prd-structure.md` — load when drafting or reviewing the
  document sections (what each section must contain, per Atlassian and
  Cagan/SVPG).
- `references/requirements-quality.md` — load when writing or critiquing
  functional/non-functional requirements, assumptions, or release criteria.

## Checklist

- [ ] Problem statement contains no solution or implementation language.
- [ ] Every goal is measurable and has a row in Success metrics.
- [ ] Non-goals / "not doing" section is present and non-empty.
- [ ] Every FR is testable, prioritized, and traceable to a goal.
- [ ] Every NFR category in step 8 has a requirement or an explicit waiver.
- [ ] No invented facts: unknowns appear in Open questions, not as claims.
- [ ] Document uses the exact headings of the Output template.
- [ ] Hand-off to user-story-mapper / epic-story-breakdown is noted; no
      epics or stories were written here.
