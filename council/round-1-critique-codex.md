# Council round 1 — Codex seat critique (verbatim)

Read-only review completed. I did not edit or create files. I used official GitHub and Apache Spark docs for the fact-check portions.

**Major Concerns**

1. **The harness claim is too loose.** The plan says "GitHub Copilot Chat (VS Code) ONLY" and then assumes native skills from `.agents/skills/`. GitHub docs confirm agent skills can live in `.agents/skills`, but the support claim is for agent-capable Copilot surfaces, including "agent mode in Visual Studio Code," not necessarily ordinary Chat usage. This must be restated as: "requires Copilot agent mode in VS Code, enabled by org policy." Source: GitHub agent skills docs. (docs.github.com/en/copilot/concepts/agents/about-agent-skills)

2. **Skill A is the riskiest part and may be infeasible as pure LLM work.** Asking Copilot to trace 3–10 repos, hundreds to ~2000 files, scheduler configs, PySpark, SQL, shell, params, and lineage into accurate markdown is likely to produce omissions and false lineage. The plan has no mechanical validation against scheduler metadata, job counts, table inventory, or known incidents.

3. **The plan rejects simpler native Copilot context options too quickly.** Copilot already has repository semantic indexing for Chat in GitHub and VS Code, and Spaces can collect repos, files, notes, uploads, and shared context. These may cover much of the "deep understanding" need without building a generated KB first. Sources: repo indexing and Spaces docs. (docs.github.com/en/copilot/concepts/context/repository-indexing; docs.github.com/en/copilot/concepts/context/spaces)

4. **The "Copilot-only" constraint has hidden policy dependencies.** Semantic indexing for non-GitHub/local repos is disabled by default for org/business contexts unless enabled by policy, and it uploads data to GitHub for searchability. That affects cloned repos, logs, and any dedicated KB repo. Source: GitHub repo indexing docs.

5. **Security/compliance is underdeveloped.** "Org policy allows code and logs in Copilot" is not enough. Spark logs can contain paths, table names, customer identifiers, secrets, tokens, SQL literals, partition values, and incident details. The plan needs mandatory redaction rules before paste/upload and before appending to `errors/playbook.md`.

6. **The KB size model is probably too optimistic.** `INDEX.md` at ~200 lines cannot reliably hold a repo table, full job inventory, routing guide, and cross-repo overview if there are many pipelines. `lineage.md` is explicitly unbounded and could become the worst file for chunk navigation.

7. **Staleness stamps are necessary but insufficient.** Commit hashes do not cover runtime scheduler state, deployed configs, external table schemas, Hive metastore stats, data drift, job parameters injected outside repo, or hotfixes not represented in the cloned workspace.

8. **"No unconfirmed assumptions currently registered" is false.** Open assumptions remain: agent mode enabled, skill loading enabled, multi-root workspace behavior, repo indexing policy, all repos visible, scheduler configs complete, Spark minor version, YARN/history-server access, event-log retention, data sensitivity, and whether devs can change Spark configs.

9. **Performance advice needs stronger guardrails.** Spark tuning depends on data size, skew, file layout, stats, cluster resources, Spark minor version, permissions, and whether configs are job-scoped or cluster-scoped. Physical plans alone are not enough for safe prescriptions. Spark docs confirm SQL UI metrics and plans exist, but config behavior is version-specific. (spark.apache.org/docs/3.5.7/web-ui.html; spark.apache.org/docs/3.5.7/sql-performance-tuning.html)

10. **Success gates are vague.** "Majority correctly diagnosed" is too weak for an RCA assistant. "Measured improvement" lacks a threshold, baseline protocol, repeat-run control, and rollback criteria.

**Minor Concerns**

1. Skill names are placeholders, but the plan should settle stable names before evals and distribution.

2. `jobs/<job>.md` needs a filename safety rule for spaces, slashes, duplicate job names, and renamed jobs.

3. The plan says "pointers, not copies," but SQL snippets may be needed as evidence. Define a maximum excerpt rule or forbid excerpts entirely.

4. The "errors/playbook.md" memory may become noisy unless entries require confirmed cause, date, job, symptoms, fix, verification, and redaction status.

5. M1 says "builder eyeballs it," but accuracy should be checked by a domain owner, not just the builder.

6. The Spark advisor should explicitly distinguish failed job RCA from slow job tuning; they use different evidence.

7. The plan should require exact Spark minor version because AQE defaults and config availability changed across Spark 3.x. AQE is documented as default since Spark 3.2.0, not all Spark 3.x. (spark.apache.org/docs/3.5.7/sql-performance-tuning.html)

8. The plan does not specify how users obtain completed-job Spark UI data if the app has ended; history server/event logs may be required.

9. "Advise-only" conflicts slightly with Skill A generating KB files. Clarify "never auto-change application code; KB/docs writes are allowed only on request."

10. GitHub CLI `gh skill` exists but is public preview and requires GitHub CLI 2.90.0+, so manual-copy distribution is okay but should mention why CLI install is not used. (docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills)

**Concrete Refinements**

1. Add a blocking M0: verify Copilot agent mode in VS Code, `.agents/skills` loading, org policy for local/non-GitHub indexing, log handling, and multi-root workspace behavior.

2. Replace full Skill A first with a smaller pilot: one repo, 3–5 known jobs, 3 known failures, one slow job, manually reviewed against scheduler truth.

3. Make the scheduler/job inventory authoritative. If no parser is allowed, require a human-maintained `jobs.yml` or table exported from the scheduler as the seed.

4. Split lineage early by domain or table prefix instead of one growing `lineage.md`.

5. Add redaction rules and a "safe-to-share checklist" to Skills B and C before accepting logs, plans, screenshots, or incident notes.

6. Tighten M2: use a fixed test set of known past incidents; require no high-confidence wrong answers, cited evidence for every answer, and correct "insufficient evidence" behavior.

7. Tighten M3: define baseline runtime, repeated measurements, minimum improvement threshold, rollback plan, and owner approval for config changes.

8. Consider a simpler v1: one `spark-etl-assistant` skill plus small curated references and an incident playbook, using Copilot repo indexing/Spaces for live code context. Add generated KB only if the pilot proves native context is not enough.

Codex session ID: 019f4c08-6acd-7011-b619-407f8e543ff8
