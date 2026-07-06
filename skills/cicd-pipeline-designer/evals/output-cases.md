# Output eval cases (≥3)

Each case is run twice — WITH the skill installed and WITHOUT (raw
assistant) — and scored against the rubric in
docs/AUTHORING-GUIDE.md §Eval thresholds. The skill must beat raw output.

## Case 1

- Prompt: "Design our CI/CD pipeline. It's a Node.js API, deployed as a
  Docker container to Kubernetes. We have unit tests and a slow Cypress
  suite. Two engineers."
- Input artifacts (if any): package.json with test scripts; existing
  minimal .github/workflows/test.yml running only unit tests.
- Rubric focus: template compliance, completeness, actionability.
- Expected qualities: all template headings present; stage table with
  runtime budgets; Cypress placed post-merge/staging (not in the fast
  tier); build-once image promotion by SHA; cache keyed on lockfile;
  gate table with condition/scope/override; GitHub Actions platform
  notes used since platform is known; DORA section names the five
  metrics with pipeline-data measurement; rollout mechanics explicitly
  deferred to deployment-strategist.

## Case 2

- Prompt: "Set up quality gates for CI — right now anyone can merge red
  builds and we deploy manually from laptops."
- Input artifacts (if any): none (greenfield policy question).
- Rubric focus: source accuracy, actionability.
- Expected qualities: gates specified as condition + scope + override
  rule; default failure policy stops the pipeline; advisory checks
  labeled; manual-laptop deploys replaced by deployment automation
  (DORA deployment automation capability cited); merge-blocking vs
  deploy-blocking gates distinguished; no platform lock-in since none
  was stated.

## Case 3

- Prompt: "We want to improve our DORA metrics. Our pipeline is one big
  job that rebuilds the app for each of dev, staging, and prod."
- Input artifacts (if any): description of a monolithic Jenkinsfile.
- Rubric focus: source accuracy (DORA five-metric model, build-once
  principle), completeness.
- Expected qualities: identifies rebuild-per-environment as the core
  defect and prescribes build-once/promote; uses the current five-metric
  DORA model (failed deployment recovery time, deployment rework rate —
  not just legacy MTTR); maps each proposed change to the metric it
  moves and where to measure it; Jenkins platform notes (stages,
  input gates, artifact archiving) applied.
