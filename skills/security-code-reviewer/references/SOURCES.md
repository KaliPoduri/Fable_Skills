# SOURCES.md — source manifest

Every normative claim in this skill traces to a source below. Never rely on
model memory alone (risk R6).

| Standard / source | Exact version | Official URL | Last verified | Offline fallback |
|---|---|---|---|---|
| OWASP Top 10 | 2025 | https://owasp.org/Top10/2025/ | 2026-07-06 | All ten categories with code-level indicators distilled in references/owasp-top10-2025.md |
| OWASP Application Security Verification Standard (ASVS) | 5.0.0 | https://github.com/OWASP/ASVS/tree/v5.0.0 | 2026-07-06 | Code-relevant checkpoints per chapter (V1–V17) distilled in references/asvs-checkpoints.md |
| CWE Top 25 Most Dangerous Software Weaknesses | 2025 edition | https://cwe.mitre.org/top25/archive/2025/2025_cwe_top25.html | 2026-07-06 | Full ranked list with review indicators distilled in references/cwe-top25-2025.md |
| OWASP Code Review Guide | 2.0 (2017) — HISTORICAL ONLY | https://owasp.org/www-project-code-review-guide/ | 2026-07-06 | Not distilled. Demoted to historical context; never cited as current guidance in findings. |

Verification notes (2026-07-06):

- OWASP Top 10:2025 page fetched; the ten category IDs/names in
  references/owasp-top10-2025.md match the live page (A01 Broken Access
  Control ... A10 Mishandling of Exceptional Conditions).
- ASVS v5.0.0 confirmed as the latest stable tag on github.com/OWASP/ASVS
  (released at Global AppSec EU 2025); chapter list V1–V17 fetched from the
  v5.0.0 tag.
- CWE Top 25 current edition confirmed as the 2025 list (released with
  CISA, 2025-12-11; analysis window June 2024–June 2025); the full ranked
  list in references/cwe-top25-2025.md was fetched from the archive page.
