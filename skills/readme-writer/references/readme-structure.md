# README structure — sections, order, and per-section guidance

Distilled from: Make a README (https://www.makeareadme.com/) and GitHub
Open Source Guides, "Starting an Open Source Project"
(https://opensource.guide/starting-a-project/). Both verified 2026-07-06.

## The questions a README must answer

GitHub's baseline (About READMEs + Open Source Guides): a README tells
readers —

1. What the project does.
2. Why the project is useful.
3. How users can get started.
4. Where users can get help.
5. Who maintains and contributes to the project.

If any of these cannot be answered after reading the first screen, the
README fails regardless of length.

## Make a README's suggested sections, in order

1. **Name** — self-explaining if possible.
2. **Description** — what it does, why it exists, what problem it solves,
   what makes it different from alternatives. Motivation and context, not
   feature bullets. This is the most-read paragraph in the repo.
3. **Badges** — build status, coverage, package version. Only badges whose
   backing service the project actually uses; a red or dead badge is worse
   than none.
4. **Visuals** — screenshots or GIFs for anything with a UI or visual
   output. One good screenshot beats three paragraphs.
5. **Installation** — prerequisites (runtime versions, system packages)
   stated explicitly; then per-environment steps. Assume the reader is a
   novice at THIS project even if expert generally.
6. **Usage** — liberal real examples, smallest useful ones inline,
   expected output shown where it helps. Link to deeper docs rather than
   inlining a manual ("too long is better than too short" applies to the
   whole README, but reference-level detail still belongs in docs/).
7. **Support** — where to ask for help: issue tracker, discussions, chat.
   Only channels that exist and are watched.
8. **Roadmap** — planned releases/ideas, if the project publicly plans.
   Omit rather than invent.
9. **Contributing** — whether contributions are welcome and how to start:
   environment setup, how to run tests, lint commands. Usually one line
   plus a link to CONTRIBUTING.md.
10. **Authors and acknowledgment** — credit where the project tracks it.
11. **License** — one line naming the license; must match the LICENSE
    file. Open Source Guides: a public open source project must have a
    license; MIT, Apache-2.0, and GPLv3 are the most common. If LICENSE is
    missing, that is a repo problem to flag — not a README sentence to
    fabricate.
12. **Project status** — if development has slowed or stopped, say so at
    the top or bottom: it sets expectations and invites maintainers.

Adaptation rule: this order is the default skeleton, not a form to fill.
Combine Installation into a "Quick start" for simple projects; drop
Badges/Visuals/Roadmap when they have no verified content.

## When and where

- Create the README before showing the project to anyone; it is the
  first file a visitor reads.
- Top-level directory, Markdown format (universal forge rendering).
- Complement, do not duplicate: CONTRIBUTING.md, CHANGELOG, issue/PR
  templates, and docs/ each own their material; the README links to them.

## Quality rules

- Plain language; no marketing adjectives; concrete nouns and verbs.
- Copy-pasteable commands only — every command verified against the repo's
  actual scripts and manifests.
- Novice-friendly install: list prerequisites; do not assume global tools.
- Keep it current: a README that lies about commands is worse than no
  README. When overhauling, hunt stale claims first.
- For internal/company repos the same skeleton applies; "Support" points
  at the owning team/channel and "License" may be replaced by an internal
  ownership note — never dropped silently.
