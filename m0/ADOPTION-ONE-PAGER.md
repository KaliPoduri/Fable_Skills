# Adoption one-pager (skeleton — fill at M0)

Names the adoption owner and gives the dev team the one page they need to
pick and invoke the right skill. Fill the blanks; keep it to one page for
the actual rollout.

## Ownership (U10)

- **Adoption owner:** ____ (drives rollout, collects feedback)
- **Rollout channel:** ____ (how the team learns the skills exist — e.g.
  team channel, README, brown-bag)
- **Support channel:** ____ (where devs ask when a skill misbehaves)

## Which skill do I use?

| I have… | Use | Invoke by typing (example) |
|---|---|---|
| A job that **failed** — error/log, need the root cause | **etl-assistant** | "this job failed with `<error>` — what's the root cause?" |
| A "how does flow X work?" / "explain this job" question | **etl-assistant** | "explain how the `<job>` flow works" |
| A SQL/script I want to improve (no runtime evidence) | **etl-assistant** | "improve this SQL: `<paste>`" |
| A job that **runs but is slow** — physical plan / Spark UI | **spark-performance-advisor** | "this job is slow, here's the physical plan: `<paste>`" |
| Need to (re)generate the knowledge base after code changed | **etl-knowledge-builder** | "rebuild the ETL knowledge base for `<repo>`" (agent mode) |

Boundary reminder: **etl-assistant** advises from code; **spark-performance-advisor**
advises from runtime evidence (plans/UI). Failed vs slow decides which one.
"Handoff" = a skill telling you which skill to invoke next — there is no
automatic switch.

## Mode note (fill after M0 Flow 2)

- Skills require: **agent mode** / **works in ask mode too** — ____
- etl-knowledge-builder ALWAYS needs agent mode (writes files + runs git).

## Demo incident (pick one from BASELINE.md)

- Incident: ____
- Skill used: ____
- Before (time-to-RCA from baseline): ____  →  With the skill: ____
