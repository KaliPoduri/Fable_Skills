# Google code review practices — distilled

Source: Google Engineering Practices Documentation, "The Code Reviewer's
Guide" (https://google.github.io/eng-practices/review/reviewer/), living
document, retrieved 2026-07-06. Google-internal terms: CL = changelist
(one self-contained change under review); LGTM = "Looks Good to Me"
(approval). Distilled for offline use — do not fetch the URL at runtime.

## The standard of code review

- The senior principle: **reviewers should approve a CL once it definitely
  improves the overall code health of the system, even if the CL isn't
  perfect.** There is no perfect code, only better code.
- Do not block on polish. Balance forward progress against the importance
  of each suggestion. Continuous small improvement beats stalled perfection.
- Reviewers own the code they approve: it must stay healthy enough that
  the codebase does not degrade over time.
- Technical facts and data overrule opinions and personal preferences.
- On style: the style guide is absolute authority where it speaks; where it
  is silent, consistency with existing local code wins; pure personal
  preference is at most a nit.
- If no other rule applies and the code is acceptable either way, accept
  the author's approach.

## What to look for in a CL

1. **Design** — the most important thing. Do the interactions of the
   pieces make sense? Does the change belong in this codebase, in this
   place, integrated cleanly? Is now the right time to add it?
2. **Functionality** — does it do what the author intended, and is that
   good for users (end users and future developers)? Think about edge
   cases, concurrency problems, races, deadlocks. Actually run or reason
   through the code, especially UI-facing and parallel code.
3. **Complexity** — is the CL more complex than it needs to be? "Too
   complex" = cannot be understood quickly by code readers, or developers
   are likely to introduce bugs when modifying it. Watch for
   over-engineering: solving a speculative future problem instead of the
   present one. Solve the problem that needs solving now.
4. **Tests** — ask for unit/integration/e2e tests appropriate to the
   change, in the same CL. Tests must actually fail when the code breaks,
   avoid false positives, and be simple and useful — tests do not test
   themselves, so avoid complexity in them.
5. **Naming** — good names are long enough to fully communicate what the
   item is or does, without being so long they are hard to read.
6. **Comments** — clear, in understandable English. Necessary comments
   explain WHY code exists, not what it does; code that needs a
   what-explanation should usually be simplified instead. (Exceptions:
   regexes, complex algorithms.) Distinguish comments from documentation.
7. **Style** — follow the project style guide. Style points not in the
   guide are personal preference: prefix with "Nit:" or let them go. Do
   not mix major style refactors into a functional CL.
8. **Consistency** — style guide > local consistency > personal taste.
   If existing code conflicts with the guide, new code follows the guide;
   file a cleanup task rather than expanding the inconsistency.
9. **Documentation** — if the CL changes how users build, test, interact
   with, or release code, check that READMEs, generated docs, etc. are
   updated; deleted code should have its docs deleted too.

Look at **every line** you are assigned to review (generated code and
large data files excepted). If you cannot understand a line, ask — code
that a reviewer cannot understand will also be opaque to future
maintainers.

**Context**: look at the CL in the whole-file and whole-system view. Is
the surrounding function/class still sensible? Does this CL improve code
health, or does it add complexity/tech-debt the system should not absorb?

**Good things**: tell the author what they did well, specifically. Reviews
that only correct mistakes waste mentoring opportunity.

## Navigating a CL in review

1. Read the CL description first: does the change make sense at all? If
   the change should not happen, respond immediately with why, and suggest
   what the author should do instead (politely).
2. Look at the most important/central part first — usually the file with
   the largest logical change. It gives context to the rest and surfaces
   major design problems early. Send major design comments immediately,
   even before finishing the rest of the review.
3. Then review the remaining files in a logical sequence (tests alongside
   the code they test).

## Speed of review

- One business day is the maximum turnaround; team velocity suffers more
  from slow reviews than individual velocity gains from batching.
- Fast response matters more than fast completion of the whole review.
- Do not interrupt deep-focus work to review; pick it up at the next
  natural break point.
- Large CLs: if too large to review promptly, ask the author to split it.
- LGTM with comments: approve while leaving unresolved comments only when
  you trust the author to address them, or the remainder is minor.

## How to write review comments

- **Courtesy**: comment on the CODE, never the developer. Not "Why did
  you use threads here?" but "The concurrency model here adds complexity
  without a visible performance benefit — is a single-threaded approach
  simpler?"
- **Explain why**: give reasons and the code-health principle behind each
  suggestion, not bare directives.
- **Label severity**: mark what is mandatory vs optional, e.g. "Nit:",
  "Optional/Consider:", "FYI:". Otherwise authors assume everything blocks.
- **Guidance balance**: point out the problem and let the author decide
  the fix (builds ownership); give an explicit suggestion when it teaches
  or saves obvious time. Do not write the whole solution for them unless
  asked.
- **Accept explanations, in code**: if a reviewer had to ask what the code
  does, the answer belongs in the code (rename, restructure, comment) —
  an explanation written only in the review tool helps no future reader.

## Handling pushback

- First consider whether the author is right — they are often closer to
  the code. If so, say so and move on.
- If not, explain further: restate the code-health reason with additional
  facts. Keep every round of the discussion polite.
- "I'll clean it up later" rarely happens; require the cleanup in this CL
  or an immediately-filed, actually-scheduled follow-up before approval.
- Escalate stalemates to a face-to-face conversation or a third opinion
  rather than fighting in comments.
- Do not let a CL degrade code health "just this once" — the sum of such
  exceptions is how codebases rot.
