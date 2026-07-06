# GitHub conventions for READMEs and community files

Distilled from: GitHub Docs, "About READMEs"
(https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)
and GitHub Open Source Guides, "Starting an Open Source Project"
(https://opensource.guide/starting-a-project/). Both verified 2026-07-06.
Most rules transfer to GitLab/Gitea/Bitbucket; the location-priority and
profile-README specifics are GitHub's.

## Where the README lives

- GitHub looks for a README in, and displays the first found from:
  `.github/`, repository root, then `docs/`. Root is the convention;
  use it unless the repo already standardized elsewhere.
- Rendered README content is truncated beyond 500 KiB — far past the point
  a README stopped being a front door. Split long material into docs/.

## Rendering features to rely on (not re-implement)

- GitHub auto-generates a table of contents from Markdown headings,
  reachable via the outline menu on the rendered file. Do not hand-write a
  TOC for a README of ordinary size; write clear headings instead.
- Section headings get anchor links; deep-link to sections
  (`#installation`) from issues and docs.

## Relative links — always, for in-repo targets

- Use relative links and image paths for files in the repository
  (`docs/setup.md`, `./CONTRIBUTING.md`). They work for clones, forks,
  and every branch; absolute URLs break in all of those.
- A leading `/` resolves from the repository root.
- Absolute URLs are correct only for genuinely external targets.

## Community files the README points to

Open Source Guides expectations for a public project:

- **LICENSE** — required for open source; without it, default copyright
  applies and reuse is legally blocked. MIT, Apache-2.0, GPLv3 are the
  most common choices. README's License section states the name and links
  the file; choosing a license is the maintainer's call — flag absence,
  never pick one unilaterally.
- **CONTRIBUTING.md** — how to participate: bug reports, feature
  suggestions, environment setup, test/lint commands. Warm tone; concrete
  first-contribution suggestions. README's Contributing section is one
  line plus this link.
- **CODE_OF_CONDUCT.md**, issue/PR templates — link if present; do not
  create them as a side effect of writing a README.
- GitHub surfaces these files in the repo UI when present at root or in
  `.github/`; keeping them out of the README body avoids duplication.

## Profile READMEs (special case)

A repository named exactly like the user/org account, public, with a
README, renders that README on the profile page. Different genre: identity
and pointers, not install instructions. Apply the summary-first rule; skip
the install/usage skeleton.

## README vs wiki vs docs

GitHub guidance: READMEs hold only the essential getting-started
information; longer documentation suits wikis or docs sites. Rule of
thumb — if a section needs scrolling to finish, move the detail out and
leave a link plus a two-line summary.
