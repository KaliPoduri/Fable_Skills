# OpenAPI 3.2.0 skeleton (distilled)

Source: OpenAPI Specification v3.2.0, published 2025-09-19,
https://spec.openapis.org/oas/v3.2.0.html (verified 2026-07-06 via
https://spec.openapis.org/oas/latest.html).

## Document rules

- Root field `openapi: 3.2.0` (exact string). `info.title` and
  `info.version` (the API's own version, not the OAS version) are
  required. At least one of `paths`, `components`, or `webhooks` must be
  present.
- `servers` lists base URLs; put the major version in the URL when using
  path versioning (`https://api.example.com/v1`).
- Reuse everything shared via `components` and `$ref` — schemas,
  parameters, responses, headers, securitySchemes.
- `operationId` unique per operation; `tags` group operations per
  resource.
- 3.2 additions worth knowing: the `query` HTTP method for
  safe-with-body queries, `additionalOperations` for non-standard
  methods, and `tags` gained `summary`/`parent` for hierarchy. Use plain
  standard methods unless the design needs these.

## Minimal valid skeleton (adapt, keep structure)

```yaml
openapi: 3.2.0
info:
  title: Orders API
  version: 1.0.0
  description: Order management for Example Corp.
servers:
  - url: https://api.example.com/v1
tags:
  - name: orders
    description: Order lifecycle
paths:
  /orders:
    get:
      operationId: listOrders
      tags: [orders]
      summary: List orders
      parameters:
        - $ref: '#/components/parameters/Limit'
        - $ref: '#/components/parameters/Cursor'
        - name: status
          in: query
          schema:
            type: string
            enum: [open, shipped, cancelled]
      responses:
        '200':
          description: A page of orders
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/Order'
                  next_cursor:
                    type: [string, 'null']
                  has_more:
                    type: boolean
        '422':
          $ref: '#/components/responses/ValidationProblem'
        default:
          $ref: '#/components/responses/Problem'
    post:
      operationId: createOrder
      tags: [orders]
      summary: Create an order
      parameters:
        - name: Idempotency-Key
          in: header
          required: true
          schema:
            type: string
            format: uuid
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/OrderCreate'
      responses:
        '201':
          description: Order created
          headers:
            Location:
              schema:
                type: string
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Order'
        '422':
          $ref: '#/components/responses/ValidationProblem'
        default:
          $ref: '#/components/responses/Problem'
  /orders/{orderId}:
    parameters:
      - name: orderId
        in: path
        required: true
        schema:
          type: string
    get:
      operationId: getOrder
      tags: [orders]
      summary: Get one order
      responses:
        '200':
          description: The order
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Order'
        '404':
          $ref: '#/components/responses/Problem'
components:
  parameters:
    Limit:
      name: limit
      in: query
      schema:
        type: integer
        minimum: 1
        maximum: 200
        default: 50
    Cursor:
      name: cursor
      in: query
      schema:
        type: string
  schemas:
    Order:
      type: object
      required: [id, status, created_at]
      properties:
        id:
          type: string
        status:
          type: string
          enum: [open, shipped, cancelled]
        created_at:
          type: string
          format: date-time
    OrderCreate:
      type: object
      required: [items]
      properties:
        items:
          type: array
          minItems: 1
          items:
            type: object
            required: [sku, quantity]
            properties:
              sku:
                type: string
              quantity:
                type: integer
                minimum: 1
    Problem:
      type: object
      properties:
        type:
          type: string
          format: uri-reference
          default: about:blank
        title:
          type: string
        status:
          type: integer
        detail:
          type: string
        instance:
          type: string
          format: uri-reference
      additionalProperties: true
  responses:
    Problem:
      description: Error (RFC 9457)
      content:
        application/problem+json:
          schema:
            $ref: '#/components/schemas/Problem'
    ValidationProblem:
      description: Validation failure (RFC 9457)
      content:
        application/problem+json:
          schema:
            allOf:
              - $ref: '#/components/schemas/Problem'
              - type: object
                properties:
                  errors:
                    type: array
                    items:
                      type: object
                      properties:
                        pointer:
                          type: string
                        message:
                          type: string
```

## Skeleton conventions

- Flesh out 2–4 representative paths fully; stub the rest with
  `description: TODO` so the surface is visible.
- Every operation carries a `default` response pointing at the shared
  Problem response — no operation may omit error handling.
- Error responses use `application/problem+json`, success uses
  `application/json`.
- Quote status codes (`'200'`) — YAML keys, not numbers.
