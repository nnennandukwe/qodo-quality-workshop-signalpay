# Workshop Payment Workflow Plan — Refund Endpoint

## Summary
Add a `POST /payments/{payment_id}/refund` endpoint that transitions a captured
payment to `refunded`, emits exactly one `payment.refunded` event, and is safe
under retry. The change is intentionally small: the contract layer is already
pre-wired (`refunded` status, `payment.refunded` event type, and the
`sp_live_payments_refund` token/`payments:refund` scope all exist in
`contracts.py`), so the work is a new endpoint plus behavior tests — not new
product scope. The teaching goal is to make an AI agent preserve idempotency,
auth-before-mutation, the event contract, and an explicit state transition,
rather than treating "add refund" as a plain file edit.

Reference implementation to mirror: `capture_payment` in `src/signalpay_api/app.py`.

## Skill Routing
- Selected repo-local rules: `PAY-001`, `PAY-002`, `PAY-003`, `PAY-004`, `PAY-005`, `PAY-006`, `PAY-007`, `PAY-009`, `PAY-010` (and `PAY-008` already satisfied by the local key config).
- Optional Qodo rules: **AVAILABLE.** `qodo-get-rules` returned hosted rules that mirror every selected `PAY-*` rule, plus enrichments that shape this plan: store a *copy* of the cached response (1507532), actionable error messages (1507597), unknown payment ID → 404 with no event (1507516), wrong audience → 401 (1507544), one gate-condition per failure test (1507608). Treated as enrichment; repo-local rules remain source of truth.
- Planning skill used: `workshop-plan-from-task`
- Implementation entry skill: `workshop-tdd-bdd`
- Conditional implementation skills:
  - `payment-idempotency` — active throughout; refund is a payment mutation path.
  - `workshop-failure-path-testing` — for the 400 / 403 / 409 / 404 / 401 gates.
- Pre-PR review skills: `workshop-guidelines-audit`, optional `workshop-pythonic-review` for changed Python.
- Post-review skill: optional `qodo-pr-resolver` after Qodo posts PR findings.
- Exact next prompt after planning:
  ```text
  Use the workshop TDD/BDD skill and the plan files in
  .plan/workshop-payment-task/. Keep the payment-idempotency skill active.

  Write the smallest failing tests first for the refund workflow:
  one happy path (capture pay_1001, then refund -> 200, status "refunded",
  exactly one payment.refunded event) and the failure paths
  (missing Idempotency-Key -> 400, missing payments:refund scope -> 403,
  refund of a non-captured payment -> 409). Add them to tests/test_payments_api.py.

  Confirm each test fails for the right reason before writing the
  POST /payments/{payment_id}/refund endpoint. Do not implement production
  code until the failing tests prove the behavior gap. Do not weaken any gate.
  ```
- Local verification gates: `make test`, `make lint`, `make typecheck`, `make security`, `make semgrep`, `make verify`.

## Selected Repo Rules (why each applies)
- `PAY-001` — refund is a mutation; reject a missing `Idempotency-Key` with 400 before any state change.
- `PAY-002` — validate the bearer token + `payments:refund` scope before mutating or emitting (audience `payments-api`).
- `PAY-003` — key the idempotency cache by `("refund", payment_id, idempotency_key)` so a refund replay never collides with a capture replay.
- `PAY-004` — a retried refund returns the original response and emits no second event.
- `PAY-005` — the response stays camelCase (`paymentId`, `customerId`) via `response_model=Payment, response_model_by_alias=True`.
- `PAY-006` — emit through `build_payment_event(event_type="payment.refunded", ...)`, preserving the stable event keys.
- `PAY-007` — write success and failure-path tests first.
- `PAY-009` — fix code/tests rather than relaxing any gate.
- `PAY-010` — define and test the explicit transition `captured -> refunded`; refunds from any other status fail closed.

## Scope
In:
- New endpoint `POST /payments/{payment_id}/refund`.
- Explicit transition guard: only `captured` payments may be refunded.
- Behavior tests written before implementation.
- Local deterministic gates, then PR + Qodo review.

Out:
- Partial / amount-specified refunds (full refund only; no amount parameter).
- Database persistence, dashboard/frontend, real processor integration, Docker/deploy.
- Changes to `contracts.py` (status, event type, scope, and token already exist).

## Behavior Scenarios (Given / When / Then)
1. Happy path — Given `pay_1001` has been captured and the caller has `payments:refund` scope, When refund runs with a new `Idempotency-Key`, Then 200 with `status: "refunded"` and exactly one `payment.refunded` event.
2. Idempotent retry — Given a refund already succeeded for an idempotency key, When the same request is retried, Then the response is identical and no additional `payment.refunded` event is emitted.
3. Missing key — Given a valid refund caller, When the `Idempotency-Key` header is absent, Then 400 with a recovery message and no state change or event.
4. Missing scope — Given a token without `payments:refund` (e.g. `sp_live_payments_reader`), When refund runs, Then 403 before mutation and no event.
5. Invalid transition — Given `pay_1002` is `pending` (never captured), When refund runs with valid scope + key, Then 409 (fail closed), status unchanged, no event.
6. (Enrichment) Unknown payment — Given an unknown `payment_id`, When refund runs, Then 404 and no event (Qodo 1507516).
7. (Enrichment) Wrong audience — Given a non-`payments-api` token, When refund runs, Then 401 (Qodo 1507544 / PAY-002).

Critical ordering note (teaching point): the idempotency-replay check must run **before** the `captured`-state guard. Otherwise a legitimate retry of a successful refund would hit the guard (the payment is now `refunded`) and wrongly return 409 instead of the cached 200. Order: auth/scope → key present → payment exists → replay cache → transition guard → mutate → event → cache copy → return.

## Rule-Driven Test Expectations
| Scenario | Rules | Key assertions |
| --- | --- | --- |
| 1 Happy path | PAY-004/005/006/010 | 200; body `status == "refunded"`; camelCase keys; exactly one event with `type == "payment.refunded"` and stable keys |
| 2 Retry | PAY-003/004 | both responses identical; refund-event count unchanged on the second call |
| 3 Missing key | PAY-001 | 400; `detail == "Idempotency-Key header is required"`; no event; status unchanged |
| 4 Missing scope | PAY-002 | 403; `detail == "payments:refund scope is required"`; no event; status unchanged |
| 5 Invalid transition | PAY-010 | 409; no event; status unchanged |
| 6 Unknown payment | Qodo 1507516 | 404; no event |
| 7 Wrong audience | PAY-002 / Qodo 1507544 | 401 |

Assert the **specific** `payment.refunded` event (filter by type), not the total event count — the happy path also contains the earlier `payment.captured` event from setup.

## Verification Gates
- `make test`, `make lint`, `make typecheck`, `make security`, `make semgrep`, `make verify`
- repo-local rules audit (`workshop-guidelines-audit`)
- Qodo PR review (plus PR Resolver for remediation)

## Failure and Recovery Rules
- Missing `Idempotency-Key` → 400, message `"Idempotency-Key header is required"` (fail closed before mutation).
- Missing `payments:refund` scope → 403, message `"payments:refund scope is required"` (before mutation/event).
- Refund of a non-`captured` payment → 409 with an actionable message naming the current status; no mutation, no event.
- Unknown payment → 404 `"payment not found"`; no event.
- No event is ever appended on any failure path; no partial state change.

## Commit Plan
- `test(payments): add failing refund workflow behavior tests`
- `feat(payments): add idempotent refund endpoint with auth and transition guards`
- `docs(plan): record refund workshop plan and verification evidence`

## Definition of Done
- Behavior tests cover the happy path plus the 400 / 403 / 409 failure paths (404 / 401 enrichment recommended).
- `make verify` passes with no weakened gates.
- Qodo findings are fixed or explicitly deferred with rationale.
- The PR explains the verification evidence and the `captured -> refunded` decision.

## Assumptions
- Only `captured` payments are refundable (`captured -> refunded`); refunding `authorized` is treated as a void concern and out of scope. Invalid source state → 409. (Reviewer may instead choose to allow `authorized -> refunded`; the transition just needs to stay explicit and tested per PAY-010.)
- Full refunds only; no amount parameter in this slice.
- Tests live in `tests/test_payments_api.py`, consistent with the existing structure; each failure-path test asserts exactly one gate (Qodo 1507608).
- The happy-path test establishes `captured` state by calling the existing capture endpoint rather than mutating seed data.
