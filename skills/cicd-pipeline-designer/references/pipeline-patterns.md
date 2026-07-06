# Pipeline patterns — stages, gates, caching, artifacts, platforms

Source: https://continuousdelivery.com/ (Jez Humble; companion to Humble
& Farley, *Continuous Delivery*, Addison-Wesley 2010), verified
2026-07-06. Platform notes distilled from GitHub Actions, GitLab CI, and
Jenkins official documentation conventions.

## Deployment-pipeline principles (Continuous Delivery)

- **Always releasable.** Code is kept in a deployable state at all
  times; the pipeline exists to prove releasability on every change.
- **Build quality in.** Quality activities (testing, security,
  performance) run continuously inside the pipeline, not as a separate
  late phase.
- **Fast feedback.** Developers learn about regressions within minutes.
  Order stages so the cheapest, most-likely-to-fail checks run first.
- **Deploys are routine.** The pipeline makes deployment a predictable,
  repeatable, on-demand affair — fully automated, no manual steps
  between artifact and environment.
- **Build once, promote many.** One artifact per change, promoted
  unchanged through every environment. Rebuilding per environment
  invalidates everything tested earlier.

## Stage responsibilities and ordering

| Stage | Responsibility | Ordering rule |
|---|---|---|
| Lint / static checks | Formatting, compile/type errors, cheap static analysis | First — seconds to run, catches the most trivial failures |
| Build + unit tests | Compile/package check, fast isolated tests | Second — the commit gate; target whole fast tier under 10 minutes |
| Package artifact | Produce the immutable deployable (binary, image, bundle) | After unit green; everything downstream consumes this artifact |
| Integration tests | Component wiring, DB/queue contracts, service APIs | After package; runs against the built artifact |
| Security checks | SCA/dependency scan, secret scan, SAST; image scan if containers | Parallel with or right after integration; always before any deploy |
| E2E / acceptance | User-visible flows against a deployed staging environment | After artifact deployed to staging |
| Deploy staging | Automated deploy of the artifact to a production-like env | Gate for acceptance tier |
| Deploy production | Same automated mechanism as staging, same artifact | Last; manual approval or automatic per team policy |

Rules of thumb:

- Merge/drop stages the project does not need (a static site needs no
  integration tier). Never invent stages for hypothetical futures.
- Anything slower than the fast-tier budget moves right (post-merge) or
  to a schedule — never delete the coverage, relocate it.
- Flaky tests are pipeline defects: quarantine, fix, or delete;
  auto-retry hides real failures and destroys gate credibility.

## Quality gates

A gate is fully specified by three fields:

1. **Condition** — objective and machine-checkable (all tests pass,
   coverage ≥ floor, zero high-severity findings, artifact signed).
2. **Scope** — what it blocks: merge (PR checks), deploy (promotion
   gates), or advisory (reported, never blocks — label it as such).
3. **Override rule** — who may bypass and how the bypass is recorded
   (e.g., named approver + reason in the run log). A gate nobody may
   ever override becomes a gate people route around.

Failure policy default: stop the pipeline. `continue-on-error` semantics
are reserved for advisory checks only.

## Caching

| Cache | Key | Note |
|---|---|---|
| Dependency downloads (npm/pip/maven/go modules) | Hash of lockfile/build file | Restore-keys fallback to latest on partial miss |
| Build outputs / incremental compile | Hash of source tree or build-tool-native | Only with a build tool that guarantees correct invalidation |
| Container layers | Base image + Dockerfile instruction order | Order Dockerfile least-changing → most-changing |

Never cache: test results, deployable artifacts, secrets. Artifacts go
to an artifact store with provenance, not a cache — caches are
best-effort and evictable; artifacts must be immutable and addressable.

## Artifact versioning flow

- Version = commit SHA (machine identity) + optional human tag
  (e.g., `1.4.2` from release-manager's process, or `app-<sha>` for
  every build).
- Store in a registry/artifact store with: pipeline run id, commit SHA,
  branch, build timestamp.
- Promotion = re-tagging/marking the same stored artifact for the next
  environment; never a rebuild.
- Retention: keep artifacts at least as long as the oldest thing running
  in production, plus rollback window.

## Platform notes

### GitHub Actions

- Workflow files in `.github/workflows/*.yml`; stages map to `jobs`,
  ordering via `needs:`; per-commit trigger via `on: [push, pull_request]`.
- Cache: `actions/cache` with `key`/`restore-keys`; artifact handoff
  between jobs via `actions/upload-artifact`/`download-artifact`.
- Gates: branch protection required checks (merge scope); `environments`
  with required reviewers (deploy scope).
- Advisory checks: `continue-on-error: true` on the job.

### GitLab CI

- Single `.gitlab-ci.yml`; `stages:` list is explicit; jobs bind via
  `stage:`; DAG ordering with `needs:`.
- Cache: `cache:` with `key: files: [lockfile]`; artifact handoff via
  `artifacts:` (also feeds `dependencies:`/`needs:` downloads).
- Gates: merge request pipelines + "pipeline must succeed" setting
  (merge scope); `when: manual` + protected environments (deploy scope).
- Advisory checks: `allow_failure: true`.

### Jenkins

- Declarative `Jenkinsfile` in the repo; stages are `stage {}` blocks
  inside `pipeline { stages {} }`; parallelize with `parallel {}`.
- Cache: no first-class cache — use workspace reuse carefully, a shared
  dependency mirror, or plugin-provided caches; prefer build-tool-native
  caching.
- Artifact handoff: `archiveArtifacts` / `stash`+`unstash` within a run;
  external artifact repository (e.g., an in-org registry) between runs.
- Gates: `input {}` step for manual approval (deploy scope); multibranch
  + branch protection on the SCM side (merge scope).
- Advisory checks: `catchError(buildResult: 'SUCCESS', stageResult:
  'FAILURE')`.
