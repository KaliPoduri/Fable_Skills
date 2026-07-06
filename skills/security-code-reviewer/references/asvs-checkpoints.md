# OWASP ASVS 5.0.0 — code-relevant checkpoints

Source: OWASP Application Security Verification Standard v5.0.0,
https://github.com/OWASP/ASVS/tree/v5.0.0 (chapter structure V1–V17
verified 2026-07-06). This file distills the chapters into checkpoints a
code reviewer can verify by reading source. Design/process-only
requirements are omitted. Requirement numbering below refers to chapters,
not individual ASVS requirement IDs — cite findings by CWE, not by ASVS ID.

## V1 Encoding and Sanitization
- Output encoding matches the target context (HTML body vs attribute vs
  JS vs URL vs CSS); encoding happens at output time, not storage time.
- Sanitization of rich content uses a maintained allow-list sanitizer.
- Canonicalize (decode, normalize Unicode/percent-encoding) BEFORE
  validating or using data in security decisions; decode only once.
- Injection defenses are parameterization-first; escaping is the fallback.

## V2 Validation and Business Logic
- Positive (allow-list) validation on type, length, range, and format at
  the trust boundary — server-side, regardless of client checks.
- Business rules enforce order and limits (steps cannot be skipped,
  quantities/prices cannot go negative, server recomputes totals).
- Anti-automation on abusable flows: rate limits, quotas, idempotency.

## V3 Web Frontend Security
- Cookies carrying session/auth: Secure, HttpOnly, SameSite set.
- CSRF defense present on state-changing requests (token or SameSite
  strategy applied consistently).
- Security headers set by the app where not platform-provided: CSP,
  X-Content-Type-Options: nosniff, frame-ancestors/clickjacking defense.
- No sensitive data placed in localStorage when cookies with HttpOnly
  would do; postMessage handlers verify origin.

## V4 API and Web Service
- Every API route enforces authn/authz server-side; no "internal-only by
  obscurity" endpoints.
- HTTP methods restricted per route; content-type validated before
  parsing bodies.
- Batch/GraphQL-style interfaces bound query depth/cost; no mass
  assignment (bind only allow-listed fields to models).

## V5 File Handling
- Uploads: validate type by content, cap size, store outside web root or
  in object storage with generated (not user-supplied) names.
- Downloads/paths: canonicalize then enforce base-directory prefix; no
  user input in filesystem paths without allow-listing.
- Archives extracted with entry-count, size, and path checks (zip-slip,
  zip bombs).

## V6 Authentication
- Passwords: dedicated password hashing (argon2/scrypt/bcrypt/PBKDF2)
  with per-user salt; no truncation; breached/weak-password checks where
  available offline.
- No default, hardcoded, or shared credentials in code or config.
- Login failures give a uniform error; throttling/lockout server-side.
- Credential comparison in constant time.
- Reset/verification tokens: CSPRNG, single-use, expiring, delivered out
  of band, never logged.

## V7 Session Management
- Session tokens from a CSPRNG, ≥128 bits entropy, opaque to the client.
- Session regenerated on login and privilege change; invalidated
  server-side on logout and timeout.
- Absolute and idle timeouts appropriate to sensitivity.

## V8 Authorization
- Deny by default; checks at the controller/service layer, not the view.
- Object-level (record ownership/tenant) checks on every read AND write.
- Field-level authorization for sensitive attributes (role, price,
  status) — no mass assignment of protected fields.
- Authorization decisions re-validated server-side per request, never
  cached from client-supplied state.

## V9 Self-contained Tokens (JWT etc.)
- Signature verified with an allow-listed algorithm; `none` rejected;
  key/algorithm confusion prevented (no HS256-with-public-key tricks).
- exp/nbf/aud/iss validated; token lifetime short; revocation strategy
  exists for logout/compromise.
- No secrets or sensitive PII inside token claims.

## V10 OAuth and OIDC
- Authorization code flow with PKCE for public clients; no implicit flow.
- redirect_uri validated by exact match; state parameter verified.
- Tokens validated for audience and issuer; access tokens never in URLs.

## V11 Cryptography
- Vetted library implementations only; no custom primitives or modes.
- AEAD modes (e.g., AES-GCM) with unique nonces; no ECB; no static IVs.
- MD5/SHA-1/DES/RC4 absent from security paths.
- CSPRNG for all security-relevant randomness.
- Key management: keys not hardcoded; rotation possible; separate keys
  per purpose.

## V12 Secure Communication
- TLS enforced in client code (no verify=False / trust-all managers /
  hostname verification disabled).
- Internal service-to-service calls also encrypted/authenticated where
  the platform does not guarantee it.

## V13 Configuration
- Secrets sourced from vault/environment injection, not source control.
- Debug features, sample apps, and verbose errors disabled in production
  paths; feature flags fail closed for security features.
- Dependencies pinned; unused services/endpoints removed.

## V14 Data Protection
- Sensitive data classified and minimized; not cached or logged
  unnecessarily; masked in UI and logs.
- Sensitive data not in URLs/query strings; no-store/no-cache headers on
  sensitive responses.
- Deletion/retention paths actually remove data.

## V15 Secure Coding and Architecture
- Memory-safe APIs preferred; bounds-checked operations in native code.
- Integer overflow checked where sizes/prices/counters are computed.
- Concurrency: shared state guarded; check-and-use made atomic (no
  TOCTOU); no security decisions on racy reads.
- Third-party components used through maintained, supported versions
  (CVE confirmation itself → dependency-auditor).

## V16 Security Logging and Error Handling
- Security events (login success/failure, lockout, privilege change,
  sensitive data access) logged with actor, action, timestamp.
- Logs free of secrets/tokens/passwords and encoded against injection.
- Errors fail closed; generic messages to clients; details server-side.
- Last-resort handler catches unexpected errors (no raw stack traces).

## V17 WebRTC
Only when the app ships WebRTC media/signaling code:
- Signaling authenticated; DTLS-SRTP enforced; TURN credentials
  short-lived; no long-term credentials in client code.
