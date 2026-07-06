# Output eval cases (≥3)

Each case is run twice — WITH the skill installed and WITHOUT (raw
assistant) — and scored against the rubric in
docs/AUTHORING-GUIDE.md §Eval thresholds. The skill must beat raw output.

## Case 1

- Prompt: "Write a commit message for this diff: we now send a
  cancellation email when an order is cancelled, and the /orders/cancel
  endpoint no longer accepts the legacy 'silent' flag."
- Input artifacts (if any): short diff summary as above.
- Rubric focus: source accuracy (Conventional Commits v1.0.0 rules),
  template compliance.
- Expected qualities: `feat` type with a scope; breaking change marked
  with `!` AND/OR a `BREAKING CHANGE:` footer naming the removed
  `silent` flag; imperative, lower-case, no-period description ≤72
  chars; body explains why, not a diff narration; output uses the
  "Commit message" + "Rationale" template headings; does not invent a
  version bump (defers SemVer action to release-manager).

## Case 2

- Prompt: "We're a 12-person team, deploy roughly twice a week, CI takes
  8 minutes, and we currently keep a permanent develop branch that's
  always painfully behind main. What branching strategy should we use?"
- Input artifacts (if any): none.
- Rubric focus: completeness (decision criteria), actionability,
  template compliance.
- Expected qualities: recommends trunk-based development with
  short-lived (≤2 day, single-author) feature branches; applies the
  criteria table (team size, cadence, CI speed) rather than fashion;
  names the merge-debt cost of the permanent develop branch; includes a
  concrete working agreement (branch lifetime, merge requirements,
  delete-on-merge, trunk always releasable); "Out of scope" line defers
  release tagging to release-manager and CI design to
  cicd-pipeline-designer.

## Case 3

- Prompt: "A commit with our staging database password is on main,
  pushed 3 days ago, with 14 commits on top of it. Also my colleague
  says I should just 'reset --hard and force-push'. What do we do?"
- Input artifacts (if any): none.
- Rubric focus: source accuracy (revert vs reset on shared history),
  actionability, safety.
- Expected qualities: rejects reset+force-push on a shared branch and
  says why (golden rule of rewriting shared history); rotation of the
  password as the FIRST mandatory step, explicitly stating history
  cleanup is not containment; provides the shared-history recipe
  (revert / remove file + .gitignore + `git rm --cached`); names a
  recovery path for every destructive step; notes that a full history
  purge is an organizational decision requiring coordination; uses the
  Situation / Recipe / Recovery path template.
