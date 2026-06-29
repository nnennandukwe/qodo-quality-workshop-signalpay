# Refund Workflow Build-Session Plan

## Summary
Use one short build session to implement the refund workflow under quality gates.

## Implementation Skill Handoff
- Planning skill completed: `workshop-plan-from-task`
- First implementation skill to run: `workshop-tdd-bdd`
- Required implementation prompt:
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
- Conditional skills to keep active during implementation:
  - `payment-idempotency` for idempotency keys, auth scope checks, event contract shape, and retry behavior.
  - `workshop-failure-path-testing` for missing-key, missing-scope, unknown-payment, and duplicate-event gates.
- Review/remediation skills:
  - `workshop-guidelines-audit` before committing or opening the PR.
  - optional `workshop-pythonic-review` for changed Python code.
  - optional `qodo-pr-resolver` only after Qodo posts PR findings.

## Execution Steps
1. Run `make doctor`.
2. Run `make verify` on the clean starter.
3. Read `AGENTS.md` and `rules/README.md`.
4. Select the relevant `PAY-*` repo-local rule IDs.
5. Optionally compare with Qodo rules if available.
6. Choose implementation skills and fill in the Implementation Skill Handoff.
7. Run the `workshop-tdd-bdd` prompt from the handoff.
8. Write failing tests for the refund behavior.
9. Implement the smallest code change: add `POST /payments/{payment_id}/refund`.
10. Run targeted tests.
11. Run `make verify`.
12. Run `workshop-guidelines-audit`.
13. Commit with a Conventional Commit.
14. Push and open a PR.
15. Inspect Qodo findings.
16. Run PR Resolver or manually fix findings.

## Test Plan
- Add one success-path test that captures then refunds `pay_1001`.
- Add one idempotency retry test for repeated refund keys.
- Add one missing-key failure test.
- Add one missing-scope failure test.
- Add one invalid-transition test for pending payment refund.
- Keep existing capture tests passing.

## Risk Checks
- No state mutation before auth and idempotency checks.
- No duplicate event for a retried idempotency key.
- No changed event field names.
- No committed secrets.

## Completion Notes
- Local verification: `uv run pytest tests/test_payments_api.py -q` passed; `make verify` passed.
- Repo rules applied: `PAY-001`, `PAY-002`, `PAY-003`, `PAY-004`, `PAY-005`, `PAY-006`, `PAY-007`, `PAY-009`, `PAY-010`
- Qodo review: pending PR review.
- Remediation: no local findings after verification.
