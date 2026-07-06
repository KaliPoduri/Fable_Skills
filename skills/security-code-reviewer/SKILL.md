---
name: security-code-reviewer
description: Reviews code for security vulnerabilities per OWASP Top 10:2025, ASVS 5.0.0, and CWE Top 25 (2025). Use this skill when asked to security review code or find injection, XSS, SSRF, crypto misuse, or secrets. Do not use for design-stage threat modeling; use threat-modeler instead. General code review belongs to code-reviewer, dependency CVEs to dependency-auditor, LLM-app risks to llm-app-security-reviewer.
metadata:
  version: "1.0.0"
  last-verified: "2026-07-06"
---

# Security Code Reviewer

Review written code for exploitable weaknesses and fix them. Ground every
finding in OWASP Top 10:2025, OWASP ASVS 5.0.0 code-relevant checkpoints,
and the 2025 CWE Top 25. Produce numbered findings (SEC-1, SEC-2, ...) with
severity, CWE ID, the vulnerable pattern, and a concrete fix — this is a
defensive review whose deliverable is fixed code, not just a list of
problems.

## Constraints

Assume no external internet access, no paid tools, and English output.
Never send project code or data to external services.
This skill CANNOT confirm live CVEs offline — never claim a dependency is
or is not vulnerable to a specific CVE; hand that to dependency-auditor.
Never weaken or remove existing security controls while fixing a finding.
Cite CWE IDs and OWASP categories only from the reference files in this
skill, not from memory.
Do not cite the OWASP Code Review Guide (2017) as current guidance; it is
historical context only.

## Workflow

1. **Scope the review.** List the files or diff under review. Ask for the
   language/framework only if it is not evident from the code. Note
   anything explicitly out of scope (third-party libraries, generated
   code, infrastructure).
2. **Map trust boundaries.** Identify where untrusted data enters
   (HTTP parameters, headers, cookies, file uploads, message queues,
   environment, database reads of user-controlled content) and where
   sensitive actions happen (auth checks, DB queries, OS calls, file I/O,
   outbound requests, deserialization, crypto, logging).
3. **Sweep by category.** Load `references/owasp-top10-2025.md` and walk
   every applicable category against the code. Check at minimum:
   - Injection: SQL/NoSQL/OS command/LDAP/template/code injection and XSS.
   - Authentication: password handling, credential comparison, MFA hooks,
     session issuance, brute-force controls.
   - Authorization: missing or object-level checks (IDOR), user-controlled
     keys, privilege escalation paths, path traversal.
   - Cryptography: weak or home-rolled algorithms, ECB mode, static IVs,
     non-cryptographic RNG for security decisions, plaintext storage of
     secrets or PII.
   - Secrets in code: hardcoded passwords, API keys, tokens, connection
     strings, private keys — in source, config, tests, and comments.
   - Input validation at trust boundaries: type, length, range, allow-list
     checks; canonicalization before validation.
   - SSRF: outbound requests built from user input without allow-listing.
   - Insecure deserialization: native deserializers fed untrusted bytes.
   - Logging/error handling: secrets or PII in logs, missing audit events
     for security actions, swallowed exceptions, fail-open error paths,
     stack traces returned to clients.
4. **Cross-check CWE.** For each suspected issue, match it to a CWE ID
   using `references/cwe-top25-2025.md`. If the weakness is real but not
   in the Top 25, still assign the correct CWE ID and say it is outside
   the Top 25.
5. **Verify exploitability before reporting.** Trace the data flow from
   source to sink. If a framework or upstream check already neutralizes
   the input, either drop the finding or report it as Low
   (defense-in-depth) and say why. Do not report pattern matches you have
   not traced.
6. **Assign severity.**
   - Critical: remotely exploitable, no auth required, full data or
     system compromise (e.g., unauthenticated SQL injection, RCE via
     deserialization).
   - High: exploitable with low effort or valid account; significant data
     exposure or privilege escalation.
   - Medium: exploitable under specific conditions, or a broken control
     with limited blast radius.
   - Low: defense-in-depth gap, hard-to-reach path, or hygiene issue.
7. **Write the fix.** For every finding give corrected code (or an exact
   change description when the fix spans many call sites) using the
   safe pattern: parameterized queries, context-aware output encoding,
   allow-list validation, vetted crypto APIs, secret references from a
   vault or environment injection, safe deserialization formats.
   Apply the fixes if the user asked for fixes; otherwise deliver them in
   the report.
8. **Report.** Emit the Output template below. Order findings by severity,
   then by file. State explicitly what was NOT covered (dependencies,
   runtime config, design) and which sibling skill owns each gap.

## Output template

```markdown
# Security Code Review — <repo/module/diff name>

## Scope
- Reviewed: <files or diff>
- Trust boundaries: <entry points found>
- Not covered: dependency CVEs (dependency-auditor), design-level threats
  (threat-modeler), <anything else skipped>

## Findings

### SEC-1: <short title>
- **Severity:** Critical | High | Medium | Low
- **CWE:** CWE-<n> (<name>)
- **OWASP:** A<xx>:2025 <category>
- **Location:** <path/file:line>
- **Vulnerable pattern:**
  ```<lang>
  <minimal offending snippet>
  ```
- **Fix:**
  ```<lang>
  <corrected snippet>
  ```
  <one or two sentences: why this fix closes the hole>

### SEC-2: ...

## Summary
| ID | Severity | CWE | Location | Fixed? |
|---|---|---|---|---|

## Residual risk and hand-offs
- <open items and which sibling skill or human owns them>
```

If zero findings survive step 5, say so explicitly, list the categories
checked, and still include Scope and Residual risk sections. Absence of
findings is not a certification of security.

## References (load on demand)

- `references/SOURCES.md` — source manifest (always present).
- `references/owasp-top10-2025.md` — load at step 3 for every review; the
  category-by-category indicator list.
- `references/cwe-top25-2025.md` — load at step 4 to assign CWE IDs and
  ranks.
- `references/asvs-checkpoints.md` — load when the review covers
  authentication, session management, authorization, crypto, or logging
  in depth, or when the user asks for an ASVS-aligned review.

## Checklist

- [ ] Every trust boundary identified in step 2 was swept in step 3.
- [ ] Every finding has SEC-<n>, severity, CWE ID, OWASP category,
      location, vulnerable snippet, and a concrete fix.
- [ ] Every finding's data flow was traced (step 5) — no untraced pattern
      matches reported.
- [ ] No claim about live CVEs or dependency vulnerability status.
- [ ] Secrets found were redacted in the report (never echo full values).
- [ ] Residual risk section names the sibling-skill hand-offs.
- [ ] Output follows the template above.
