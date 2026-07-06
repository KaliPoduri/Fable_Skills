# INVEST — story quality criteria

Distilled from: Bill Wake, "INVEST in Good Stories, and SMART Tasks",
XP123, 2003-08-17 (postscript 2011-02-16),
https://xp123.com/invest-in-good-stories-and-smart-tasks/ (verified
2026-07-06). One-Sprint readiness rule from the Scrum Guide, November
2020, https://scrumguides.org/scrum-guide.html (verified 2026-07-06).

INVEST is Wake's acronym for the characteristics of a good user story:
Independent, Negotiable, Valuable, Estimable, Small, Testable. Use it as a
diagnostic: a failed letter points to a specific fix, usually rewording,
splitting, or getting missing information.

## The six criteria

### I — Independent

The story can be scheduled and delivered in any order relative to other
stories; it does not overlap other stories in content.
- Smells: "part 2 of...", criteria that only make sense after another
  story ships, two stories editing the same behavior.
- Fixes: merge overlapping stories and re-split along a different
  dimension; move shared setup into the earlier story; state the one real
  dependency explicitly instead of a chain.

### N — Negotiable

A story is not a contract; it is an invitation to a conversation. Detail
is co-created with the team, not fixed upfront.
- Smells: story text prescribing UI widgets, database columns, or
  APIs; acceptance criteria enumerating every pixel.
- Fixes: restate the goal in terms of user-observable outcome; move
  implementation ideas to a note labeled as ideas, not requirements.

### V — Valuable

The story delivers visible value to a customer or user (or a paying
stakeholder). A story that is only "technically necessary" hides its value.
- Smells: horizontal layer stories ("build the DAO layer"), pure refactor
  stories with no observable effect.
- Fixes: re-slice vertically so each piece crosses the stack and shows a
  user-visible result; if value is risk-reduction, say whose risk and why
  they care.

### E — Estimable

The team can size the story well enough to plan it. (Per the Scrum Guide,
the Developers who will do the work are the ones who size it.)
- Smells: nobody can say if it is a day or a month; unknown technology;
  unresolved domain question.
- Fixes: for missing knowledge, split out a timeboxed spike; for missing
  domain answers, record the open question and park the story; for
  too-big stories, split (see epic-story-breakdown).

### S — Small

Fits comfortably within one iteration. Practical Scrum bar: the story
"can be Done by the Scrum Team within one Sprint" — smaller is better;
a few days is a common target near the top of the backlog.
- Smells: compound goals joined by "and", "manage X" verbs, criteria
  lists longer than ~5 scenarios.
- Fixes: split by workflow step, path, data, rules, or CRUD — hand the
  split itself to epic-story-breakdown when it produces multiple stories.
- Kanban: replace "one Sprint" with "flows within the team's target cycle
  time".

### T — Testable

You can tell, objectively, whether the story is done. If you cannot write
the test, you do not understand the story yet.
- Smells: adverbs ("fast", "easy", "intuitive"), no failure paths, hidden
  quality bars.
- Fixes: turn each criterion into a Gherkin scenario with an observable
  Then; give non-functional needs a measurable threshold ("results within
  2 seconds for 95% of searches").

## Running the check

1. Evaluate all six letters, in order, against the drafted narrative and
   criteria. Never skip letters that look obviously fine — record PASS.
2. For each concern, write ONE line naming the smell and ONE concrete fix.
3. Severity guide: Small or Testable failures usually block readiness;
   Independent and Estimable concerns are warnings to raise in
   refinement; Negotiable and Valuable failures mean the story is
   mis-framed — reword before polishing criteria.

## Ready check (sanity, not a formal gate)

The Scrum Guide 2020 defines no "Definition of Ready"; its bar is that
items the team can get Done within one Sprint are ready for selection.
The skill's Ready check is therefore a courtesy sanity list: narrative and
criteria complete, Sprint-sized, dependencies known, testable as written.
Do not present it as an official Scrum artifact.
