# Semantic Versioning 2.0.0 — distilled rules

Source: https://semver.org/ (SemVer 2.0.0, verified 2026-07-06).

## Format

`MAJOR.MINOR.PATCH` (X.Y.Z), non-negative integers, no leading zeros.
Optional suffixes: `-<pre-release>` and `+<build-metadata>`.

## Increment rules

| Bump | When | Resets |
|---|---|---|
| MAJOR | Any backward-incompatible change to the public API | MINOR and PATCH to 0 |
| MINOR | Backward-compatible new functionality; also for deprecating public API functionality | PATCH to 0 |
| PATCH | Backward-compatible bug fixes only | — |

Preconditions:

- The project MUST declare a public API (code docs or the API surface
  itself). Without one, SemVer bumps are arbitrary — get the API surface
  stated first.
- Released versions are immutable: never re-tag or modify a released
  version; any change is a new version.

## 0.y.z (initial development)

- Major version zero means anything MAY change at any time; the public
  API is not stable and consumers get no compatibility promise.
- 1.0.0 is the declaration that the public API is stable and in
  production use. When users depend on it in production, it should be
  1.0.0 already.
- Practical convention for 0.y.z (state it when used): breaking →
  bump y, everything else → bump z.

## Pre-release versions

- Append `-` plus dot-separated identifiers: `1.0.0-alpha`,
  `1.0.0-alpha.1`, `1.0.0-rc.2`. Identifiers: alphanumerics and
  hyphens; numeric identifiers without leading zeros.
- A pre-release has LOWER precedence than the normal version:
  `1.0.0-rc.1 < 1.0.0`.
- Pre-releases signal instability; dependency tooling typically will not
  auto-select them.

## Build metadata

- Append `+` plus identifiers: `1.0.0+20130313144700`,
  `1.4.2+sha.5114f85`.
- Build metadata MUST be ignored for precedence — `1.0.0+a` and
  `1.0.0+b` are the same version for ordering. Use it to embed commit
  SHAs or build ids without affecting version comparison.

## Precedence (ordering)

1. Compare MAJOR, then MINOR, then PATCH numerically.
2. A pre-release version < its normal version (`1.0.0-alpha < 1.0.0`).
3. Between pre-releases: compare identifiers left to right — numeric
   identifiers compare numerically, alphanumeric ones lexically
   (ASCII); numeric < alphanumeric; more fields > fewer when all
   preceding fields are equal.
   Canonical chain: `1.0.0-alpha < 1.0.0-alpha.1 < 1.0.0-alpha.beta <
   1.0.0-beta < 1.0.0-beta.2 < 1.0.0-beta.11 < 1.0.0-rc.1 < 1.0.0`.

## Edge-case classification table

| Change | Bucket |
|---|---|
| Removing/renaming any public function, endpoint, CLI flag, config key | Breaking → MAJOR |
| Tightening accepted input (rejecting what was accepted) | Breaking → MAJOR |
| Changing a default that alters observable behavior | Breaking → MAJOR (usually) |
| Raising the minimum supported runtime/platform | Breaking → MAJOR (treat as such unless project policy says otherwise — state the policy) |
| Adding a new endpoint/function/optional parameter | Feature → MINOR |
| Deprecating (still working) public functionality | MINOR (SemVer: deprecations MUST bump at least MINOR) |
| Substantial internal rework with identical public behavior | MINOR permitted; PATCH if purely fix-motivated |
| Fixing behavior to match documented contract | PATCH (even if someone depended on the bug — note it in release notes) |
| Fixing a security vulnerability without API change | PATCH (+ Security changelog entry) |
| Docs, tests, build tooling only | No release required; rides along with the next one |

When a "fix" changes behavior that the documentation also promised
(i.e., docs and code disagreed), decide which was the contract, say so
in the release notes, and bump accordingly — silent contract flips are
how trust in version numbers dies.
