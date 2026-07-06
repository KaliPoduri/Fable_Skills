# OWASP Top 10:2025 — distilled for code review

Source: OWASP Top 10:2025, https://owasp.org/Top10/2025/ (category IDs and
names verified 2026-07-06). Indicators below are the code-level review
translation of each category for this skill; CWE mappings use the 2025 CWE
Top 25 (see cwe-top25-2025.md).

Walk every applicable category against the code under review. For each
indicator that fires, trace source-to-sink before reporting.

## A01:2025 — Broken Access Control

The application fails to enforce who may do what to which object.

Code-level indicators:
- Handlers that fetch or mutate a record by an ID taken from the request
  with no ownership/tenant check (IDOR; CWE-639, CWE-862).
- Authorization enforced only in the UI or client code, not on the server
  endpoint.
- Role checks done by string comparison against user-supplied fields
  (header, cookie, hidden form field, JWT claim accepted unverified).
- Missing authorization on "secondary" routes: exports, admin APIs,
  webhooks, internal endpoints exposed by the same router (CWE-862,
  CWE-863, CWE-284).
- Path traversal: file paths built from user input without
  canonicalization + allow-list ("../" reaching outside the intended
  directory; CWE-22).
- CORS configured with wildcard origin plus credentials.
- Method-based bypass: authz applied to GET but not PUT/DELETE on the same
  resource.

Fix direction: deny by default; enforce object-level checks server-side in
one shared layer; canonicalize paths then verify prefix; never trust
client-asserted roles.

## A02:2025 — Security Misconfiguration

Insecure defaults or settings left in code and config.

Code-level indicators:
- Debug mode, verbose error pages, or development endpoints reachable in
  production code paths.
- Default credentials or sample accounts left enabled.
- Security headers not set where the framework requires explicit opt-in
  (CSP, X-Content-Type-Options, HSTS).
- Overly permissive framework settings: directory listing, permissive
  file permissions written by the code, disabled CSRF protection,
  `verify=False` / disabled TLS certificate validation.
- XML parsers configured with external entity resolution enabled (XXE).
- Cloud/container config in repo granting wildcard permissions.

Fix direction: production-safe defaults in code, explicit hardening of
parsers and HTTP clients, fail closed when config is missing.

## A03:2025 — Software Supply Chain Failures

Compromise or weakness entering through dependencies, build, or
distribution.

Code-level indicators (what is visible in a code review):
- Dependencies pulled from unpinned or mutable references (floating
  versions, git URLs at HEAD, curl-pipe-to-shell in build scripts).
- Lockfiles absent or ignored; checksums/signatures not verified for
  downloaded artifacts.
- Build scripts executing code from untrusted sources; postinstall hooks
  doing network fetches.
- Vendored code modified without provenance notes.

Boundary: confirming whether a specific dependency version carries a live
CVE is OUT OF SCOPE offline — hand to dependency-auditor. Report only what
the code/build files show.

## A04:2025 — Cryptographic Failures

Wrong, weak, or missing cryptography for data that needs protection.

Code-level indicators:
- Home-rolled crypto or custom "encoding as encryption" (Base64, XOR).
- Weak primitives: MD5/SHA-1 for security purposes, DES/3DES/RC4, RSA
  without OAEP, ECB mode anywhere, static or reused IVs/nonces (CWE-327
  family; not in Top 25 2025 but still assign the correct CWE).
- Passwords hashed with fast hashes (plain SHA-256, MD5) instead of a
  dedicated password hash (argon2, scrypt, bcrypt, PBKDF2).
- Non-cryptographic RNG (`random`, `Math.random`, `rand()`) used for
  tokens, session IDs, password resets, or keys.
- Secrets/PII stored or transmitted in plaintext; TLS optional or
  downgradable in client code.
- Keys or IVs hardcoded in source (also report under secrets).

Fix direction: platform-vetted crypto APIs, modern AEAD modes
(e.g., AES-GCM with unique nonces), dedicated password hashing with
per-user salt, CSPRNG for anything security-relevant.

## A05:2025 — Injection

Untrusted data interpreted as code or commands by an interpreter. Includes
XSS.

Code-level indicators:
- SQL/NoSQL built by string concatenation or interpolation of request
  data (CWE-89). ORMs are not automatically safe: raw fragments,
  `WHERE` strings, order-by column names from input.
- OS command execution with shell=true or string-built commands
  (CWE-78, CWE-77).
- Dynamic code evaluation of user input: eval/exec, template injection in
  server-side template engines (CWE-94).
- LDAP/XPath/regex built from input without escaping.
- XSS: request data written into HTML/JS/attributes without context-aware
  output encoding; `innerHTML`/`dangerouslySetInnerHTML`/`v-html` with
  user content; unsanitized markdown-to-HTML (CWE-79).

Fix direction: parameterized queries everywhere; argument-vector process
execution (no shell); auto-escaping template engines with encoding chosen
per output context; sanitize HTML with a maintained allow-list sanitizer
only when rich text is truly required.

## A06:2025 — Insecure Design

Missing or ineffective control design — the flaw exists even in a perfect
implementation.

Code-level indicators (report what code reveals; full design analysis is
threat-modeler's job):
- Security-relevant business logic without limits: unlimited retries,
  no rate limiting on auth or expensive operations (CWE-770), unbounded
  resource allocation from user input.
- Trust decisions based on client-controlled state (price, role, quota
  computed client-side and accepted).
- Recovery/secondary flows weaker than primary flows (password reset via
  guessable questions, admin backdoor parameters).

Boundary: if the fix requires re-architecting a flow rather than editing
code, record the finding and hand off to threat-modeler.

## A07:2025 — Authentication Failures

Identity confirmation, session issuance, and credential handling broken.

Code-level indicators:
- Missing authentication on functions that need it (CWE-306): internal
  or "hidden" endpoints, health/debug routes exposing data.
- Credential comparison vulnerable to timing attacks (== on secrets).
- Session IDs/tokens that are predictable, long-lived without rotation,
  not invalidated on logout or privilege change.
- Session fixation: session not regenerated at login.
- Password policy enforced client-side only; no brute-force lockout or
  throttling on login endpoints.
- Remember-me/reset tokens stored or logged in plaintext, or generated
  with non-CSPRNG.
- JWTs accepted with `alg: none`, unverified signatures, or no expiry
  check.

Fix direction: framework auth middleware on every protected route,
constant-time comparison, CSPRNG tokens with expiry + one-time use,
regenerate session on privilege change.

## A08:2025 — Software or Data Integrity Failures

Code and data trusted without integrity verification. Includes insecure
deserialization.

Code-level indicators:
- Native deserialization of untrusted bytes: pickle, Java
  ObjectInputStream, PHP unserialize, YAML load in non-safe mode,
  BinaryFormatter (CWE-502).
- Auto-update or plugin-load mechanisms fetching code without signature
  verification.
- CI/CD or build logic in repo that executes unreviewed remote content.
- Integrity-relevant client data (signed cookies, tokens) accepted
  without verifying the signature, or signed with a hardcoded/weak key.

Fix direction: prefer data-only formats (JSON) with schema validation;
if native deserialization is unavoidable, allow-list types; verify
signatures before use.

## A09:2025 — Security Logging and Alerting Failures

The application cannot detect or reconstruct an attack — or its logs
create new exposure.

Code-level indicators:
- No audit log for logins, failures, lockouts, privilege changes,
  payments, or data exports.
- Secrets, tokens, passwords, or PII written to logs (also a data
  exposure finding, CWE-200).
- Log entries built from raw user input without encoding (log injection /
  forging).
- Exceptions swallowed silently in security-relevant paths (`catch {}`).
- Errors returned to clients with stack traces, SQL text, or internal
  paths (CWE-200).

Fix direction: structured audit events for security actions, redaction at
the logging layer, encode user input in log messages, generic client-side
error messages with server-side detail.

## A10:2025 — Mishandling of Exceptional Conditions

Error and edge paths that fail open, leak, or corrupt state.

Code-level indicators:
- Fail-open control flow: an exception in an authz/validation check leads
  to the action proceeding (return-true-on-error, missing rethrow).
- Empty or overly broad catch blocks around security checks.
- Null/absent-value paths that skip validation (CWE-476 analogues in
  managed languages: unchecked optionals feeding security decisions).
- Resource cleanup missing on error paths (locks, temp files with
  sensitive content, connections) enabling DoS (CWE-770).
- Race/TOCTOU windows: check and use of a file or record as separate
  non-atomic steps.
- Error messages that reveal which part of a credential was wrong
  (username vs password enumeration).

Fix direction: fail closed by default; narrow catches; validate the
exceptional path with the same rigor as the happy path; atomic
check-and-use operations.
