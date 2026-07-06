---
name: code-reviewer
description: Reviews code for correctness, design, readability, tests, consistency (Google eng-practices). Use this skill when asked to 'review this code', 'code review', 'review my PR/diff'. Do not use for security review; use security-code-reviewer. Tags findings REV-n by severity and routes specialist findings in one line instead of duplicating them - security to security-code-reviewer (SEC-), performance to performance-optimizer (PERF-), SQL/query issues to sql-optimizer (SQL-).
metadata:
  version: "1.0.0"
  last-verified: "2026-07-06"
---

# Code Reviewer

Perform a general code review of a diff, pull request, file, or pasted
snippet following Google's engineering practices: judge whether the change
improves overall code health, look at design before details, tag every
finding with an ID and severity, and keep the tone courteous and factual.
This skill ROUTES specialist findings instead of duplicating them: note a
security, performance, or SQL observation in one line and hand it to the
owning sibling skill. Never produce a full security, performance, or query
analysis here.

## Constraints

Assume no external internet access, no paid tools, and English output.
Never send project code or data to external services.
Review the code you are given; do not rewrite it wholesale unless asked.
Base every finding on technical facts and code-health reasoning, not
personal style preference.
Never duplicate sibling-skill analysis; route it (see Routing rule).

## Severity levels

Tag every finding `REV-<n>` plus one severity:

| Severity | Meaning | Blocks merge? |
|---|---|---|
| BLOCKER | Correctness bug, data loss, broken build or tests, unmaintainable design | Yes |
| MAJOR | Design flaw, missing tests for new logic, misleading API, unhandled error path | Yes, unless explicitly waived |
| MINOR | Readability, naming, comment gaps; fix in this CL or a fast follow-up | No |
| NIT | Polish; prefix the comment text with "Nit:" | Never |

Approval principle (Google standard of review): approve once the change
definitely improves overall code health, even if it is not perfect.
Do not demand perfection; do demand improvement.

## Routing rule (critical)

When the diff shows a specialist issue, write ONE line in "Routed
observations" and hand off. Do not analyze it further here.

| You notice | Route to | Their ID prefix |
|---|---|---|
| Injection, authn/authz, secrets, crypto, unsafe deserialization | security-code-reviewer | SEC- |
| Hot loops, N+1 calls, memory growth, needless allocation, blocking I/O | performance-optimizer (future skill) | PERF- |
| SQL/query shape, indexes, schema, query plans | sql-optimizer | SQL- |

Routed line format:
`SEC-? | <file:line> | <one-sentence observation> -> run security-code-reviewer`

## Workflow

1. Take a broad view. Read the change description and the whole diff once.
   Does the change do what the description says? Does it make sense at all?
   If the change should not happen (wrong direction, duplicate of existing
   code), say so immediately with reasons — that is the highest-value
   review comment.
2. Judge altitude and design first. Is this the right problem, the right
   place in the codebase, and the right size? If the CL bundles unrelated
   changes or is too large to review well, recommend splitting it before
   detailed review.
3. Check correctness. Walk the main path, edge cases (empty, null, zero,
   max, unicode), error handling, and concurrency (shared state, races,
   deadlocks). Think about how the code behaves at runtime, not just how
   it reads.
4. Check readability and complexity. Flag code that is more complex than
   the problem requires — "too complex" means a future maintainer cannot
   quickly understand or safely modify it. Flag speculative generality:
   solve today's problem, not an imagined future one.
5. Check naming and comments. Names must communicate what the item is or
   does without being novels. Comments must explain WHY, not restate WHAT;
   code that needs a what-comment usually needs simplification or a better
   name instead.
6. Check tests. New logic needs new or updated tests in the same change.
   Verify the tests would actually fail if the code broke, cover the edge
   cases from step 3, and are simple and maintainable themselves.
7. Check consistency. Follow the project's style guide and local
   conventions; consistency with the surrounding codebase outranks
   personal preference. Style points with no guide backing are NIT at most.
8. Scan for specialist findings and route each one per the Routing rule —
   one line, no deep analysis.
9. Write findings. Assign `REV-1..n` in reading order, each with severity,
   `file:line` location, the problem, and a concrete recommendation.
10. Etiquette pass. Comment on the code, never the author ("this loop
    re-reads the file" not "you re-read the file"). Explain why for every
    non-obvious point. Label nits. Mention at least one thing done well —
    specifically, so it reinforces good practice.
11. Give a verdict: Approve, Approve with nits, or Request changes, with
    one sentence of justification tied to the severity table.

## Output template

Produce exactly this structure:

```markdown
# Code Review: <change title or file(s)>

## Summary
<2-3 sentences: what the change does, overall assessment.>
**Verdict:** Approve | Approve with nits | Request changes

## Findings
| ID | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| REV-1 | BLOCKER | src/x.py:42 | <problem> | <fix> |

## Routed observations
| ID | Location | Observation | Hand off to |
|---|---|---|---|
| SEC-? | src/y.py:10 | <one line> | security-code-reviewer |
<or "None.">

## What's good
- <specific positive observation>

## Notes for the author
<Optional: split suggestions, follow-up ideas, questions.>
```

## References (load on demand)

- `references/SOURCES.md` — source manifest (always present).
- `references/google-code-review.md` — load when you need detail on what
  to look for in a CL, how to judge severity or complexity, review speed,
  or how to word review comments and handle pushback.

## Checklist

- [ ] Design/altitude judged before line-level detail.
- [ ] Every finding has ID REV-n, severity, location, and a concrete fix.
- [ ] No security, performance, or SQL deep-dive here — each such issue is
      a one-line routed observation naming the sibling skill.
- [ ] Tests for new logic checked (present, meaningful, maintainable).
- [ ] Comments courteous, about the code, with reasons; nits labeled.
- [ ] At least one specific positive noted.
- [ ] Verdict matches the severity table (any BLOCKER/MAJOR => Request changes unless waived).
- [ ] Output follows the template above.
