# SOURCES.md — source manifest

Every normative claim in this skill traces to a source below. Never rely on
model memory alone (risk R6).

| Standard / source | Exact version | Official URL | Last verified | Offline fallback |
|---|---|---|---|---|
| Agent Skills specification (SKILL.md format: name ≤64 lowercase-hyphen no leading/trailing/consecutive hyphens, must match folder; description 1–1024 chars; optional license/compatibility/metadata/allowed-tools; body <500 lines recommended; references one level deep) | current (unversioned page) | https://agentskills.io/specification | 2026-07-06 | limits distilled in references/authoring-checklist.md; enforced by tools/validate_skills.py |
| Fable Skills authoring standards (folder contract, description formula, first-250-chars rule, 500-char library cap, voice split, depth model, script rules, security gate, shared constraints, eval thresholds, definition of done) | repo HEAD | docs/AUTHORING-GUIDE.md (repo-internal path, no URL) | 2026-07-06 | the guide lives in this repo; skill runs only on the build machine |
| Harness support matrix (frontmatter field support, discovery paths, listing limits) | repo HEAD | docs/COMPATIBILITY.md (repo-internal path, no URL) | 2026-07-06 | lives in this repo |
| Per-harness install steps and table | repo HEAD | docs/PER-HARNESS-SETUP.md (repo-internal path, no URL) | 2026-07-06 | lives in this repo |
| Library CI validator behavior (PASS/FAIL rules, 500-char and 500-line caps, staleness warning) | repo HEAD | tools/validate_skills.py (repo-internal path, no URL) | 2026-07-06 | lives in this repo |
