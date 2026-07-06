---
name: release-manager
description: "Runs releases: SemVer versioning, Keep a Changelog changelogs, git tags, release notes, hotfix path. Use this skill when asked to cut a release, pick a version, or write a changelog. Do not use for CI/CD pipeline design; use cicd-pipeline-designer. Not for commit messages or branching; use git-workflow-expert. Includes the release-cut checklist."
metadata:
  version: "1.0.0"
  last-verified: "2026-07-06"
---

# Release Manager

Run the release process for the project at hand: decide the next version
number with Semantic Versioning 2.0.0, update the changelog per Keep a
Changelog 1.1.0, tag the release in git, write release notes for humans,
and walk the release-cut checklist (freeze, verify, tag, publish,
announce). Also handle the hotfix path when production needs a fix that
cannot wait for the next planned release.

## Constraints

Assume no external internet access, no paid tools, and English output.
Never send project code or data to external services.
Never push tags, publish packages, or create platform releases without
explicit user confirmation — prepare commands and content, then ask.
Version decisions apply SemVer 2.0.0 only if the project declares a
public API; for 0.y.z projects state explicitly that anything may change.
Pipeline design belongs to cicd-pipeline-designer; commit message and
branching conventions belong to git-workflow-expert.

## Workflow

1. **Establish release context.** Find the current version (latest git
   tag, package manifest, CHANGELOG). Collect changes since the last
   release: `git log <last-tag>..HEAD --oneline` plus the CHANGELOG
   `Unreleased` section if one exists. Identify the project's public API
   surface (exported functions, CLI flags, HTTP endpoints, config
   schema) — SemVer is meaningless without one declared.
2. **Classify every change.** Bucket each change as: breaking (public
   API incompatible), feature (backward-compatible functionality),
   fix (backward-compatible bug fix), or internal (no user-visible
   effect). When unsure whether a change is breaking, load
   `references/semver-rules.md` and check the edge-case table.
3. **Decide the version.** Highest bucket wins: breaking → MAJOR,
   feature → MINOR, fix-only → PATCH. For pre-1.0.0 projects or
   pre-releases (`-alpha.1`, `-rc.1`), follow the pre-release rules in
   `references/semver-rules.md`. State the decision as one line:
   `<old> → <new> because <highest-impact change>`.
4. **Update the changelog.** Follow Keep a Changelog 1.1.0: move
   `Unreleased` content into a new `## [<version>] - <YYYY-MM-DD>`
   section; group entries under Added / Changed / Deprecated / Removed /
   Fixed / Security; keep an empty `Unreleased` section at top; update
   the link references at the bottom. Load
   `references/changelog-format.md` for the exact file skeleton and
   entry style. Write entries for humans — impact, not commit subjects.
5. **Write the release notes.** Separate artifact from the changelog:
   short narrative summary (what this release means for users),
   highlights, breaking changes with migration steps, then the full
   change list (may link/copy the changelog section). Use the output
   template below.
6. **Walk the release-cut checklist.**
   - Freeze: no new features onto the release ref; agree what may still
     land (critical fixes only).
   - Verify: full pipeline green on the exact release commit; changelog
     and manifest version updated and committed.
   - Tag: annotated tag `v<version>` on that commit —
     `git tag -a v<version> -m "<one-line summary>"` (annotated, not
     lightweight, so the tag carries author/date/message).
   - Publish: push the tag, publish the package/artifact, create the
     platform release with the release notes — each only after user
     confirmation.
   - Announce: post the release notes to the team channel/tracker;
     close the release milestone.
7. **Hotfix path (when asked to fix production now).** Branch from the
   production tag (`git checkout -b hotfix/<issue> v<current>`), apply
   the minimal fix, PATCH-bump, run the same verify-tag-publish steps in
   compressed form, then merge/cherry-pick the fix back to the main line
   so the next release contains it. Never hotfix from an unreleased
   main branch state.
8. **Hand off boundaries.** If the conversation turns to pipeline stages
   or gates, point to cicd-pipeline-designer; for commit message or
   branch naming conventions, git-workflow-expert.

## Output template

For a release cut, deliver these three artifacts in order:

```markdown
## Version decision
<old> → <new>
Reasoning: <highest-impact change and its SemVer bucket; note if 0.y.z
or pre-release rules applied>

## CHANGELOG update
<the exact new/modified sections of CHANGELOG.md, in Keep a Changelog
1.1.0 format, ready to paste>

## Release notes — v<version> (<date>)
### Summary
<2-4 sentences: what this release means for users>
### Highlights
- <top items, user-facing wording>
### Breaking changes and migration
- <each breaking change with the concrete migration step, or "None">
### Full changes
<grouped list or pointer to the changelog section>

## Release-cut checklist
- [ ] Freeze declared (scope: <what may still land>)
- [ ] Pipeline green on release commit <sha>
- [ ] CHANGELOG.md and version manifest updated, committed
- [ ] Annotated tag v<version> created
- [ ] Tag pushed / package published / platform release created (after
      user confirmation)
- [ ] Announcement posted, milestone closed
```

For a version-decision-only request, deliver just the Version decision
block. For changelog/notes-only requests, deliver those blocks.

## References (load on demand)

- `references/SOURCES.md` — source manifest (always present).
- `references/semver-rules.md` — load when classifying changes or
  deciding the version (steps 2–3), especially for pre-releases,
  0.y.z projects, build metadata, or precedence questions.
- `references/changelog-format.md` — load when creating or updating
  CHANGELOG.md (step 4) for the file skeleton, categories, and link
  reference style.

## Checklist

- [ ] Version decision names the single highest-impact change and its
      SemVer bucket; 0.y.z / pre-release caveats stated when they apply.
- [ ] Changelog entries grouped under the six Keep a Changelog
      categories, newest version first, dated YYYY-MM-DD, `Unreleased`
      section retained at top.
- [ ] Entries written for humans (impact), not raw commit subjects.
- [ ] Release notes include breaking changes with migration steps, or
      state "None".
- [ ] Tag command uses an annotated tag `v<version>` on the verified
      release commit.
- [ ] No push/publish step executed without explicit user confirmation.
- [ ] Hotfix (if any) branched from the production tag and merged back
      to the main line.
- [ ] Output follows the template above.
