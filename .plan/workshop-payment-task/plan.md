# Refund Workflow Workshop Plan

## Summary
Add a refund workflow while preserving the system's payment mutation guarantees.

This is a workshop task. The implementation path is refund-only, not capture-retry.
The goal is to practice the quality workflow more than to expand product scope.

## Skill Routing
- Selected repo-local rules: `PAY-001`, `PAY-002`, `PAY-003`, `PAY-004`, `PAY-005`, `PAY-006`, `PAY-007`, `PAY-009`, `PAY-010`
- Optional Qodo rules: loaded successfully during setup; they matched the repo-local concerns around idempotency, auth-before-mutation, retry behavior, stable event keys, tests, and unchanged gates. Do not block implementation on Qodo portal availability.
- Planning skill used: `workshop-plan-from-task`
- Implementation entry skill: `workshop-tdd-bdd`
- Conditional implementation skills:
  - `payment-idempotency` because refunds are payment mutation paths.
  - `workshop-failure-path-testing` because missing keys, missing scopes, and retry behavior must fail closed.
- Pre-PR review skills:
  - `workshop-guidelines-audit`
  - optional `workshop-pythonic-review` for changed Python code
- Post-review skill: optional `qodo-pr-resolver` after Qodo posts PR findings.
- Exact next prompt after planning:
  ```text
  Use the workshop TDD/BDD skill.

  Use .plan/workshop-payment-task/plan.md and .plan/workshop-payment-task/build-session-execution-plan.md.
  Write the smallest failing tests first for the refund workflow.
  Cover:
  - successful refund of a captured payment
  - retry with the same refund idempotency key returning the same payload and emitting no second payment.refunded event
  - missing Idempotency-Key failing before mutation or event emission
  - missing payments:refund scope failing before mutation or event emission
  - non-captured payment refund failing closed

  Do not implement production code until the failing tests prove the behavior gap.
  ```
- Local verification gates: `make test`, `make lint`, `make typecheck`, `make security`, `make semgrep`, `make verify`

## Selected Repo Rules
- `PAY-001`
- `PAY-002`
- `PAY-003`
- `PAY-004`
- `PAY-005`
- `PAY-006`
- `PAY-007`
- `PAY-009`
- `PAY-010`

## Scope
- Add `POST /payments/{payment_id}/refund`.
- Require `payments:refund` scope before any refund mutation.
- Require `Idempotency-Key` before mutation or event emission.
- Key refund replay results as `("refund", payment_id, idempotency_key)`.
- Refund only captured payments; non-captured payments fail closed with `409`.
- Emit one stable `payment.refunded` event through `build_payment_event`.
- Preserve existing capture behavior.
- Add behavior tests before implementation.
- Run local deterministic gates.
- Open a PR and let Qodo review it.

Out of scope:
- database persistence
- frontend dashboard
- external payment processor integration
- Docker or deployment

## Behavior Scenarios
- Given a valid payment and a valid scope, when the workflow runs with a new idempotency key, then exactly one event is emitted.
- Given the same idempotency key is retried, when the workflow runs again, then the same response is returned and no second event is emitted.
- Given a token without the required scope, when the workflow runs, then the API rejects the request before mutation.
- Given the idempotency key is missing, when the workflow runs, then the API fails closed.
- Given a pending payment, when refund is requested, then the API returns `409` and leaves payment/event state unchanged.

## Verification Gates
- `make test`
- `make lint`
- `make typecheck`
- `make security`
- `make semgrep`
- `make verify`
- repo-local rules audit
- Qodo PR review

## Definition of Done
- Behavior tests cover success and failure paths.
- Local gates pass.
- Qodo findings are fixed or explicitly deferred with rationale.
- The PR explains the verification evidence.

## Assumptions
- Refunds are allowed only from `captured` to `refunded`.
- `PaymentStatus` and `PaymentEventType` already include `refunded` and `payment.refunded`.
- Local skill-install artifacts under `.agents/skills/` and `.claude/` remain uncommitted unless explicitly requested.
