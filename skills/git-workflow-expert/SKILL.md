---
name: git-workflow-expert
description: "Guides Git workflow: Conventional Commits, branch strategy, PR hygiene, rebase vs merge, revert vs reset. Use this skill when asked for a commit message, branching strategy, or PR structure. Do not use for release tagging; use release-manager instead. Do not use for CI pipeline design; use cicd-pipeline-designer instead. Covers trunk-based development, .gitignore discipline, and safe undo."
metadata:
  version: "1.0.0"
  last-verified: "2026-07-06"
---

# Git Workflow Expert

Apply disciplined Git working practices: Conventional Commits v1.0.0
messages, a branch strategy chosen by explicit criteria (trunk-based,
short-lived feature branches, or release branches), small reviewable PRs,
clean history (rebase vs merge decided by whether history is shared),
.gitignore discipline, and safe undo (prefer revert on anything pushed).
Recommendations distill conventionalcommits.org, trunkbaseddevelopment.com,
and the official Git documentation (see References).

## Constraints

Assume no external internet access, no paid tools, and English output.
Never send project code or data to external services.
Never rewrite history that others may have pulled (pushed shared branches).
Never run destructive commands (`reset --hard`, `push --force`, `clean -f`)
without naming a recovery path (reflog, backup branch) first.
Technology-agnostic: advise on Git itself, not on a specific host's UI.

## Workflow

1. **Classify the request** as one of: commit message, branch strategy,
   PR preparation, history cleanup, or undo. Handle only what was asked.
2. **Commit messages** — write them in Conventional Commits v1.0.0 form:
   `<type>[optional scope][!]: <description>`, blank line, optional body,
   optional footers. Use `feat` for new behavior, `fix` for bug fixes;
   other common types: `docs`, `refactor`, `test`, `build`, `ci`, `perf`,
   `chore`. Mark breaking changes with `!` after type/scope or a
   `BREAKING CHANGE:` footer. Description: imperative, lower-case start,
   no trailing period. Body explains *why*, not a diff narration. One
   logical change per commit — if the diff needs "and" in the subject,
   split the commit. Load `references/conventional-commits.md` for the
   full rules and worked examples.
3. **Branch strategy** — recommend by criteria, not fashion:
   - Default to **trunk-based development with short-lived feature
     branches** (branch lives hours to ~2 days, one dev, merged after
     review + green CI, then deleted).
   - **Direct-to-trunk** only for very small, high-trust teams with fast
     CI.
   - **Release branches** only when several versions must be supported in
     production or release cadence is decoupled from development; cut
     just-in-time from trunk, fix on trunk first and cherry-pick to the
     release branch, delete when the release is out of support.
   - Long-lived shared development branches (git-flow style `develop`)
     are a last resort; name the merge-debt cost if asked to adopt them.
   Load `references/branching-strategies.md` for the decision table.
4. **PR preparation** — keep PRs small and single-purpose (one concern;
   if the description needs "also", split it). Write the description with:
   what changed, why, how it was tested, and anything reviewers should
   look at first. Self-review the diff before requesting review; remove
   stray debug output, commented-out code, and unrelated formatting churn.
   Ensure the branch is up to date with its target and CI is green before
   requesting review.
5. **History cleanup** — decide rebase vs merge by one question: *has the
   branch been shared?*
   - Private, unpushed (or explicitly single-author WIP) branch: rebase
     onto the target for a linear history; interactive rebase
     (`git rebase -i`) to squash fixups and reword messages is safe here.
   - Shared or pushed branch others may have pulled: never rewrite; merge
     or revert instead.
   - Force-push only your own PR branch after a rebase, prefer
     `--force-with-lease`, and say so in the PR.
6. **.gitignore discipline** — ignore generated artifacts (build output,
   dependency dirs, caches, logs), local environment files, and secrets;
   never ignore lockfiles or source. Editor/OS noise belongs in the
   user's global ignore file (`core.excludesFile`), not every repo. If a
   file is already tracked, adding it to .gitignore does nothing — untrack
   with `git rm --cached <file>` first. Never commit secrets; if one
   lands in history, rotating the secret is mandatory (history rewriting
   alone is not containment).
7. **Undo** — choose the recipe by whether the commit is shared:
   - Shared history: `git revert <commit>` (new inverse commit; safe).
   - Local only: `git reset` (`--soft` keep staged, `--mixed` keep in
     working tree, `--hard` discard — destructive).
   - Single files, uncommitted: `git restore <file>` /
     `git restore --staged <file>`.
   - Lost work: `git reflog` finds recent HEADs for ~90 days.
   Load `references/undo-recipes.md` for the full recipe table.
8. **Deliver the output** in the matching template below. Flag — but do
   not perform — anything owned by a sibling skill: version bumps,
   CHANGELOG, and tags belong to `release-manager`; pipeline/workflow
   design belongs to `cicd-pipeline-designer`.

## Output template

Use the section matching the request; keep headings exactly.

For a commit message:

```markdown
## Commit message
<type>(<scope>): <description>

<body — why the change was made>

<footer(s), e.g. BREAKING CHANGE: ..., Refs: #123>

## Rationale
- Type chosen because ...
- Breaking-change marker: yes/no because ...
```

For a branch strategy recommendation:

```markdown
## Recommendation
<strategy name, one sentence>

## Criteria applied
| Criterion | Your situation | Points to |
|---|---|---|

## Working agreement
- Branch lifetime limit: ...
- Merge requirements: ...
- Release handling: ...

## Out of scope
Version numbering/tagging -> release-manager. CI design -> cicd-pipeline-designer.
```

For history cleanup / undo:

```markdown
## Situation
Shared history: yes/no. Target state: ...

## Recipe
1. <exact commands, one per line>

## Recovery path
<how to get back if this goes wrong — reflog/backup branch>
```

## References (load on demand)

- `references/SOURCES.md` — source manifest (always present).
- `references/conventional-commits.md` — load when writing or reviewing
  commit messages; full v1.0.0 rules, types, breaking changes, examples.
- `references/branching-strategies.md` — load when choosing or defending
  a branch strategy or PR working agreement; decision criteria table.
- `references/undo-recipes.md` — load when undoing, rewriting, or
  recovering history; revert/reset/restore/reflog recipes.

## Checklist

- [ ] Commit messages follow Conventional Commits v1.0.0 (type, optional
      scope, imperative description; breaking changes marked).
- [ ] Branch strategy recommendation cites the criteria that drove it.
- [ ] No history rewrite advised on shared/pushed branches.
- [ ] Every destructive command comes with a named recovery path.
- [ ] Secrets handling: rotation advised, never just history rewriting.
- [ ] Release tagging/CHANGELOG deferred to release-manager; CI design
      deferred to cicd-pipeline-designer.
- [ ] Output follows the matching template above.
