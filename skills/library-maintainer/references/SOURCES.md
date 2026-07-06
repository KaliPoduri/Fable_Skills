# SOURCES.md — source manifest

Every normative claim in this skill traces to a source below. Never rely on
model memory alone (risk R6).

| Standard / source | Exact version | Official URL | Last verified | Offline fallback |
|---|---|---|---|---|
| Agent Skills specification (validation target: name/description/frontmatter rules the library must keep passing) | current (unversioned page) | https://agentskills.io/specification | 2026-07-06 | rules distilled in references/maintenance-runbook.md; enforced by tools/validate_skills.py |
| Semantic Versioning (MAJOR.MINOR.PATCH triage for metadata.version bumps) | 2.0.0 | https://semver.org/spec/v2.0.0.html | 2026-07-06 | triage table distilled in references/maintenance-runbook.md |
| Keep a Changelog (CHANGELOG.md categories: Added/Changed/Deprecated/Removed/Fixed/Security under [Unreleased]) | 1.1.0 | https://keepachangelog.com/en/1.1.0/ | 2026-07-06 | category list distilled in references/maintenance-runbook.md; live format visible in repo CHANGELOG.md |
| Fable Skills authoring standards (rules every maintained skill must still satisfy after edits; 90-day staleness aid) | repo HEAD | docs/AUTHORING-GUIDE.md (repo-internal path, no URL) | 2026-07-06 | lives in this repo |
| Verification governance record (one row per re-verification EVENT; table format; still-unverified list) | repo HEAD | VERIFICATION-LOG.md (repo-internal path, no URL) | 2026-07-06 | lives in this repo |
| Per-harness install master table (Job 6 drift target) | repo HEAD | docs/PER-HARNESS-SETUP.md (repo-internal path, no URL) | 2026-07-06 | lives in this repo |
| Library CI validator (staleness warning at 90 days; PASS/FAIL semantics) | repo HEAD | tools/validate_skills.py (repo-internal path, no URL) | 2026-07-06 | lives in this repo |
