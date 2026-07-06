---
name: skill-name-here
description: <Third-person what-it-does, one sentence.> Use this skill when <triggers with keywords>. Do not use for <negative boundary — name the sibling skill that owns that case>. <Keywords + negative boundary MUST fit in the first 250 chars; total ≤500 chars (library policy).>
metadata:
  version: "0.1.0"
  last-verified: "YYYY-MM-DD"
---

# <Skill Title>

<One-paragraph purpose. Imperative voice throughout the body ("Do X", not
"The agent does X"). Keep the whole body under 500 lines.>

## Constraints

Assume no external internet access, no paid tools, and English output.
Never send project code or data to external services.
<Plus any skill-specific constraints — one line each.>

## Workflow

1. <Step — bite-sized, verifiable.>
2. <Step.>
3. <Step.>

## Output template

<Exact structure the deliverable must follow — headings, tables, format.>

## References (load on demand)

- `references/SOURCES.md` — source manifest (always present).
- `references/<topic>.md` — load when <condition>.

## Checklist

- [ ] <Verification item the agent must confirm before finishing.>
- [ ] Output follows the template above.
