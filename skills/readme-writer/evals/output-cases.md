# Output eval cases (≥3)

Each case is run twice — WITH the skill installed and WITHOUT (raw
assistant) — and scored against the rubric in
docs/AUTHORING-GUIDE.md §Eval thresholds. The skill must beat raw output.

## Case 1

- Prompt: "Write a README for this repository." (run inside a small CLI project with pyproject.toml, a console-script entry point, a tests/ folder, an .env.example, and an MIT LICENSE file — but no existing README)
- Input artifacts (if any): the repository itself.
- Rubric focus: source accuracy (grounding in repo); template compliance.
- Expected qualities: summary derived from actual code/manifest, not generic filler; quick start uses the real install command and entry point from pyproject.toml with prerequisites stated; configuration table lists the variables from .env.example; License section says MIT matching the LICENSE file; all in-repo links relative and resolving; no Roadmap/Badges/Visuals sections invented; sections follow the template order.

## Case 2

- Prompt: "Our README is out of date — the install steps still reference the old Makefile we deleted, and we added Docker support last month. Bring it in line with the repo."
- Input artifacts (if any): an existing README with stale Makefile commands; repo now contains Dockerfile, docker-compose.yml, and npm scripts.
- Rubric focus: actionability; source accuracy (stale-claim detection); minimal-change discipline.
- Expected qualities: every stale Makefile command found and replaced with verified npm/docker commands; Docker usage added under Installation/Quick start; still-accurate prose preserved rather than rewritten wholesale; a summary of what changed and why reported to the user; no unverified commands introduced.

## Case 3

- Prompt: "Improve our README so a brand-new contributor can get the dev environment running; contributions section too. Keep it short — deep docs live in docs/."
- Input artifacts (if any): repo with docs/ folder, CONTRIBUTING.md, test and lint scripts in the package manifest.
- Rubric focus: completeness (audience fit); template compliance (front-door rule).
- Expected qualities: quick start targets the contributor audience with verified setup, test, and lint commands; Contributing section is one line linking the real CONTRIBUTING.md, not an inlined guide; deep material linked into docs/ with relative links instead of expanded in the README; Getting help points only at channels that exist in the repo metadata; inapplicable sections omitted rather than padded.
