# DORA capabilities and metrics — distilled reference

Source: https://dora.dev/capabilities/ and
https://dora.dev/guides/dora-metrics-four-keys/ (verified 2026-07-06).
DORA (DevOps Research and Assessment) is the largest and longest-running
research program studying the capabilities that drive software delivery
and operations performance.

## The delivery metrics: from four keys to five

DORA's metrics have evolved from the original "four keys" to a
five-metric model. Failed Deployment Recovery Time replaced the older
MTTR framing, and Deployment Rework Rate was added. Use the five-metric
model in new designs; recognize "four key metrics" as the historical
name users still type.

Throughput (3):

| Metric | Definition |
|---|---|
| Change lead time | Time for a change to go from committed to version control to deployed in production. |
| Deployment frequency | Number of deployments over a given period, or time between deployments. |
| Failed deployment recovery time | Time to recover from a deployment that fails and requires immediate intervention. |

Stability (2):

| Metric | Definition |
|---|---|
| Change fail rate | Ratio of deployments that require immediate intervention following a deployment. |
| Deployment rework rate | Ratio of deployments that are unplanned but happen as a result of an incident in production. |

### Measuring them from pipeline data

- Change lead time: commit timestamp → production-deploy job success
  timestamp, per change.
- Deployment frequency: count of successful production-deploy job runs
  per period.
- Failed deployment recovery time: failed production deploy →
  next successful deploy or rollback completion.
- Change fail rate: production deploys followed by hotfix/rollback ÷
  total production deploys.
- Deployment rework rate: unplanned incident-driven deploys ÷ total
  production deploys (needs incident tagging on deploy runs).

## Capabilities catalog

The catalog holds 34 capabilities (as verified 2026-07-06), organized
into a core model of technical/process fundamentals, an AI-related set,
and further capabilities supporting learning and feedback. The ones a
pipeline design directly exercises:

| Capability | What the pipeline must provide |
|---|---|
| Continuous integration | Every commit triggers automated build + fast tests; broken builds fixed immediately; merge blocked on red. |
| Continuous delivery | Software kept releasable at all times; deploy is push-button or automatic from a green pipeline. |
| Deployment automation | Deploys are fully scripted in the pipeline; no manual steps between artifact and environment. |
| Test automation | Reliable automated suites at unit/integration/e2e tiers, run in the pipeline, owned by developers. |
| Trunk-based development | Pipeline supports short-lived branches and frequent merges to trunk; fast tier cheap enough to run per commit. |
| Version control | Application code, pipeline config, and infrastructure definitions all live in version control. |
| Pervasive security | Security checks (SCA, secret scan, SAST, image scan) integrated into the pipeline, not a separate late phase. |
| Working in small batches | Pipeline fast enough that small, frequent changes are cheaper than big-batch releases. |
| Monitoring and observability | Pipeline emits deploy events/markers so production telemetry can correlate changes with incidents. |
| Streamlining change approval | Gates encode approval policy in the pipeline (automated checks or lightweight recorded approvals) instead of external change boards. |

Other catalog areas (culture, learning, work-in-process limits,
AI-related capabilities such as platform engineering) matter to
performance but are outside a pipeline design's direct scope — name
them only if the user asks.

## Using this in a design review

For step 8 of the workflow, answer three questions in the deliverable:

1. Which capabilities above does the design satisfy, and where
   (stage/gate)?
2. Which of the five metrics should improve, and by what mechanism
   (e.g., caching cuts change lead time; build-once promotion cuts
   change fail rate)?
3. Where would the team read each metric from pipeline data (see
   measurement notes above)?
