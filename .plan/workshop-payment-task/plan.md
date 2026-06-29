# High-Level Implementation Plan: Refund Workflow

## Summary
Add the **refund workflow** path from the Hands-On Task. This plan intentionally chooses refund rather than capture-retry handling so the workshop stays focused on one small payment mutation.

The intended product behavior is a `POST /payments/{payment_id}/refund` mutation that refunds an eligible captured payment while preserving:

- idempotency through `Idempotency-Key`
- auth and `payments:refund` scope checks before mutation
- stable camelCase API responses
- stable payment event keys built with `build_payment_event`
- one durable outcome and one refund event per idempotency key

No implementation code is written in this planning step.

## Selected Repo-Local Rule IDs

- `PAY-001` because refund is a payment mutation endpoint and must reject requests without `Idempotency-Key` before changing state or emitting events.
- `PAY-002` because refund must validate the bearer session and require `payments:refund` before state mutation, idempotency result writes, or event emission.
- `PAY-003` because refund idempotency results must be keyed by operation name, payment ID, and idempotency key, for example `("refund", payment_id, idempotency_key)`, so refund cannot replay capture results.
- `PAY-004` because retrying the same refund with the same operation, payment ID, and idempotency key must return the original response and emit no duplicate refund event.
- `PAY-005` because the public refund response must keep the existing `Payment` contract with stable camelCase JSON fields such as `paymentId` and `customerId`.
- `PAY-006` because the refund workflow emits a payment event and must use `build_payment_event` with stable keys: `eventId`, `type`, `paymentId`, `customerId`, `amount`, `currency`, and `status`.
- `PAY-007` because the behavior change requires tests first for success and failure paths, including missing key, missing scope, and retry behavior.
- `PAY-009` because all local verification gates must pass without weakening Ruff, Pyright, Bandit, Pytest, Semgrep, or related checks.
- `PAY-010` because the refund transition must be explicit and tested. The existing contracts already include `refunded` and `payment.refunded`; the implementation should still prove the allowed transition, expected to be captured-to-refunded.

`PAY-008` is not part of the product behavior, but remains a setup safety guardrail: do not commit Qodo API keys, local credentials, `.env` files, or generated secret material.

## Optional Qodo Rule Status

- Loaded: no.
- Reason: `qodo-get-rules` is not available on `PATH` in this environment.
- Differences from repo rules: none identified because no Qodo-hosted rules were loaded. The committed repo-local `PAY-*` rules remain the source of truth.

## Skill Routing

- Planning skill used: `workshop-plan-from-task`.
- First implementation skill to run: `workshop-tdd-bdd`.
- Conditional implementation skills to keep in context:
  - `payment-idempotency` for idempotency keys, auth ordering, retry replay, and duplicate-event prevention.
  - `workshop-failure-path-testing` for missing-key, missing-scope, invalid-transition, and duplicate-event gates.
- Pre-PR review skills:
  - `workshop-guidelines-audit` before committing or opening the PR.
  - optional `workshop-pythonic-review` for changed Python code.
- Post-review skill: optional `qodo-pr-resolver` only after Qodo posts PR findings.

Exact next prompt after planning:

```text
Use the workshop TDD/BDD skill and the plan files just created.
Write the smallest failing tests first for the refund workflow path.
Cover one happy path and at least one failure path.
Keep the payment-idempotency skill active as a constraint: require Idempotency-Key, check auth and payments:refund scope before mutation, replay the original response on retry, and emit no duplicate refund event.
Do not implement production code until the failing tests prove the behavior gap.
```

## Scope

In scope:

- Add one refund mutation workflow, expected route: `POST /payments/{payment_id}/refund`.
- Require `Authorization: Bearer ...` with `payments:refund` scope.
- Require `Idempotency-Key` for the refund mutation.
- Refund only an explicit eligible state, expected to be a captured payment.
- Return the stable `Payment` response model by alias with `status: "refunded"`.
- Emit exactly one `payment.refunded` event through `build_payment_event` for the first successful refund request.
- Replay the original refund response and emit no new event on retry with the same idempotency key.
- Add or update behavior tests before production code.
- Run the local verification ladder.

Out of scope:

- Capture-retry handling; this plan chooses refund instead.
- Partial refunds, refund amounts, processor integration, settlement, persistence, database schema, or frontend changes.
- New dependencies.
- Moving repo-local rules into `.qodo/`.
- Storing or editing Qodo credentials.

## Behavior Scenarios

### Happy path: refund an eligible payment

- Given `pay_1001` has been captured and the caller has a valid `payments:refund` token
- And the request includes a new `Idempotency-Key`
- When the caller posts to `/payments/pay_1001/refund`
- Then the API returns `200`
- And the JSON response uses camelCase fields with `status` set to `refunded`
- And exactly one `payment.refunded` event is appended with the stable event shape

### Retry path: same idempotency key

- Given a refund has already succeeded for a payment with idempotency key `refund-pay-1001-001`
- When the caller repeats the same refund request with the same key
- Then the API returns the original response body
- And no duplicate `payment.refunded` event is appended

### Missing idempotency key

- Given the caller has a valid `payments:refund` token
- When the caller posts to the refund endpoint without `Idempotency-Key`
- Then the API returns `400` with a clear recovery message
- And payment state, idempotency state, and event state do not change

### Missing refund scope

- Given the caller has a known token without `payments:refund`
- And the request includes an `Idempotency-Key`
- When the caller posts to the refund endpoint
- Then the API returns `403`
- And no payment state, idempotency state, or event state changes

### Invalid transition

- Given a payment is not in the explicit refundable state, such as `pending`
- When the caller posts to the refund endpoint with valid auth and an idempotency key
- Then the API rejects the request without changing state or emitting a refund event
- And the test documents the chosen status code and recovery message, expected to be a conflict-style response such as `409`

## Rule-Driven Test Expectations

- Add tests before implementation in `tests/test_payments_api.py`.
- Test the exact public JSON shape for the refund response, not only selected fields.
- Test the exact refund event shape or all stable event keys, including `type: "payment.refunded"`.
- Test retry behavior by sending the same refund request twice with the same idempotency key and asserting identical responses plus one refund event.
- Test missing `Idempotency-Key` returns `400` and causes no mutation or event.
- Test a known token without `payments:refund` returns `403` before any mutation or event.
- Test the explicit transition rule for non-refundable status if the implementation adds that guard.
- Keep existing capture and contract tests passing.

## Verification Gates

Run targeted checks during implementation:

```bash
uv run pytest tests/test_payments_api.py -q
```

Run the full local ladder before PR:

```bash
make lint
make typecheck
make security
make test
make semgrep
make verify
```

Do not weaken or skip gates to make the task pass.

## Failure and Recovery Rules

- Missing bearer token or invalid token fails closed with `401` before refund logic.
- Known token without `payments:refund` fails closed with `403` before mutation, idempotency writes, or event emission.
- Missing `Idempotency-Key` fails closed with `400` before mutation or event emission.
- Unknown payment fails without event emission.
- Non-refundable status fails without event emission or response caching.
- Successful refund stores a copied durable response, not a mutable object reference that can drift later.
- Retried refund with the same operation, payment ID, and idempotency key returns the stored response and emits no duplicate event.

## Commit Plan

- `test(payments): cover refund workflow safety`
- `feat(payments): add idempotent refund workflow`
- `docs(plan): record refund workflow plan` if plan files are committed separately or updated in the PR

## Definition of Done

- The refund workflow is covered by success, retry, and failure-path behavior tests.
- Existing capture, auth, contract, and workshop structure tests still pass.
- `make verify` passes without weakened gates.
- The PR summary names the selected `PAY-*` rules and includes verification evidence.
- Qodo review findings are fixed or explicitly deferred with rationale; if Qodo rules/review are unavailable, the fallback is documented.
- No secrets, local credentials, or Qodo API keys are committed.

## Assumptions

- The selected Hands-On Task path is refund workflow, not capture-retry handling.
- A captured payment is the intended refundable state.
- Existing `PaymentStatus` and `PaymentEventType` already include `refunded` and `payment.refunded`; if implementation discovers otherwise, update the explicit contract and tests under `PAY-010`.
- The existing `sp_live_payments_refund` token should be used for authorized refund tests.
- The existing in-memory app state remains sufficient for the workshop; no persistence layer is required.
