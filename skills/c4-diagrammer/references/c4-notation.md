# C4 model — levels, elements, notation discipline

Source: C4 model by Simon Brown, https://c4model.com/ (unversioned living
site, verified 2026-07-06). Distilled for offline use. C4 is explicitly
notation-independent and tooling-independent; the abstraction levels and
their meaning are the normative part.

## The abstractions

- **Person**: a human user of the system (role, actor, persona).
- **Software system**: the highest level of abstraction — something that
  delivers value to its users; the thing you are describing or one of its
  neighbors.
- **Container**: a separately runnable/deployable unit that executes code
  or stores data — server app, single-page app, mobile app, database,
  file system, message bus. NOT a Docker container specifically.
- **Component**: a grouping of related functionality inside a container,
  behind a well-defined interface (e.g. a controller + service cluster).
  Components are not separately deployable.
- **Code**: classes/functions — C4 recommends NOT hand-drawing this level;
  generate from tooling if ever needed. Do not offer it.

## The four levels + supplementary views

| # | Diagram | Scope | Elements shown | Primary audience |
|---|---|---|---|---|
| 1 | System Context | One system | The system as one box, people, neighboring systems | Everyone incl. non-technical |
| 2 | Container | Inside one system | Containers + people + external systems | Technical, inside and around the team |
| 3 | Component | Inside one container | Components + the elements they talk to | Developers of that container |
| 4 | Code | Inside one component | Classes etc. — generated, rarely worthwhile | Developers, on demand |

Supplementary:

- **System Landscape**: multiple systems of the organization and their
  relationships — a context diagram zoomed out past one system. Use only
  when the enterprise big picture is requested.
- **Dynamic**: elements collaborating for ONE scenario/use case, with
  numbered interactions. Any abstraction level, but keep it to one.
- **Deployment**: mapping of containers to infrastructure nodes
  (deployment view is typically owned by the architecture document; draw
  it here only when explicitly requested as a diagram).

## Level selection heuristics

- "Who uses it / what does it integrate with?" -> System Context.
- "What is it made of / what would we deploy?" -> Container.
- "How is the API service structured inside?" -> Component (of that one
  container only).
- "What happens when a user checks out?" -> Dynamic.
- "Show all our systems" -> System Landscape.

Component diagrams are optional in C4 practice — create them only where
they add value (complex or risky containers), and expect them to go stale
fastest.

## Notation discipline (review checklist, from c4model.com)

Every diagram:

- Has a title describing diagram type and scope.
- Shows ONE abstraction level; no mixing systems with components.
- Every element has a name AND a short description (the description
  answers "what is this?" without opening another document).
- Containers and components carry a technology label ("React SPA",
  "Kotlin/Spring Boot", "PostgreSQL 16").
- Every relationship is a directed line with a verb phrase ("sends
  invoices to", "reads customer data from") — an unlabeled line forces
  the reader to guess. Add protocol/technology where it matters
  ("JSON/HTTPS", "gRPC", "async via Kafka").
- Acronyms/abbreviations spelled out or well known to the audience.
- A legend exists: shapes, colors, line styles, borders explained —
  notation is free-form in C4, so the legend is what makes it readable.
- Internal vs external elements visually distinct.

## Scoping rules

- One software system per context/container diagram; the system in scope
  is visually emphasized or bounded.
- One container per component diagram.
- Diagrams with more than ~20 elements usually mean the abstraction level
  is wrong or the scope is too wide — split or zoom out.
- Consistency across a set: the same element keeps the same name and
  description at every level.
