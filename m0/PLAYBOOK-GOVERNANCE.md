# Playbook governance (complete at M0)

Governs the error-pattern playbook that etl-assistant drafts after a
user-confirmed root cause (PLAN §5). Entries land in the KB
(`errors/<YYYY-MM>.md`) via PR only — never a silent write. Fill every
blank before Skill B (M3) ships.

## Roles

- **Playbook reviewer** (approves/rejects each entry PR): ____
- **Security owner** (signs off on anything persisted to the KB — redaction
  correctness): ____
- **Backup reviewer** (when the primary is unavailable): ____

## Entry schema (what etl-assistant drafts)

Each entry carries: date · job · symptom / error pattern · confirmed cause ·
fix · verification evidence · redaction-check done. Missing any field →
entry is not eligible to merge.

## Approval criteria (all must hold to merge)

- [ ] Root cause was **confirmed** (not a guess) by the reporting dev.
- [ ] Evidence cited (file:line or runtime observation); excerpts ≤10 lines.
- [ ] Redaction check done — no secrets, tokens, customer identifiers, or
      raw row values (content-based, PLAN §7). Security owner confirms.
- [ ] Fix is advise-only; no production change was made by the tool.

## Disputed-cause handling

- If reviewers disagree on the cause: the entry **stays out**, OR lands
  explicitly **marked contested** with the competing explanations recorded.
  Never merge a disputed cause as settled fact. Chosen policy: ____
  (stay-out / land-marked-contested).

## Redaction / security

- Anything persisted is stripped of data values regardless of length (line
  caps are brevity rules, not privacy controls).
- Security owner (above) is the named accountable person for persisted
  content.

## Change log

- Governance completed on: ____  by: ____
