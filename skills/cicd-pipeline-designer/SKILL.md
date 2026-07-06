---
name: cicd-pipeline-designer
description: "Designs CI/CD pipelines: stages, test tiers, quality gates, caching, DORA alignment. Use this skill when asked to design a CI/CD pipeline or CI quality gates. Do not use for canary or blue-green rollout mechanics; use deployment-strategist. Not for release cutting (release-manager) or branch strategy (git-workflow-expert). Platform-agnostic: generic YAML plus GitHub Actions/GitLab/Jenkins notes."
metadata:
  version: "1.0.0"
  last-verified: "2026-07-06"
---

# CI/CD Pipeline Designer

Design a CI/CD pipeline for the project at hand: pick the stages, order them
for fastest feedback, define quality gates and failure policy, plan caching
and artifact versioning, and check the design against DORA capabilities and
metrics. Produce a written pipeline design document plus a generic YAML
sketch the team can translate to their platform.

## Constraints

Assume no external internet access, no paid tools, and English output.
Never send project code or data to external services.
Stay technology-agnostic: express the pipeline as generic YAML with
per-platform notes for GitHub Actions, GitLab CI, and Jenkins. Do not emit
platform-locked syntax unless the user names their platform.
Design pipelines only. Rollout mechanics (canary, blue-green, feature
flags) belong to deployment-strategist; release cutting and versioning
decisions belong to release-manager; branching models belong to
git-workflow-expert.

## Workflow

1. **Establish context.** Ask or infer: language/build tool, test suite
   shape (unit/integration/e2e), deploy target (server, container,
   package, static site), team size, current pain (slow builds, flaky
   deploys, no gates). Inspect the repo for existing pipeline files
   (`.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`, `azure-pipelines.yml`)
   and build files before proposing anything.
2. **Choose the stage layout.** Default backbone, in feedback-speed order:
   lint/static checks, build + unit tests, package artifact, integration
   tests, security checks, e2e/acceptance tests, deploy to staging,
   deploy to production. Merge or drop stages the project does not need;
   never add stages "for later". Load `references/pipeline-patterns.md`
   for stage responsibilities and ordering rules.
3. **Define test tiers per stage.** Fast tests (unit, lint) run on every
   commit and block merge. Slower tiers (integration, e2e) run after a
   green fast tier, on the merged result or on a schedule if runtime
   forces it. State the target runtime budget per tier (fast tier under
   10 minutes is the working default from Continuous Delivery practice).
4. **Set quality gates and failure policy.** For each gate specify:
   condition (tests pass, coverage floor, no high-severity findings),
   scope (blocks merge, blocks deploy, warns only), and override rule
   (who may bypass, how it is recorded). Every gate failure must stop the
   pipeline by default — "continue on error" only for explicitly
   advisory checks, and label them advisory.
5. **Place security checks.** Minimum set: dependency/SCA scan, secret
   scan, and static analysis (SAST) in the pipeline; container/image scan
   if images are built. Shift them left of deploy, right of unit tests.
   Map to the DORA "pervasive security" capability.
6. **Plan caching.** Cache dependency downloads and build outputs keyed
   on lockfile/build-file hash. Never cache test results or artifacts
   destined for deploy. Note per-platform cache mechanics from
   `references/pipeline-patterns.md`.
7. **Design the artifact flow.** Build once, promote the same artifact
   through every environment — never rebuild per environment. Version
   artifacts immutably (commit SHA plus human-readable tag); store in a
   registry/artifact store; record provenance (pipeline run id, commit).
8. **Check against DORA.** Load `references/dora.md`. Confirm the design
   supports: continuous integration, deployment automation, test
   automation, trunk-based development compatibility, version control of
   pipeline config, working in small batches. State which of the five
   DORA metrics the pipeline improves and how the team could measure
   them from pipeline data.
9. **Write the deliverable** using the output template below: design
   document plus generic YAML sketch plus per-platform notes.
10. **Hand off boundaries.** If the user then asks how to roll out
    (canary/blue-green), point to deployment-strategist; for cutting the
    release itself, release-manager; for branch strategy,
    git-workflow-expert.

## Output template

Produce a Markdown document with exactly these headings:

```markdown
# CI/CD Pipeline Design — <project>

## Context and assumptions
<stack, deploy target, team constraints, existing pipeline state>

## Stage layout
| # | Stage | Purpose | Trigger | Runtime budget | Blocks |
|---|-------|---------|---------|----------------|--------|

## Quality gates and failure policy
| Gate | Condition | Scope (merge/deploy/advisory) | Override rule |
|------|-----------|-------------------------------|---------------|

## Caching plan
<what is cached, cache key, invalidation, what must never be cached>

## Artifact versioning flow
<build-once point, version scheme, store, promotion path env-by-env>

## Pipeline sketch (generic YAML)
<generic YAML per references/pipeline-patterns.md conventions>

## Platform notes
### GitHub Actions
### GitLab CI
### Jenkins

## DORA alignment
<capabilities supported; which of the five metrics improve and how to
measure them from pipeline data>

## Out of scope
<named handoffs: deployment-strategist, release-manager,
git-workflow-expert>
```

The generic YAML sketch uses this neutral shape (not any vendor's schema):

```yaml
pipeline:
  trigger: [push, pull_request]
  stages:
    - name: fast-checks
      jobs: [lint, unit-tests]
      budget: 10m
      on_failure: stop
    - name: package
      jobs: [build-artifact]
      produces: app-${GIT_SHA}
    - name: verify
      jobs: [integration-tests, sast, dependency-scan, secret-scan]
      needs: package
    - name: acceptance
      jobs: [e2e-tests]
      environment: staging
      uses: app-${GIT_SHA}
    - name: deploy
      jobs: [deploy-production]
      uses: app-${GIT_SHA}
      gate: manual-or-automated-per-team-policy
```

## References (load on demand)

- `references/SOURCES.md` — source manifest (always present).
- `references/pipeline-patterns.md` — load when laying out stages,
  gates, caching, or writing the YAML sketch and platform notes
  (steps 2–7 and the sketch section).
- `references/dora.md` — load when doing the DORA alignment check
  (step 8) or when the user asks about DORA capabilities or metrics.

## Checklist

- [ ] Stages ordered fastest-feedback-first; each has a runtime budget.
- [ ] Every gate has condition, scope, and override rule; failures stop
      the pipeline unless explicitly labeled advisory.
- [ ] Security checks (SCA, secret scan, SAST) present and placed before
      deploy.
- [ ] Artifact is built once and promoted; version is immutable and
      traceable to a commit.
- [ ] Caching keys derive from lockfile/build-file hashes; deployables
      are never served from cache.
- [ ] DORA alignment section names concrete capabilities and metrics
      with a measurement source.
- [ ] Rollout mechanics, release cutting, and branch strategy are
      explicitly deferred to their sibling skills, not designed here.
- [ ] Output follows the template above.
