---
name: api-designer
description: Designs HTTP/REST APIs — resources, methods, status codes, versioning, pagination, RFC 9457 errors, idempotency, OpenAPI 3.2. Use this skill when asked to design an API or write an OpenAPI spec. Do not use for data modeling; use data-modeler instead. Also covers API error format, filtering, and sorting conventions. Do not use for security requirements gates (use security-requirements-writer) or design-stage threat analysis (use threat-modeler).
metadata:
  version: "1.0.0"
  last-verified: "2026-07-06"
---

# API Designer

Design an HTTP/REST API from a feature description or an existing system:
model the resources, assign methods and status codes per RFC 9110, pick a
versioning strategy, define pagination/filtering/sorting conventions, specify
errors as RFC 9457 problem details, state idempotency guarantees, and deliver
an OpenAPI 3.2.0 skeleton the team can grow into the full contract.

## Constraints

Assume no external internet access, no paid tools, and English output.
Never send project code or data to external services.
Stay technology-agnostic: do not assume a specific framework, gateway, or
cloud provider unless the user names one.
Design the contract only. Do not design database schemas or storage layouts
(data-modeler), write security requirements (security-requirements-writer),
or enumerate design threats (threat-modeler).
Base every method, status-code, and error-format decision on the distilled
references in this skill, not on memory of other styles.

## Workflow

1. **Clarify scope.** From the request (and any code or docs provided),
   list: the consumers (browser app, mobile, service-to-service, third
   parties), the core domain operations, expected read/write ratio, and any
   existing API conventions in the project. Ask only when a choice would
   change the contract (e.g. public vs internal API); otherwise record an
   assumption in the output.
2. **Model resources.** Turn domain operations into nouns. For each
   resource decide: collection or singleton, identifier format, parent
   relationships (nest at most one level: `/stores/{storeId}/orders`), and
   which fields are server-owned (id, timestamps) vs client-writable. Name
   collections with plural nouns, lowercase, hyphenated
   (`/purchase-orders`). Express actions that do not map to CRUD as
   sub-resources or verbs on a resource (`POST /orders/{id}/cancellation`
   or `POST /orders/{id}:cancel` — pick one style and apply it everywhere).
3. **Assign methods and status codes.** Load `references/rest-conventions.md`
   and apply its method table: GET (read, safe), PUT (full replace,
   idempotent), PATCH (partial update, not idempotent by default), POST
   (create/process), DELETE (remove, idempotent). Give every endpoint its
   success code (200/201/202/204) and its expected error codes (400, 401,
   403, 404, 409, 422, 429, 500 as applicable). Never invent status codes;
   never tunnel everything through POST + 200.
4. **Pick a versioning strategy.** Choose URI-path versioning (`/v1/...`)
   unless the project already uses header or media-type versioning. State
   the compatibility rule: additive changes (new fields, new endpoints) do
   not bump the version; breaking changes (removing/renaming fields,
   changing types or semantics) require a new major version and a
   deprecation window. Record the chosen rule in the output.
5. **Define pagination, filtering, sorting.** Default to cursor-based
   pagination (`?cursor=` + `?limit=`, response carries `next_cursor`);
   use offset pagination (`?offset=&limit=`) only when the client needs
   random page access and the collection is small. Filtering: one query
   parameter per field (`?status=open&created_after=...`). Sorting:
   `?sort=field` and `?sort=-field` for descending, comma-separated for
   multiple keys. Document the maximum `limit` and the default.
6. **Specify the error contract.** Load `references/problem-details.md`.
   Every 4xx/5xx response body is `application/problem+json` per RFC 9457
   with `type`, `title`, `status`, `detail`, `instance`, plus extension
   members for machine-readable specifics (e.g. `errors[]` for field
   validation). Define the `type` URI namespace even if the URIs are not
   dereferenceable (they identify, not locate). Never leak stack traces or
   internal identifiers in `detail`.
7. **State idempotency and concurrency rules.** GET/PUT/DELETE are
   idempotent by definition — say so per endpoint. For POST endpoints where
   a retry must not duplicate work (payments, order creation), require an
   `Idempotency-Key` request header and define the replay behavior (same
   key + same body → same response; same key + different body → 422).
   For lost-update protection on PUT/PATCH, require `ETag` + `If-Match`
   and return 412 on mismatch.
8. **Produce the OpenAPI 3.2.0 skeleton.** Load
   `references/openapi-skeleton.md` and emit a valid `openapi: 3.2.0`
   document: `info`, `servers`, `tags`, 2–4 representative `paths` fully
   fleshed out (parameters, request/response schemas, problem+json error
   responses), shared `components/schemas` including a reusable `Problem`
   schema, and `components/responses` for the common errors. Cover the
   remaining endpoints as path stubs with a `TODO` description rather than
   omitting them.
9. **Self-check.** Walk the Checklist below. Fix gaps before presenting.

## Output template

Produce a single API design document with exactly these headings:

```markdown
# API Design: <system name>

## Overview
<Purpose, consumers, versioning strategy, base URL pattern. Assumptions made.>

## Resource model
<Resource list: name, identifier, parent, brief field notes.>

## Endpoints
| Method | Path | Purpose | Success | Key errors | Idempotent |
|---|---|---|---|---|---|

## Conventions
### Pagination
### Filtering and sorting
### Errors (RFC 9457)
<The Problem shape, the type URI namespace, one worked example per error class.>
### Idempotency and concurrency

## OpenAPI 3.2.0 skeleton
<The YAML document in a fenced code block.>

## Open questions
<Decisions deferred to the team, each with the recommended default.>
```

## Review mode

When asked to review or clean up an EXISTING API design instead of creating
one, run the same workflow as a critique:

1. Map the current endpoints into the Endpoints table format.
2. Flag violations against the references — verbs in paths, tunneling
   through POST, 200-with-error bodies, missing pagination caps, ad-hoc
   error shapes, missing idempotency on retryable POSTs.
3. Propose the corrected contract side by side; mark each change as
   breaking or non-breaking under the project's versioning rule.
4. Deliver in the same Output template, with a `### Findings` subsection
   added under Overview listing each violation and its fix.

## References (load on demand)

- `references/SOURCES.md` — source manifest; consult when citing or
  re-verifying any standard.
- `references/rest-conventions.md` — load at step 2–5: resource naming,
  method/status-code tables, versioning, pagination/filtering/sorting.
- `references/problem-details.md` — load at step 6: RFC 9457 member
  definitions, extension rules, worked examples.
- `references/openapi-skeleton.md` — load at step 8: OpenAPI 3.2.0
  structure, minimal valid skeleton, Problem schema component.

## Checklist

- [ ] Every endpoint has a method, success status, and error statuses from
      the tables in references/rest-conventions.md — no invented codes.
- [ ] Resource names are plural nouns, nesting is at most one level, and
      non-CRUD actions follow one consistent style.
- [ ] Versioning strategy and breaking-change rule are stated explicitly.
- [ ] Pagination, filtering, and sorting parameters are defined with
      defaults and maximums.
- [ ] All 4xx/5xx bodies are application/problem+json with the five RFC 9457
      members; at least one worked error example is shown.
- [ ] POST endpoints that must not duplicate on retry specify
      Idempotency-Key behavior; PUT/PATCH specify ETag/If-Match or state why
      not needed.
- [ ] The OpenAPI skeleton says `openapi: 3.2.0`, parses as YAML, and
      includes a reusable Problem schema.
- [ ] Output follows the Output template headings exactly.
- [ ] No database schema, security requirements list, or threat enumeration
      included — those belong to data-modeler, security-requirements-writer,
      and threat-modeler.
