---
name: payment-idempotency
description: "Enforce SignalPay payment mutation rules: idempotency keys, auth scope checks, stable event contracts, and one durable outcome per retry key."
---

# Payment Idempotency

Use this skill when changing payment mutation workflows such as capture, refund, retry, settlement, or event emission.

## Required Rules

1. Payment mutation endpoints must require an `Idempotency-Key` header.
2. Auth and required scope checks must happen before state mutation.
3. A repeated operation with the same payment ID, operation name, and idempotency key must return the original response.
4. A repeated operation must not emit a duplicate event.
5. Event payloads must preserve stable camelCase keys.
6. Tests must cover the first request and retry behavior.

## Review Checklist

- Does the handler fail closed when the key is missing?
- Is the idempotency cache keyed by operation, payment ID, and idempotency key?
- Does the code store a copy of the response rather than a mutable object reference?
- Does the emitted event type match the workflow?
- Does a token without the required scope fail before mutation?

## Suggested Tests

- Missing idempotency key returns 400.
- Missing scope returns 403 and emits no event.
- First request mutates state and emits one event.
- Second request with the same key returns the same payload and emits no new event.

