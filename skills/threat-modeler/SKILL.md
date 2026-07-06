---
name: threat-modeler
description: Threat models system designs — assets, trust boundaries, STRIDE-per-element, risk ranking, threat register, mitigations. Use this skill when asked to threat model a design or run STRIDE analysis. Do not use for code review; use code-reviewer instead. For finding vulnerabilities in written code use security-code-reviewer; for testable security requirements use security-requirements-writer. Covers architecture security threat analysis and trust-boundary diagrams.
metadata:
  version: "1.0.0"
  last-verified: "2026-07-06"
---

# Threat Modeler

Produce a design-stage threat model for a described or documented system:
decompose it into assets, entry points, trust boundaries, and elements;
enumerate threats with STRIDE-per-element; rank risks; map mitigations to
every threat; and deliver a threat model document with a numbered threat
register (TM-1, TM-2, ...). Structure follows the four questions: what are
we working on, what can go wrong, what are we going to do about it, did we
do a good enough job.

## Constraints

Assume no external internet access, no paid tools, and English output.
Never send project code or data to external services.
Model the design as described. Do not invent architecture details — mark
every guess as an explicit assumption in the output.
This is analysis of a DESIGN, not a penetration test, code audit, or
compliance assessment; findings are candidate threats, not confirmed
vulnerabilities.
Stay technology-agnostic in mitigations unless the user names the stack.
Designing or reshaping the API contract itself belongs to api-designer;
threat-model the design you are given.

## Workflow

1. **Scope the system (what are we working on?).** From the description,
   diagrams, or docs provided, capture: the system's purpose, in-scope and
   out-of-scope components, the data it handles and how sensitive that data
   is, and who operates and uses it. List assumptions where information is
   missing; if a missing fact would change the model materially (e.g.
   internet-facing or not), ask.
2. **Decompose the system.** Load `references/threat-modeling-process.md`.
   Identify:
   - **Assets** — data and capabilities worth protecting, with sensitivity.
   - **Actors and entry points** — every way anything enters the system
     (UIs, APIs, queues, file imports, admin channels).
   - **Elements** — classify each component as external entity, process,
     data store, or data flow.
   - **Trust boundaries** — where the level of trust changes (internet to
     DMZ, service to database, user to admin plane, tenant to tenant).
   Render the decomposition as a Mermaid flowchart with trust boundaries as
   subgraphs, or as structured text lists when a diagram adds nothing.
3. **Enumerate threats (what can go wrong?).** Load `references/stride.md`.
   Walk every element and apply only the STRIDE categories that map to its
   element type (processes: all six; data flows and data stores: T, I, D;
   external entities: S, R). Give extra attention to every element and flow
   touching a trust boundary. For each threat write one concrete sentence:
   actor, action, target, consequence — not "tampering may occur".
4. **Rank the risks.** Score each threat Likelihood (High/Medium/Low) and
   Impact (High/Medium/Low), combine via the matrix in
   `references/threat-modeling-process.md` into Risk (Critical/High/
   Medium/Low). Note the rationale in one clause when it is not obvious.
5. **Map mitigations (what are we going to do about it?).** For every
   threat choose a response: **Mitigate** (name the control, tied to the
   STRIDE category's defense class — authentication for S, integrity
   controls for T, etc.), **Eliminate** (remove the feature/flow),
   **Transfer** (shift to another component or party), or **Accept**
   (justify; acceptable only for Low risk). No threat may be left without
   a response.
6. **Build the threat register.** Number threats TM-1, TM-2, ... in the
   register table (format below). Order by risk, highest first.
7. **Validate (did we do a good enough job?).** Confirm: every element was
   walked, every trust-boundary crossing has at least one threat considered
   (or an explicit "none found" note), every threat has a response, and the
   register IDs are contiguous. List open questions and the assumptions
   that most need review by the team.

## Delta mode

When asked what a CHANGE introduces (a new integration, feature, or data
flow added to an existing system), do not remodel the whole estate:

1. Summarize the existing system in three or four lines and mark it as
   context, not scope.
2. Decompose only the new/changed elements, entry points, and any trust
   boundary the change creates or crosses.
3. Enumerate STRIDE only for the new elements and for existing elements
   whose exposure the change alters.
4. Deliver the full Output template; in Scope and assumptions state
   explicitly that unchanged components were not re-analyzed.

## Quality bar for threat entries

Hold every register row to this bar before finishing:

- Statement form: actor, action, target, consequence.
  - Reject: "Tampering may occur on the data flow."
  - Accept: "An on-path attacker modifies sales records in transit between
    client and collection API, corrupting weekly revenue reports."
- Mitigation names a concrete control ("require If-Match with ETag;
  return 412"), not a class ("add integrity checks").
- One primary response per threat; secondary defenses go in the
  Mitigation plan, not extra register columns.
- No duplicate threats restated per downstream consequence — record the
  chain once, where it starts.

## Output template

Produce a single threat model document with exactly these headings:

```markdown
# Threat Model: <system name>

## Scope and assumptions
<Purpose, in/out of scope, data sensitivity. Numbered assumptions A-1, A-2, ...>

## System decomposition
### Assets
### Actors and entry points
### Trust boundaries
### Diagram
<Mermaid flowchart with trust boundaries as subgraphs, or structured text.>

## Threat register
| ID | Element | STRIDE | Threat | Likelihood | Impact | Risk | Response | Mitigation |
|---|---|---|---|---|---|---|---|---|
| TM-1 | ... | S/T/R/I/D/E | <actor does X to Y causing Z> | H/M/L | H/M/L | Critical/High/Medium/Low | Mitigate/Eliminate/Transfer/Accept | <control or justification> |

## Mitigation plan
<Mitigations grouped and ordered by risk; note which are design changes vs
operational controls, and any that block launch.>

## Validation and open questions
<Coverage confirmation, unresolved questions, assumptions needing review.>
```

## References (load on demand)

- `references/SOURCES.md` — source manifest; consult when citing or
  re-verifying any standard.
- `references/stride.md` — load at step 3: STRIDE definitions, the
  category-to-security-property map, the per-element applicability table,
  and mitigation classes per category.
- `references/threat-modeling-process.md` — load at steps 2, 4, and 7:
  four-question framework, decomposition and DFD/Mermaid guidance, risk
  matrix, validation patterns and anti-patterns.

## Checklist

- [ ] Every component is classified as external entity, process, data
      store, or data flow, and every trust boundary is named.
- [ ] STRIDE applied per element type using the applicability table — no
      category skipped for processes, none misapplied to flows/stores.
- [ ] Every threat is a concrete sentence (actor, action, target,
      consequence) with Likelihood, Impact, and Risk assigned.
- [ ] Every threat has a response; Accept appears only on Low risk with a
      written justification.
- [ ] Register IDs are TM-<n>, contiguous, ordered by risk.
- [ ] Assumptions are numbered and listed; material unknowns were asked
      about, not silently guessed.
- [ ] Output follows the Output template headings exactly.
- [ ] No code-level vulnerability findings claimed — that is
      security-code-reviewer's job; no requirements document produced —
      that is security-requirements-writer's job.
