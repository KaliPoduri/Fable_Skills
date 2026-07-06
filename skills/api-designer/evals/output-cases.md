# Output eval cases (≥3)

Each case is run twice — WITH the skill installed and WITHOUT (raw
assistant) — and scored against the rubric in
docs/AUTHORING-GUIDE.md §Eval thresholds. The skill must beat raw output.

## Case 1

- Prompt: "Design a REST API for a library lending system: members borrow
  and return books, librarians manage the catalog, and we need overdue
  reports."
- Input artifacts (if any): none.
- Rubric focus: template compliance, completeness, source accuracy.
- Expected qualities: follows the Output template headings exactly;
  plural-noun resources with at most one nesting level; endpoint table with
  method, success code, error codes, and idempotency column; a stated
  versioning strategy with breaking-change rule; cursor pagination with
  documented limit defaults; errors specified as application/problem+json
  with the five RFC 9457 members and at least one worked example; an
  `openapi: 3.2.0` YAML skeleton with a reusable Problem schema; open
  questions listed with recommended defaults.

## Case 2

- Prompt: "Our API returns errors as `{ \"success\": false, \"msg\": \"...\" }`
  with HTTP 200. Define a proper error format and show what the validation
  and rate-limit responses should look like."
- Input artifacts (if any): the ad-hoc error shape above.
- Rubric focus: source accuracy (RFC 9457), actionability.
- Expected qualities: rejects 200-with-error explicitly; proposes
  application/problem+json with type/title/status/detail/instance; defines
  a `type` URI namespace and explains URIs identify rather than locate;
  shows a 422 example with an `errors[]` extension (pointer + message) and
  a 429 example with retryAfterSeconds plus the Retry-After header; warns
  against clients parsing `detail`.

## Case 3

- Prompt: "We have POST /createOrder, POST /getOrder, POST /updateOrder,
  POST /deleteOrder — all return 200. Clean this up and make order creation
  safe to retry."
- Input artifacts (if any): the four RPC-style endpoints above.
- Rubric focus: source accuracy (RFC 9110 method/status discipline),
  completeness, actionability.
- Expected qualities: remaps to GET/POST/PUT-or-PATCH/DELETE on /orders and
  /orders/{id} with correct success codes (200/201/204) and Location header
  on create; states idempotency per method; adds Idempotency-Key semantics
  for POST /orders including replay and same-key-different-body → 422
  behavior; recommends ETag/If-Match with 412 for updates.
