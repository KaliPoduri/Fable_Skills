# RFC 9457 — Problem Details for HTTP APIs (distilled)

Source: RFC 9457, July 2023, Proposed Standard, obsoletes RFC 7807.
https://www.rfc-editor.org/rfc/rfc9457 (verified 2026-07-06).

## What it is

A standard machine-readable error body for HTTP APIs. Media types:
`application/problem+json` (use this) and `application/problem+xml`.
Every 4xx/5xx response carries a problem details object; the HTTP status
code and the body must agree.

## Members (all optional, all top-level)

| Member | Type | Meaning | Rules |
|---|---|---|---|
| `type` | string (URI reference) | Identifies the problem TYPE (the class of error) | Defaults to `about:blank` when absent. The URI is an identifier first — it SHOULD resolve to human docs, but consumers must not need to dereference it. Compare as opaque strings. |
| `title` | string | Short human-readable summary of the type | Same wording for every occurrence of the same `type`; do not vary per request. |
| `status` | number | The HTTP status code for this occurrence | Advisory copy of the response status; must match it. |
| `detail` | string | Human-readable explanation of THIS occurrence | For humans, not for parsing. Never include stack traces, SQL, or internal hostnames. |
| `instance` | string (URI reference) | Identifies this specific occurrence | E.g. a per-request URI (`/errors/3f1b...`) usable in support tickets and log correlation. |

## Extension members

Add any additional top-level members for machine-readable specifics —
consumers ignore unknown members. Define each extension in the API docs.
The canonical validation-error pattern:

```json
{
  "type": "https://api.example.com/problems/validation-error",
  "title": "Request failed validation",
  "status": 422,
  "detail": "2 fields are invalid.",
  "instance": "/errors/9d3f8c1a",
  "errors": [
    { "pointer": "/email", "message": "must be a valid email address" },
    { "pointer": "/age",   "message": "must be >= 0" }
  ]
}
```

Rules for extensions:
- Machine-readable data goes in extensions — never make clients parse
  `detail`.
- Keep extension member names consistent across the whole API
  (`errors[]` with `pointer` + `message` everywhere, not `fields[]` in one
  endpoint and `violations[]` in another).

## The `type` namespace

- Reserve one URI prefix for the API, e.g.
  `https://api.example.com/problems/<slug>`. In-org/offline these need not
  be dereferenceable — they identify, not locate.
- One `type` per distinct error CLASS the client might branch on:
  `validation-error`, `insufficient-funds`, `rate-limit-exceeded`,
  `stale-version`. Do not mint a type per endpoint.
- Generic transport-level errors with nothing to add beyond the status
  code may use `about:blank` + the status's standard reason phrase as
  `title`.

## Worked examples per error class

401 (no extension needed):

```json
{ "type": "about:blank", "title": "Unauthorized", "status": 401,
  "detail": "Access token is expired." }
```

409 business conflict (domain-specific type + extension):

```json
{
  "type": "https://api.example.com/problems/duplicate-sku",
  "title": "SKU already exists",
  "status": 409,
  "detail": "A product with SKU 'AB-123' already exists in store 42.",
  "instance": "/errors/51c9aa02",
  "conflictingResourceId": "prod_8871"
}
```

429 with retry guidance (also set the `Retry-After` header):

```json
{
  "type": "https://api.example.com/problems/rate-limit-exceeded",
  "title": "Rate limit exceeded",
  "status": 429,
  "detail": "Limit is 100 requests per minute.",
  "retryAfterSeconds": 31
}
```

## Anti-patterns to reject

- `200 OK` with `{ "success": false, "error": ... }` — status code must
  carry the outcome.
- A bare string body or ad-hoc `{ "message": "..." }` shape for errors.
- Different error shapes on different endpoints of the same API.
- Stack traces, ORM messages, or internal service names in `detail`.
- Clients switching behavior on `title` or `detail` text — they must
  switch on `type` (and `status`).

## Reusable OpenAPI `Problem` schema

```yaml
Problem:
  type: object
  properties:
    type:
      type: string
      format: uri-reference
      default: "about:blank"
    title:
      type: string
    status:
      type: integer
      minimum: 100
      maximum: 599
    detail:
      type: string
    instance:
      type: string
      format: uri-reference
  additionalProperties: true   # extension members allowed
```
