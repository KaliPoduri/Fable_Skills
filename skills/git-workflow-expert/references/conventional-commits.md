# Conventional Commits v1.0.0 — distilled

Source: Conventional Commits specification v1.0.0,
https://www.conventionalcommits.org/en/v1.0.0/ (verified 2026-07-06).
See `SOURCES.md`.

## Structure

```
<type>[optional scope][!]: <description>

[optional body]

[optional footer(s)]
```

## Rules (normative, from the v1.0.0 spec)

1. Every commit MUST be prefixed with a type (a noun: `feat`, `fix`, …)
   followed by an optional scope, optional `!`, and a required colon and
   space.
2. `feat` MUST be used when the commit adds a new feature.
3. `fix` MUST be used when the commit patches a bug.
4. A scope MAY follow the type: a noun in parentheses describing the
   affected area, e.g. `feat(parser): ...`.
5. The description MUST immediately follow the colon and space — a short
   summary of the change.
6. A longer body MAY follow, beginning one blank line after the
   description; it is free-form and may span paragraphs.
7. Footers MAY follow one blank line after the body. Each footer is a
   token, then `: ` or ` #`, then a value (git-trailer style). Footer
   tokens use `-` instead of spaces (e.g. `Reviewed-by`), with
   `BREAKING CHANGE` as the only exception.
8. Breaking changes MUST be indicated either by `!` immediately before
   the colon (`feat(api)!: ...`) or by a `BREAKING CHANGE: <description>`
   footer (or both).
9. `BREAKING-CHANGE` is synonymous with `BREAKING CHANGE` in footers, and
   `BREAKING CHANGE` MUST be uppercase.
10. Types other than `feat` and `fix` MAY be used. Common convention
    (from the Angular convention, referenced by the spec): `build`,
    `chore`, `ci`, `docs`, `style`, `refactor`, `perf`, `test`.
11. Units of information (type, scope, description…) MUST NOT be treated
    as case sensitive by tooling, except `BREAKING CHANGE`.
12. If a commit conforms to multiple types, prefer making multiple
    commits — one logical change per commit.

## SemVer correlation

- `fix:` → PATCH release.
- `feat:` → MINOR release.
- Any commit with a breaking-change marker (`!` or `BREAKING CHANGE:`)
  → MAJOR release, regardless of type.

(Acting on this — bumping versions, writing CHANGELOG, tagging — is
release-manager's job; this skill only formats the commits that feed it.)

## House style for the description line

Beyond the spec, apply these widely used conventions:

- Imperative mood ("add", not "added"/"adds") — matches Git's own
  generated messages.
- Lower-case first word after the colon; no trailing period.
- Aim ≤72 characters for the whole subject line; never let tooling wrap it.
- Body explains *why* and any non-obvious consequence; do not narrate the
  diff.
- Reference issues in footers (`Refs: #123`, `Fixes: #123`), not in the
  subject.

## Worked examples

Minimal:

```
docs: correct spelling of CHANGELOG
```

With scope:

```
feat(lang): add Polish language
```

Breaking change via `!` and footer, with body:

```
feat(api)!: send an email to the customer when a product is shipped

Shipping notifications were previously the storefront's job. Moving them
server-side guarantees delivery even when the storefront is down.

BREAKING CHANGE: `notify` flag removed from the /ship endpoint; emails
are always sent.
Refs: #482
```

Revert (spec recommendation — `revert` type with a footer naming the
undone commits):

```
revert: let us never again speak of the noodle incident

Refs: 676104e, a215868
```

## Anti-patterns to reject

- `fix: fixed the bug` — no information; describe the behavior fixed.
- `feat: update code` / `chore: changes` — vague type-plus-noise.
- `feat: add login and fix session timeout and update docs` — three
  commits pretending to be one; split it.
- Breaking behavior change with no `!`/`BREAKING CHANGE` marker — silently
  breaks consumers relying on SemVer automation.
- Type `chore` for everything — erodes the SemVer signal; pick the true
  type.
