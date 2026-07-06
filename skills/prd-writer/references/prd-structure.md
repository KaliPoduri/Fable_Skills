# PRD structure — what each section must contain

Distilled from: Atlassian Agile Coach, "What is a Product Requirements
Document (PRD)?" (https://www.atlassian.com/agile/product-management/requirements)
and the Atlassian Confluence PRD template
(https://www.atlassian.com/software/confluence/templates/product-requirements).
Both verified 2026-07-06. Cagan/SVPG principles cross-referenced from
references/requirements-quality.md.

## The agile framing (Atlassian)

- A PRD defines the purpose, features, and behavior of a product or
  feature. Its job is to build SHARED UNDERSTANDING among product,
  engineering, design, and stakeholders — not to be a contract.
- Prefer lightweight: a PRD for a large, complex epic; plain backlog items
  for small well-understood work. If the user's request is one small story,
  say so and suggest going straight to user-story-writer.
- Effective agile PRDs center on: goals, assumptions, user stories/needs,
  design references, and clear OUT-OF-SCOPE items. They stay flexible —
  a living document updated as the team learns, not frozen at kickoff.
- One page people actually read beats twenty pages nobody does. Link to
  research, designs, and technical docs instead of embedding them.

## Section-by-section quality bar

### Header block (participants, status, target release)
Purpose: orient a reader in 10 seconds. Must name an owner (one person),
a status (Draft / In review / Approved), and a target release or explicit
TBD. Stale headers destroy trust in the whole document — include a
Last-updated date.

### Problem statement
Who is affected, what they cannot do today, evidence it matters, cost of
doing nothing. The test: a reader who stops here can still explain why the
project exists. Zero solution language — if a sentence names a UI element,
an architecture, or a vendor, move it out or delete it.

### Goals / Objectives
2–5 outcomes, each measurable, each explaining how the work supports a
larger organizational goal (Atlassian: the Objective section links feature
to company goals). "Improve UX" is not a goal; "cut task completion time
for X from 4 min to 1 min" is.

### Non-goals ("Not doing")
Atlassian calls this out explicitly: listing what you are NOT doing is as
important as what you are. Each non-goal gets a one-line reason. Non-goals
(never, on purpose) are distinct from out-of-scope (not this release).
This section is the primary defense against scope creep.

### Target users
For each user type: who they are, their goal, key tasks, environment.
If the org has personas, reference them by name; do not re-invent. If not,
define minimal user types and record them under Assumptions.

### Assumptions
User, technical, and business assumptions (Atlassian template groups them
this way). Each must be falsifiable. The dangerous ones — those that, if
wrong, kill the product — get flagged as risks with a validation plan.

### Scope (in / out)
In-scope: the capability areas this release covers. Out-of-scope: deferred
items, each with a home (backlog, next release, or open question). Never
leave a stakeholder's pet feature silently absent — put it in one of the
two lists.

### Functional requirements
See references/requirements-quality.md for the writing rules. Structure:
ID (FR-n), statement, priority, traceability to a goal. Group by user
scenario, not by system component — the PRD describes user value.

### Non-functional requirements / release criteria
See references/requirements-quality.md, "Release criteria". Every category
gets a decision: a measurable requirement or an explicit "not a constraint
for this release". Silence is the failure mode.

### Success metrics
Atlassian template: a success-metrics table alongside goals. Each row:
metric, baseline, target, measurement method and timing. If no baseline
exists, the first milestone is "instrument and measure baseline".

### Risks
Three families: product risk (users do not want it), delivery risk (team
cannot build it in time/quality), dependency risk (blocked on another
team, system, or decision). Each gets a mitigation or an escalation owner.

### Open questions
Atlassian template includes an open-questions tracking table: question,
owner, needed-by (and answer + date once resolved). This is where honest
PRDs put everything they do not know. An empty open-questions section in a
Draft PRD is a red flag, not an achievement.

## Anti-patterns to reject

- Solution-in-disguise: requirements that prescribe implementation
  ("use a message queue") instead of outcome ("orders must survive a
  processing-node crash").
- Spec-novel: >2 pages of prose before the first requirement. Cut or link.
- Frozen document: no Last-updated, no status, no owner.
- Wish-list goals: goals with no metric row.
- Missing "not doing": every stakeholder assumes their item is in.
