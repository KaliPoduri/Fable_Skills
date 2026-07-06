# Branch strategy selection — distilled

Sources: Trunk Based Development site by Paul Hammant,
https://trunkbaseddevelopment.com/ (living site, fetched 2026-07-06);
branching/merging semantics from Git documentation, git-scm.com/docs
(Git 2.55.0 docs). See `SOURCES.md`.

## The strategies

### Trunk-based development (TBD)

One shared branch ("trunk", typically `main`). Developers integrate at
least daily. No long-lived development branches, which prevents large
merge conflicts and integration surprises. Two variants:

- **Committing straight to trunk** — very small teams (roughly 2–5
  experienced devs), each commit is small, tested, and releasable.
- **Short-lived feature branches for review** — the scaled variant: a
  branch is created from trunk by one developer, lives hours to about two
  days at most, gets code review and green CI, merges to trunk, and is
  deleted. "Short-lived" is the load-bearing property; a two-week
  "feature branch" is not TBD.

Prerequisites: fast CI on every merge, small slices of work, and a way to
hide unfinished work in released code (feature flags or dark launches,
keystone-last ordering).

### Release branches (optional add-on to TBD)

Cut just-in-time from trunk when stabilizing a release. Harden, ship,
then delete (or keep only while that version is supported). Cardinal
rule: fix bugs on trunk first and cherry-pick to the release branch —
never fix only on the release branch, or the fix is lost at the next cut.
High-throughput teams skip release branches entirely and release from
trunk, fixing forward.

### Long-lived shared development branches (git-flow style)

A permanent `develop` branch plus feature/release/hotfix branch ceremony.
Cost: continuous merge debt, late integration, duplicated fixes, and
ambiguity about what is releasable. Treat as legacy; only justified when
an organization genuinely ships and supports many divergent versions and
cannot adopt flags/cherry-picking. If asked to adopt it, name these costs.

## Decision table

| Criterion | Points to |
|---|---|
| Team ≤ ~5, high trust, fast test suite | TBD, direct to trunk |
| Team needs code review gates / larger team | TBD + short-lived feature branches |
| Continuous deployment (many releases/day) | TBD, release from trunk, fix forward |
| Must support multiple released versions in production | TBD + release branches (fix on trunk, cherry-pick) |
| Slow or unreliable CI | Fix CI first — every strategy degrades without it (pipeline design itself: cicd-pipeline-designer) |
| Unfinished features would block release | Feature flags / dark launch, not a long-lived branch |
| Regulated sign-off per release | Release branches with recorded hardening window |

## Working-agreement defaults (recommend unless overridden)

- Branch lifetime limit: ≤ 2 days; one author per branch.
- Branch from trunk, merge back to trunk; no branch-off-branch chains.
- Merge requirements: review approval + green CI; delete branch on merge.
- Keep trunk releasable at all times; a red trunk build is the team's top
  priority.
- Rebase the short-lived branch onto trunk to stay current (it is private
  to one author, so rewriting it is safe); merge to trunk via the team's
  standard mechanism (merge commit / squash / fast-forward — pick one
  convention and keep it consistent).

## PR hygiene (applies to the short-lived-branch variant)

- One concern per PR. If the description needs "also", split it.
- Small enough to review in one sitting; prefer stacking consecutive
  small PRs over one large one.
- Description answers: what changed, why, how it was tested, where to
  start reading. Link the issue.
- Self-review the diff first: no debug output, no commented-out code, no
  unrelated reformatting.
- CI green and branch current with target before requesting review.
- Draft status while incomplete; ready-for-review means "I would merge
  this".

## Boundaries

- Version numbering, CHANGELOG, tagging the release: release-manager.
- Designing the CI pipeline that gates merges: cicd-pipeline-designer.
