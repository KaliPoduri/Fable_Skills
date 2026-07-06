# Keep a Changelog 1.1.0 — distilled format

Source: https://keepachangelog.com/en/1.1.0/ (verified 2026-07-06).

## Guiding principles

- Changelogs are for humans, not machines.
- There is an entry for every single version.
- The same types of changes are grouped.
- Versions and sections are linkable.
- The latest version comes first (reverse chronological).
- The release date of each version is displayed (YYYY-MM-DD).
- State whether the project follows Semantic Versioning.

## The six categories

| Category | Use for |
|---|---|
| Added | New features |
| Changed | Changes in existing functionality |
| Deprecated | Soon-to-be-removed features |
| Removed | Now-removed features |
| Fixed | Any bug fixes |
| Security | Vulnerability fixes (call these out — users scan for them) |

Only include categories that have entries; keep the order above.

## The Unreleased section

Keep an `## [Unreleased]` section at the top, always:

- Users see what is coming in the next release.
- At release time, move its content into the new version section and
  leave `Unreleased` empty — the release edit becomes trivial.

## File skeleton

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.0] - 2026-07-06

### Added

- Config file support: read defaults from `.toolrc` before CLI flags.

### Fixed

- Crash when the input directory contained symlinked files.

## [1.0.0] - 2026-05-02

### Added

- Initial stable release.

[unreleased]: https://example.com/repo/compare/v1.1.0...HEAD
[1.1.0]: https://example.com/repo/compare/v1.0.0...v1.1.0
[1.0.0]: https://example.com/repo/releases/tag/v1.0.0
```

## Entry style

- Write impact for a reader, not commit subjects: "Uploads over 2 GB no
  longer time out" beats "fix timeout in uploader.py".
- One entry per notable change; link issues/PRs where the project does.
- Yanked releases: mark the heading `## [0.0.5] - 2014-12-13 [YANKED]`
  so pulled versions stay visible with the warning.
- Never rewrite history silently: if an old section needs correcting,
  add the correction and make it clear it is a correction.

## Anti-patterns to reject

- Dumping `git log` output as the changelog — commit noise, merge
  commits, and internal refactors bury what users care about. Commit
  diffs and changelogs serve different readers.
- Ignoring deprecations — users must be able to see what to migrate off
  BEFORE the removal lands in a MAJOR release.
- Regional or ambiguous dates (e.g., 06/07/2026) — use YYYY-MM-DD.
- Skipping versions or leaving undated releases.
