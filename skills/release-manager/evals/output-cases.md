# Output eval cases (≥3)

Each case is run twice — WITH the skill installed and WITHOUT (raw
assistant) — and scored against the rubric in
docs/AUTHORING-GUIDE.md §Eval thresholds. The skill must beat raw output.

## Case 1

- Prompt: "Cut a release. Since v1.4.2 we merged: a fix for the retry
  loop, a new `--json` output flag, and we renamed the `timeout` config
  key to `request_timeout`."
- Input artifacts (if any): git log excerpt with the three changes; an
  existing CHANGELOG.md with an Unreleased section.
- Rubric focus: source accuracy (SemVer classification), template
  compliance.
- Expected qualities: version decision 1.4.2 → 2.0.0 (config key rename
  is breaking; highest bucket wins — not 1.5.0); changelog section in
  Keep a Changelog 1.1.0 format with Changed/Added/Fixed groups, dated
  YYYY-MM-DD, Unreleased kept at top, link refs updated; release notes
  include a migration step for the renamed key; annotated tag command;
  publish steps gated on user confirmation.

## Case 2

- Prompt: "What version should this be? We're at 0.8.3 and we completely
  reworked the plugin API."
- Input artifacts (if any): none.
- Rubric focus: source accuracy (0.y.z rules), actionability.
- Expected qualities: states that at major version zero anything may
  change and SemVer makes no stability promise; applies the stated
  0.y.z convention (breaking → 0.9.0) rather than jumping to 1.0.0 or
  incorrectly forcing a MAJOR bump; raises the question of declaring
  1.0.0 if the API is now stable and production-used; asks for or
  identifies the declared public API surface.

## Case 3

- Prompt: "Write the changelog and release notes from this git log."
  (log contains ~30 commits: merge commits, 'wip', 'fix typo', two real
  features, one security fix)
- Input artifacts (if any): raw `git log --oneline` dump.
- Rubric focus: completeness, actionability (for-humans principle).
- Expected qualities: does NOT transcribe the git log; filters noise
  (wip/typo/merge commits) into nothing or a single internal note;
  writes impact-phrased entries; security fix appears under a Security
  heading and in the notes' highlights; six-category grouping with only
  non-empty categories present; notes separate narrative summary from
  the grouped list.
