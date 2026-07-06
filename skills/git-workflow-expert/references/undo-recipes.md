# Undo and history-hygiene recipes — distilled

Source: Git reference documentation, https://git-scm.com/docs
(git-revert, git-reset, git-restore, git-rebase, git-reflog, gitignore;
Git 2.55.0 docs, verified 2026-07-06). See `SOURCES.md`.

## The one question that picks the recipe

**Has the history been shared?** (pushed to a branch others may have
pulled, including CI systems and forks)

- Shared → add new commits that undo (`git revert`). Never rewrite.
- Private → rewriting is allowed (`git reset`, `git rebase`,
  `git commit --amend`).

## Recipe table

| Situation | Recipe | Destructive? |
|---|---|---|
| Undo a pushed commit | `git revert <sha>` | No — adds an inverse commit |
| Undo a pushed merge commit | `git revert -m 1 <merge-sha>` (mainline = first parent) | No |
| Undo last local commit, keep changes staged | `git reset --soft HEAD~1` | No |
| Undo last local commit, keep changes unstaged | `git reset HEAD~1` (mixed, default) | No |
| Throw away last local commit and its changes | `git reset --hard HEAD~1` | YES — working tree changes gone |
| Unstage a file | `git restore --staged <file>` | No |
| Discard uncommitted edits to a file | `git restore <file>` | YES — edits gone |
| Fix the last local commit's message/content | `git commit --amend` | Rewrites — local only |
| Squash/reword several local commits | `git rebase -i <base>` | Rewrites — local only |
| Recover a "lost" commit or pre-reset state | `git reflog`, then `git branch rescue <sha>` | No |
| Stop tracking a file but keep it on disk | `git rm --cached <file>` + .gitignore entry | No (commit removes it from the index only) |

## Revert details

- `git revert` creates a new commit that inverts a previous commit —
  history stays append-only, so it is always safe on shared branches.
- Revert commits in reverse order when reverting a sequence, or pass a
  range: `git revert <oldest>^..<newest>`.
- For merge commits, `-m 1` declares the first parent (the branch merged
  *into*) as mainline. Note: after reverting a merge, re-merging the same
  branch later brings nothing in — the revert must itself be reverted
  first.

## Reset details (local-only tool)

- `--soft` moves the branch pointer only (changes stay staged).
- `--mixed` (default) also resets the index (changes stay in the working
  tree).
- `--hard` also resets the working tree — the only variant that destroys
  uncommitted work. Before any `--hard`, name the recovery path: committed
  work is recoverable via `git reflog` (~90 days by default);
  *uncommitted* work is not — stash or back up first.

## Rebase safety rules

- Golden rule: never rebase commits that exist outside your own private
  branch. Rewriting shared history forces every other clone to recover.
- Interactive rebase (`git rebase -i`) is for polishing a private branch
  before review/merge: squash fixups, reword messages, drop dead
  experiments, reorder for reviewability.
- After rebasing an already-pushed PR branch that only you work on, push
  with `--force-with-lease` (refuses to clobber unseen remote commits) —
  never bare `--force` — and note the rebase in the PR.
- If a rebase goes wrong mid-flight: `git rebase --abort` returns to the
  pre-rebase state.

## .gitignore discipline

- Ignore: build output, dependency directories, caches, logs, coverage
  reports, local env files (`.env*` with secrets), machine-local tool
  state.
- Do not ignore: lockfiles, source, project-wide editor config the team
  standardizes on.
- Personal editor/OS noise (IDE dirs, `.DS_Store`, `Thumbs.db`) belongs
  in the developer's global ignore file: set once with
  `git config --global core.excludesFile <path>`.
- Order matters within a .gitignore: later patterns override earlier
  ones; `!pattern` re-includes. It is not possible to re-include a file
  if a parent directory of it is excluded.
- Already-tracked files are unaffected by .gitignore. Untrack with
  `git rm --cached <file>`, commit, then the ignore rule applies.

## Secrets in history

If a secret was ever committed:

1. **Rotate the secret immediately** — treat it as compromised. History
   rewriting is cleanup, not containment: clones, forks, CI logs, and
   caches may already hold it.
2. Remove it from the working tree and add an ignore rule for its file.
3. Full history purge (dedicated rewrite tooling) is an organizational
   decision — it rewrites every descendant commit and breaks all clones;
   coordinate before attempting, and only after rotation.
