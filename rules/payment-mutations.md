# Payment Mutation Rules

Use these rules when changing endpoints that mutate payment state, including
capture, refund, retry, settlement, or event emission behavior.

## PAY-001: Payment mutation endpoints require `Idempotency-Key`

- Trigger: adding or changing a payment mutation endpoint.
- Required behavior: reject mutation requests without an `Idempotency-Key`
  header before changing state or emitting events.
- Verification signal: tests cover the missing-key case and assert a `400`
  response with a clear recovery message.

## PAY-003: Idempotency cache keys include operation, payment ID, and idempotency key

- Trigger: caching or replaying mutation responses.
- Required behavior: key cached results by operation name, payment ID, and
  idempotency key so one workflow cannot replay another workflow's result.
- Verification signal: code uses an operation-specific result key and tests
  cover retry behavior for the relevant endpoint.

## PAY-004: Retried mutation returns the original response and emits no duplicate event

- Trigger: implementing retry or idempotent mutation behavior.
- Required behavior: a repeated request with the same operation, payment ID,
  and idempotency key returns the first response and does not append another
  event.
- Verification signal: tests assert the first and second response match and
  the event list contains exactly one event.
