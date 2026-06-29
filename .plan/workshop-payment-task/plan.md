# Workshop Payment Workflow Plan

## Summary
Add a small refund workflow to the SignalPay API while preserving the production-shaped payment guarantees from the workshop: idempotency, auth scope checks before mutation, stable camelCase API responses, stable event keys, and one event per idempotency key.

The selected workshop path is refund. Capture-retry handling is intentionally out of scope for this run so the change stays small enough to test, verify, and review.

## Skill Routing
- Selected repo-local rules: `PAY-001`, `PAY-002`, `PAY-003`, `PAY-004`, `PAY-005`, `PAY-006`, `PAY-007`, `PAY-009`, `PAY-010`
- Optional Qodo rules: loaded with `qodo-get-rules`; 25 hosted rules returned for refund workflow idempotency and workshop safety. They align with the repo-local rules on idempotency headers, retry replay, auth-before-mutation, event shape, behavior tests, verification gates, and secret safety.
- Planning skill used: `workshop-plan-from-task`
- Implementation entry skill: `workshop-tdd-bdd`
- Conditional implementation skills:
  - `payment-idempotency` because refund is a payment mutation workflow and must preserve idempotency-key, auth, response replay, and event guarantees.
  - `workshop-failure-path-testing` because missing keys, missing scopes, missing/invalid auth, unknown payments, and retry behavior must fail closed without mutation or duplicate events.
- Pre-PR review skills:
  - `workshop-guidelines-audit`
  - optional `workshop-pythonic-review` for changed Python code
- Post-review skill: optional `qodo-pr-resolver` only after Qodo posts PR findings.
- Exact next prompt after planning:
  ```text
  Use the workshop TDD/BDD skill and the plan files just created.
  Implement the refund workflow path only; do not implement capture-retry.
  Write the smallest failing tests first for refund behavior.
  Cover one happy path, missing Idempotency-Key, missing required scope, and retry with the same idempotency key.
  Use the payment-idempotency skill as a constraint while designing the tests.
  Do not implement production code until the failing tests prove the behavior gap.
  ```
- Local verification gates: `make test`, `make lint`, `make typecheck`, `make security`, `make semgrep`, `make verify`

## Selected Repo Rules
- `PAY-001` because refund is a payment mutation endpoint and must reject requests without `Idempotency-Key` before changing state or emitting events.
- `PAY-002` because refund reads and mutates payment state, so bearer session validation and the required scope check must happen before mutation, idempotency writes, or events.
- `PAY-003` because refund retry results must be cached by operation name, payment ID, and idempotency key so a refund cannot replay a capture result or another payment's result.
- `PAY-004` because a retried refund with the same idempotency key must return the original response and emit no duplicate refund event.
- `PAY-005` because the refund endpoint response is public API output and must preserve stable camelCase JSON fields such as `paymentId` and `customerId`.
- `PAY-006` because refund emits a payment event and must use `build_payment_event` with stable keys: `eventId`, `type`, `paymentId`, `customerId`, `amount`, `currency`, and `status`.
- `PAY-007` because the refund workflow changes endpoint behavior, state transition behavior, and event emission; tests must cover success and failure paths before implementation.
- `PAY-009` because local verification gates must stay intact; failures must be fixed in code or tests rather than weakening Ruff, Pyright, Bandit, Pytest, Semgrep, or hooks.
- `PAY-010` because refund introduces or uses an explicit payment status/transition that must be represented in the `PaymentStatus` type and tested.

`PAY-008` remains a setup and safety constraint for Qodo credentials. It is not a refund behavior rule, but it still governs this planning/setup work: no API key or local credential belongs in committed files.

## Optional Qodo Rule Status
- Loaded: yes
- Search queries:
  - `Refund Workflow Idempotency and Event Safety`
  - `Code Quality and Workshop Safety Standards`
- Result count: 25 hosted rules
- Differences from repo rules: no conflict found. Qodo returned more granular versions of the same standards, including idempotent payment mutations, required `Idempotency-Key`, original response replay, no duplicate events, auth-before-mutation, workflow-matching event type, camelCase event payloads, required behavior tests, no weakened gates, and no committed secrets.

## Scope
In:
- Add one refund workflow path.
- Require `Idempotency-Key` for refund requests.
- Validate auth and required refund/payment mutation scope before mutation.
- Cache refund responses with an operation-specific idempotency key.
- Return the original refund response on retry.
- Emit exactly one refund event for the first successful request.
- Preserve camelCase response fields and stable event keys.
- Add tests before production code.
- Run deterministic local gates.

Out:
- Capture-retry handling.
- External payment processor integration.
- Database persistence beyond existing in-memory workshop patterns.
- Frontend or dashboard changes.
- Deployment, Docker, or infrastructure changes.
- Moving repo-local rules into `.qodo/`.
- Committing Qodo credentials, `.env`, or local config.

## Behavior Scenarios
- Given an authorized caller, an existing refundable payment, and a new `Idempotency-Key`, when the caller requests a refund, then the API returns a camelCase refund response, updates the payment to the explicit refund status, and emits exactly one refund event.
- Given the same authorized caller, payment ID, refund operation, and `Idempotency-Key`, when the refund request is retried, then the API returns the exact original response and the event list still contains only one refund event.
- Given a refund request without `Idempotency-Key`, when the endpoint is called, then the API returns `400` with an actionable recovery message and does not mutate payment state or emit an event.
- Given a caller with a valid token but without the required refund/payment mutation scope, when the refund endpoint is called, then the API returns `403` before mutation and no event is emitted.
- Given missing, unknown, or wrong-audience auth, when the refund endpoint is called, then the API returns `401` before mutation and no event is emitted.
- Given a payment that is not eligible for refund, when the refund endpoint is called with valid auth and idempotency, then the API fails closed with a clear error and no refund event.

## Rule-Driven Test Expectations
- Missing idempotency key test: assert `400`, clear message naming `Idempotency-Key`, unchanged state, and no emitted event.
- Missing scope test: assert `403`, unchanged payment state, no idempotency cache write, and no emitted event.
- Success-path test: assert response status and exact camelCase payload shape, explicit refund status transition, and one event built with stable keys.
- Retry test: assert first and second response bodies match exactly and only one refund event exists for the payment/idempotency key.
- Status transition test: assert the new or changed refund status is represented by `PaymentStatus` and accepted only for the intended transition.

## Verification Gates
- Before implementation: run targeted tests after writing them and confirm they fail for the missing behavior.
- During implementation: run the targeted refund tests after the smallest useful production change.
- Full local gate before PR:
  ```bash
  make lint
  make typecheck
  make security
  make test
  make semgrep
  make verify
  ```
- Rule audit: run `workshop-guidelines-audit` before committing or opening the PR.
- Qodo PR review: open the PR after local gates pass, then inspect Qodo comments. Use `qodo-pr-resolver` only after Qodo posts findings.

## Failure and Recovery Rules
- Missing `Idempotency-Key` must fail before auth-passed mutation, cache writes, or events, with an actionable `400` response.
- Missing required scope must fail as `403` before mutation, idempotency writes, or events.
- Missing, unknown, or wrong-audience tokens must fail as `401` before mutation, idempotency writes, or events.
- Retried refunds must return cached/original output and must not emit duplicate events.
- Unsupported refund transitions must fail closed with unchanged state and no refund event.

## Commit Plan
- `test(payments): cover refund workflow safety`
- `feat(payments): add idempotent refund workflow`
- `docs(workshop): record refund verification evidence` only if workshop notes or PR evidence need a docs update.

## Definition of Done
- Plan files identify refund as the selected workshop path and capture-retry as out of scope.
- Behavior tests cover success, missing idempotency key, missing scope/auth, retry replay, and refund transition expectations.
- Implementation preserves selected `PAY-*` rules and `payment-idempotency` checklist items.
- `make verify` passes without weakening gates.
- No Qodo API key, `.env`, or local credential is committed.
- PR includes selected repo-local rules, optional Qodo rule status, verification evidence, and Qodo review/remediation notes.

## Assumptions
- The implementation will follow existing FastAPI route, contract, helper, and in-memory storage patterns in `src/signalpay_api/`.
- The refund endpoint should use the existing local session verification helper and payment API audience.
- The required scope should match the existing payment mutation scope pattern unless the codebase already defines a more specific refund scope.
- The refund event type should be workflow-specific, such as `payment.refunded`, and must be confirmed against existing event naming patterns before implementation.
- If the current model lacks a refund status, the implementation must update the explicit `PaymentStatus` type and tests under `PAY-010`.
