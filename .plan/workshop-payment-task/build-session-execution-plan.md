# Workshop Payment Workflow Build-Session Plan — Refund Endpoint

## Summary
One short build session: add `POST /payments/{payment_id}/refund` to
`src/signalpay_api/app.py` (mirroring `capture_payment`) and prove it with
behavior tests in `tests/test_payments_api.py`, all under the verification
gates. Tests first; implementation only after they fail for the right reason.

## Starting State
- Branch: create `feat/refund-workflow` off `main` before editing.
- Current local verification: clean. `make doctor` passed; `make verify` green
  (ruff, pyright 0 errors, bandit clean, 13 pytest passed, semgrep clean).
- Selected repo-local rule IDs: `PAY-001`, `PAY-002`, `PAY-003`, `PAY-004`,
  `PAY-005`, `PAY-006`, `PAY-007`, `PAY-009`, `PAY-010`.
- Optional Qodo rules status: AVAILABLE via `qodo-get-rules`; hosted rules mirror
  the selected `PAY-*` set with enrichments (store-a-copy 1507532, actionable
  errors 1507597, unknown-payment 404-no-event 1507516, wrong-audience 401
  1507544, one-gate-per-failure-test 1507608). Enrichment only.
- Pre-wired contract (no change needed): `PaymentStatus` includes `refunded`,
  `PaymentEventType` includes `payment.refunded`, token
  `sp_live_payments_refund` has scope `payments:refund`.

## Implementation Skill Handoff
- Planning skill completed: `workshop-plan-from-task`
- **First implementation skill to run: `workshop-tdd-bdd`**
- Required implementation prompt (run this next):
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
- Conditional skills to keep active during implementation:
  - `payment-idempotency` — idempotency key, auth scope, event contract, retry.
  - `workshop-failure-path-testing` — the 400 / 403 / 409 / 404 / 401 gates.
- Review/remediation skills:
  - `workshop-guidelines-audit` before committing or opening the PR.
  - optional `workshop-pythonic-review` for changed Python.
  - optional `qodo-pr-resolver` only after Qodo posts PR findings.

## Execution Steps
1. Create branch `feat/refund-workflow`.
2. Confirm baseline: `make verify` is green (already verified this session).
3. Re-read `AGENTS.md`, `rules/README.md`, and the selected `PAY-*` rule docs.
4. Keep `payment-idempotency` constraints in view; Qodo rules already compared (enrichment).
5. Run the `workshop-tdd-bdd` prompt above.
6. Write failing tests (happy + 400 + 403 + 409; add 404/401 enrichment if time).
7. Run targeted tests; confirm they fail for the right reason (assertion, not import error).
8. Implement `refund_payment` in `app.py`, mirroring `capture_payment`:
   auth+`payments:refund` scope → key present (400) → payment exists (404) →
   replay cache `("refund", payment_id, key)` → transition guard
   (`captured` only, else 409) → set status `refunded` →
   `build_payment_event(event_type="payment.refunded", ...)` + append →
   store `deepcopy(payment)` in `idempotency_results` → return payment.
9. Run targeted tests until green.
10. Run `make verify`.
11. Run `workshop-guidelines-audit` against the diff.
12. Commit with Conventional Commits (test → feat → docs).
13. Push branch and open a PR.
14. Inspect Qodo review findings (or document the fallback if Qodo GitHub is blocked).
15. Run `qodo-pr-resolver` or manually fix findings; record remediation notes.

## Test Plan
- Targeted (write first, in `tests/test_payments_api.py`):
  - `test_refund_captured_payment_emits_one_refund_event` (happy)
  - `test_refund_is_idempotent_on_retry` (same key → identical body, no new refund event)
  - `test_refund_requires_an_idempotency_key` (400)
  - `test_refund_requires_refund_scope` (403)
  - `test_refund_rejects_non_captured_payment` (409)
  - optional: `test_refund_unknown_payment_returns_404`, `test_refund_rejects_wrong_audience` (401)
- Full: `make verify` (must stay green; existing 13 tests keep passing — PAY-009).

## Risk Checks
- Idempotency: cache key is `("refund", ...)`, distinct from capture; retry returns the stored copy; replay check runs *before* the state guard.
- Auth scope: `payments:refund` validated before any mutation or event; 401 wrong audience, 403 missing scope.
- Event contract: only `build_payment_event` with `payment.refunded`; stable camelCase keys unchanged; exactly one refund event; none on failure paths.
- State transition: only `captured -> refunded`; every other source status → 409, no mutation (PAY-010).
- Static analysis / secrets: `bandit` + `semgrep` clean; no secrets in code, tests, or plan (PAY-008).

## Completion Notes
- Local verification: `make verify` green — ruff pass, pyright 0 errors, bandit clean, pytest 20 passed (13 existing + 7 refund), semgrep clean (exit 0). Red→green confirmed: the 7 refund tests failed for the right reason before the endpoint existed and passed after it was added.
- Repo rules applied: PAY-001 (400 on missing key), PAY-002 (auth + `payments:refund` before mutation; 401/403), PAY-003 (cache key `("refund", payment_id, key)`), PAY-004 (retry returns cached copy, no second event), PAY-005 (camelCase response via `response_model_by_alias`), PAY-006 (`build_payment_event` `payment.refunded`, stable keys), PAY-007 (1 happy + 6 failure/edge tests), PAY-009 (no gate weakened), PAY-010 (explicit `captured -> refunded` guard, else 409). PAY-008 satisfied (no secrets in diff).
- Qodo review: pending — runs after the PR opens. Local `workshop-guidelines-audit`: PASS (no Must-Fix). Qodo enrichment rules adopted: store-a-copy (1507532), unknown-payment 404-no-event (1507516), wrong-audience 401 (1507544), one-gate-per-failure-test (1507608).
- Remediation: none outstanding from the local audit; record and resolve any Qodo PR findings here after review (use `qodo-pr-resolver`).
