# Repo instructions snippet — ETL skill routing + chunk protocol

Paste the block below into each code repo's `copilot-instructions.md`
(or `AGENTS.md`) — PLAN.md §2 routing hardening. Replace
`<KB-REPO-PATH>` with the path to the knowledge-base repo/folder as
cloned in your workspace (e.g. `../etl-knowledge-repo`) before
committing.

```markdown
## ETL skill routing

- Job FAILED / root cause / explain a flow / improve an ETL SQL or PySpark script (no runtime evidence) → invoke `etl-assistant`.
  Example: "Use etl-assistant: job orders_daily failed with FetchFailedException — what's the root cause?"
- Job runs but is SLOW and you HAVE runtime evidence (physical plan, Spark UI, timings) → invoke `spark-performance-advisor`.
  Example: "Use spark-performance-advisor: here is the physical plan for billing_agg — why is it slow?"
- (Re)generate or update the ETL knowledge base → invoke `etl-knowledge-builder` (agent mode required).
  Example: "Use etl-knowledge-builder: rebuild the KB chunks for the billing-etl repo."

## ETL knowledge-base chunk protocol

- The KB lives at `<KB-REPO-PATH>/etl-knowledge/`. <!-- REPLACE <KB-REPO-PATH> with your KB repo path -->
- Read `etl-knowledge/INDEX.md` FIRST, then the routed per-repo index, then the job chunk — at most 3 KB files per question; never bulk-read the KB.
- KB chunks are pointers, not truth: verify claims in live code (`repo:path:line`) before concluding.
```
