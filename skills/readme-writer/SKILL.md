---
name: readme-writer
description: "Writes or overhauls repository README files: summary, quick start, install, usage, config, license. Use this skill when asked to write a README or improve an out-of-date README. Do not use for user guides or tutorials; use user-guide-writer instead. Do not use for editing arbitrary prose or docs for clarity; use tech-writer instead."
metadata:
  version: "1.0.0"
  last-verified: "2026-07-06"
---

# README Writer

Write or overhaul a repository README so a newcomer can answer, within one
screen of reading: what this project does, why it is useful, how to get it
running, and where to get help. Ground every claim in the actual repository
— read the code, manifests, and scripts first; never describe commands or
features you have not verified exist.

## Constraints

Assume no external internet access, no paid tools, and English output.
Never send project code or data to external services.
Verify before you write: every install command, usage example, config key,
and badge must come from files in the repository, not from memory.
Do not invent project status, roadmap items, or license terms; if a fact
is missing (e.g., no LICENSE file), flag it instead of guessing.
Keep the README a front door, not a manual — deep material links out to
docs/ or the wiki (GitHub: longer documentation belongs in wikis/docs).

## Workflow

1. Inventory the repository. Identify: language(s) and package manifests
   (package.json, pyproject.toml, go.mod, …), build/run scripts, test
   commands, config files and environment variables, CI setup, LICENSE,
   CONTRIBUTING.md, existing docs/ folder, and the current README if any.
2. Determine the audience. Library consumer, app end user, internal team,
   or contributor? The quick start must serve the primary audience first;
   secondary audiences get a link (e.g., "Developing" section or
   CONTRIBUTING.md).
3. If overhauling an existing README: diff it against reality. List every
   claim that is stale (dead commands, renamed scripts, removed features,
   wrong versions) and every gap (missing install/usage/config/license).
   Preserve content that is still accurate — this is an overhaul, not a
   rewrite for its own sake.
4. Extract the one-paragraph summary: what the project does and why it is
   useful, in plain language, no marketing adjectives. State what makes it
   different if alternatives exist (Make a README: description should
   cover motivation and what problem it solves).
5. Write the quick start: the shortest verified path from clone/install to
   first visible result. Every command must be copy-pasteable and match
   the repo's actual scripts. Note prerequisites (runtime versions, system
   deps) explicitly.
6. Write installation and usage: expand beyond quick start only where the
   repo warrants it. Show real, minimal examples with expected output
   where feasible. Load references/readme-structure.md for the full
   section order and per-section guidance.
7. Document configuration: table of config keys / env vars actually read
   by the code, with default and purpose. Point to sample config files if
   present.
8. Add the community sections: where to get help (issues, discussions,
   chat — only channels that exist), contributing pointer (link
   CONTRIBUTING.md if present; otherwise one line on how to propose
   changes), authors/acknowledgments if the project tracks them, license
   note matching the LICENSE file, and project status if development is
   dormant (Make a README: say so explicitly to set expectations).
9. Order and trim. Follow the section order in the Output template; cut
   any section with nothing verified to say rather than padding it. Use
   relative links for in-repo files so they work in clones and branches
   (GitHub docs). Load references/github-conventions.md when the repo is
   hosted on a forge (rendering, README locations, relative links,
   community files).
10. Verify: run or dry-check the quick-start commands if the environment
    allows; otherwise mark them as untested in your summary to the user
    (never in the README). Confirm every relative link target exists.
    Run the Checklist, then present the README (or the diff, when
    overhauling).

## Output template

Produce a Markdown README with these sections, in this order. Sections
marked (if applicable) are omitted — not left empty — when they do not
apply:

```markdown
# <Project name>

<Badges — only ones whose services the project actually uses.> (if applicable)

<One-paragraph summary: what it does, who it is for, why it is useful.>

<Screenshot / GIF for visual projects.> (if applicable)

## Quick start
<Prerequisites, then the shortest copy-pasteable path to a first result.>

## Installation
<Full install matrix: package manager, from source, containers.> (if applicable)

## Usage
<Minimal real examples; expected output where useful. Link docs/ for more.>

## Configuration
| Key / variable | Default | Purpose |
|---|---|---|
(if applicable)

## Getting help
<Issues / discussions / chat — only channels that exist.>

## Contributing
<One line + link to CONTRIBUTING.md, or how to propose changes.>

## Authors and acknowledgments (if applicable)

## License
<SPDX name matching the LICENSE file, one line. If no LICENSE file exists,
flag it to the user; do not state a license in the README.>

## Project status (if applicable — required when development is dormant)
```

## Edge cases

- Monorepo: the root README summarizes the whole and links each package;
  each published package gets its own README following the same template.
  Write only the READMEs the user asked for.
- Profile README (repo named after the user/org): different genre —
  identity and pointers, no install/usage skeleton. See
  references/github-conventions.md.
- No-code repos (docs, data, config): keep summary, usage ("how to
  consume these files"), contributing, and license; drop install.
- Missing LICENSE, CONTRIBUTING.md, or support channels: leave the
  corresponding section out or minimal, and report the gap to the user as
  a repo issue — never fabricate the missing artifact's contents.
- Existing README in a non-root location (.github/ or docs/): keep it
  where it is unless the user asks to move it; note the location rule
  from references/github-conventions.md.

## References (load on demand)

- `references/SOURCES.md` — source manifest (always present).
- `references/readme-structure.md` — load when deciding sections, their
  order, and per-section content (Make a README + GitHub guidance).
- `references/github-conventions.md` — load when the repository is hosted
  on GitHub or a similar forge (README locations, rendering, relative
  links, profile READMEs, community files).

## Checklist

- [ ] Every command, script name, config key, and version was verified
      against files in this repository.
- [ ] Quick start goes from zero to first visible result with
      copy-pasteable commands and stated prerequisites.
- [ ] All in-repo links are relative and their targets exist.
- [ ] License section matches the LICENSE file, or its absence was flagged
      to the user.
- [ ] No empty or padded sections; inapplicable sections omitted.
- [ ] Deep documentation is linked, not inlined; README stays a front door.
- [ ] Output follows the section order of the template above.
- [ ] For overhauls: stale claims corrected, accurate content preserved,
      and the changes summarized to the user.
