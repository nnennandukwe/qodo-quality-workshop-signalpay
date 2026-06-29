---
name: workshop-failure-path-testing
description: "Design failure-first tests for payment workflow gates, recovery behavior, auth checks, idempotency, and event emission."
---

# Workshop Failure Path Testing

Use this skill when a workflow must refuse unsafe progression.

## High-Value Failure Paths

- Missing `Idempotency-Key` blocks mutation.
- Missing required auth scope blocks mutation.
- Unknown payment ID returns 404 without emitting an event.
- Retried idempotency key returns original response without duplicate event.
- Wrong token audience returns 401.

## Test Rules

- Assert no forbidden state mutation occurred.
- Assert no duplicate event was emitted.
- Assert response text tells the caller what to fix.
- Keep each failure test focused on one gate.

## Output

List:

- negative paths added
- blocking guarantees verified
- remaining untested gate conditions

