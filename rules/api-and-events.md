# API and Event Contract Rules

Use these rules when changing response models, event payloads, payment
statuses, or route contracts.

## PAY-005: Public API responses use stable camelCase JSON fields

- Trigger: adding or changing response models or endpoint return payloads.
- Required behavior: public JSON fields stay camelCase, including
  `paymentId` and `customerId`.
- Verification signal: API tests assert exact response payload shape and route
  decorators preserve alias output with `response_model_by_alias=True`.

## PAY-006: Payment events use `build_payment_event` and preserve stable event keys

- Trigger: emitting or changing payment events.
- Required behavior: build payment events through `build_payment_event` and
  preserve the existing event keys: `eventId`, `type`, `paymentId`,
  `customerId`, `amount`, `currency`, and `status`.
- Verification signal: tests assert exact event shape and event type for the
  workflow.

## PAY-010: New payment statuses or transitions must be explicit and tested

- Trigger: adding or changing payment statuses or state transitions.
- Required behavior: update the explicit `PaymentStatus` type and add tests
  for the allowed transition.
- Verification signal: type checks pass, existing status tests still pass, and
  behavior tests prove the new transition.
