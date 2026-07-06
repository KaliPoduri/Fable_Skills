# REST conventions — methods, status codes, versioning, pagination

Distilled from RFC 9110 (HTTP Semantics, STD 97, June 2022,
https://www.rfc-editor.org/rfc/rfc9110) and RFC 5789 (PATCH, March 2010,
https://www.rfc-editor.org/rfc/rfc5789). Widely adopted REST naming and
pagination conventions are marked [convention] — they are library guidance,
not RFC requirements.

## Resource naming [convention]

- Collections: plural nouns, lowercase, hyphen-separated:
  `/purchase-orders`, `/users`.
- Item: collection + identifier: `/users/{userId}`.
- Nest at most one level for ownership: `/stores/{storeId}/orders`.
  Deeper relationships: filter on the flat collection instead
  (`/orders?storeId=...`).
- Singleton sub-resource for one-to-one data: `/users/{id}/preferences`.
- Non-CRUD actions: model as sub-resource (`POST /orders/{id}/cancellation`)
  or custom action suffix (`POST /orders/{id}:cancel`). Pick ONE style per
  API and never mix.
- No verbs in collection paths, no trailing slashes, no file extensions.

## HTTP methods (RFC 9110 §9; PATCH from RFC 5789)

| Method | Use for | Safe | Idempotent | Request body |
|---|---|---|---|---|
| GET | Read a resource or collection | Yes | Yes | No |
| HEAD | GET without body (existence, size checks) | Yes | Yes | No |
| POST | Create in a collection; process a request | No | No | Yes |
| PUT | Full replace at a known URI; create-at-URI | No | Yes | Yes |
| PATCH | Partial update (RFC 5789) | No | No | Yes |
| DELETE | Remove a resource | No | Yes | Usually no |
| OPTIONS | Capability discovery / CORS preflight | Yes | Yes | No |

Notes:
- Safe = no state change intended (RFC 9110 §9.2.1). Never mutate on GET.
- Idempotent = repeating the request has the same effect as once
  (RFC 9110 §9.2.2). Clients and proxies may retry idempotent requests
  automatically — design handlers accordingly.
- PATCH is NOT idempotent by definition (RFC 5789); it can be made
  effectively idempotent with conditional requests (`If-Match`).
- PUT replaces the entire representation. If the client sends a partial
  body with PUT, that is a design error — use PATCH.

## Status codes (RFC 9110 §15) — the working set

Success:

| Code | Meaning | Typical use |
|---|---|---|
| 200 OK | Success with body | GET, PATCH/PUT returning the resource |
| 201 Created | Resource created | POST to collection; include `Location` header |
| 202 Accepted | Queued for async processing | Long-running jobs; return a status URL |
| 204 No Content | Success, no body | DELETE; PUT/PATCH without response body |

Client errors:

| Code | Meaning | Typical use |
|---|---|---|
| 400 Bad Request | Malformed syntax / unparseable body | Broken JSON, bad parameter type |
| 401 Unauthorized | No/invalid credentials | Missing or expired token |
| 403 Forbidden | Authenticated but not allowed | Insufficient permission |
| 404 Not Found | Resource does not exist | Also use to hide existence from unauthorized callers when policy requires |
| 405 Method Not Allowed | Method not supported on this path | Include `Allow` header |
| 406 Not Acceptable | Cannot honor `Accept` header | Content negotiation failure |
| 409 Conflict | State conflict | Duplicate unique field; edit of stale resource without ETags |
| 410 Gone | Existed, permanently removed | Retired versions/resources |
| 412 Precondition Failed | `If-Match` mismatch | Optimistic concurrency violation |
| 415 Unsupported Media Type | Wrong `Content-Type` | Non-JSON body to JSON endpoint |
| 422 Unprocessable Content | Syntactically valid, semantically invalid | Field validation failures |
| 429 Too Many Requests | Rate limit hit | Include `Retry-After` header |

Server errors:

| Code | Meaning | Typical use |
|---|---|---|
| 500 Internal Server Error | Unexpected failure | Catch-all; never expose internals |
| 502 Bad Gateway | Upstream returned invalid response | Gateway/proxy layers |
| 503 Service Unavailable | Temporarily overloaded / maintenance | Include `Retry-After` |
| 504 Gateway Timeout | Upstream timed out | Gateway/proxy layers |

Rules:
- 400 = "I cannot read this"; 422 = "I can read it, but it is invalid".
- Never return 200 with an error payload inside.
- Every 4xx/5xx body is `application/problem+json` — see
  references/problem-details.md.

## Versioning [convention]

- Default: URI-path major version — `/v1/orders`. Visible, cache-friendly,
  simple to route. Alternatives (use only if the project already does):
  header (`Api-Version: 2026-07-01`) or media-type
  (`application/vnd.example.v2+json`).
- Only MAJOR versions in the path. Never `/v1.2/`.
- Additive, non-breaking (no version bump): new endpoints, new OPTIONAL
  request fields, new response fields (clients must ignore unknown fields),
  new enum values only where the contract says the enum is open.
- Breaking (new major version required): removing or renaming fields or
  endpoints, changing a field's type or meaning, tightening validation,
  changing status codes or error semantics, making an optional field
  required.
- Deprecation: announce, dual-run old and new versions for a stated window,
  signal with a `Deprecation` and `Sunset` response header where supported.

## Pagination [convention]

Cursor-based (default — stable under concurrent writes, scales):

```
GET /orders?limit=50&cursor=eyJpZCI6MTAyM30
→ 200
{ "data": [ ... ], "next_cursor": "eyJpZCI6MTA3M30", "has_more": true }
```

- `cursor` is an opaque server token — clients must not parse it.
- Last page: `next_cursor` null/absent, `has_more` false.

Offset-based (only for small, mostly-static collections needing random
page access):

```
GET /orders?limit=50&offset=100
→ 200
{ "data": [ ... ], "total": 1234, "limit": 50, "offset": 100 }
```

Both: document the default `limit`, the maximum `limit` (cap it — e.g.
200), and reject out-of-range values with 422.

## Filtering and sorting [convention]

- Filter: one query parameter per field: `?status=open&customer_id=42`.
  Ranges via suffixed parameters: `?created_after=...&created_before=...`
  (ISO 8601 timestamps).
- Multiple values: comma-separated `?status=open,pending` (documented as
  OR within a field, AND across fields).
- Sort: `?sort=created_at` ascending, `?sort=-created_at` descending,
  comma-separated for tie-breakers: `?sort=-created_at,id`.
- Whitelist filterable and sortable fields; reject unknown ones with 422
  (silently ignoring hides client bugs).

## Idempotency keys and concurrency [convention]

- For POSTs that must not duplicate on retry (payments, order creation):
  require an `Idempotency-Key` header (client-generated UUID). Server
  stores key + request hash + response for a documented retention window.
  Replay with same key and same body → return the stored response. Same
  key, different body → 422 problem.
- Optimistic concurrency: return `ETag` on reads; require `If-Match` on
  PUT/PATCH; on mismatch return 412 with a problem body telling the client
  to re-fetch.
