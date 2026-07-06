# Output eval cases (≥3)

Each case is run twice — WITH the skill installed and WITHOUT (raw
assistant) — and scored against the rubric in
docs/AUTHORING-GUIDE.md §Eval thresholds. The skill must beat raw output.

## Case 1

- Prompt: "Create a container diagram of our system." (run in a repo with
  a frontend, one API service, a worker, a queue, and a database)
- Input artifacts (if any): the repository (docker-compose or deploy
  configs reveal the containers).
- Rubric focus: template compliance, source accuracy.
- Expected qualities: single `C4Container` Mermaid block with title;
  `System_Boundary` around internal containers; technology label on every
  container; verb-phrase + protocol on every `Rel`; italic caption-legend
  under the fence; experimental-syntax note present; no components or
  code-level elements mixed in.

## Case 2

- Prompt: "Give me a context diagram for the order service, and note we
  also integrate with an external tax calculation SaaS."
- Input artifacts (if any): none beyond the prompt.
- Rubric focus: completeness, abstraction discipline.
- Expected qualities: order service as ONE `System` box; tax SaaS as
  `System_Ext`; at least one `Person`; no internal containers leaked into
  the context view; unknown actors asked about or flagged as assumptions
  in Notes rather than invented.

## Case 3

- Prompt: "My wiki's renderer doesn't support Mermaid C4 blocks —
  redraw the container diagram so it still renders."
- Input artifacts (if any): a C4Container diagram from a previous turn.
- Rubric focus: actionability, template compliance.
- Expected qualities: `flowchart TB` fallback with C4 metadata in node
  text (`Name`, `[Container: Technology]`, description), subgraph as the
  system boundary, labeled edges with protocol, `classDef` distinguishing
  external elements, heading carries the title; information content
  matches the original diagram.
