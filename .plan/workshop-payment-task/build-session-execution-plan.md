# Build-Session Execution Plan: Refund Workflow

## Summary
Complete one TDD build session for the Hands-On Task by implementing the refund workflow only. The session should start from the plan in `.plan/workshop-payment-task/plan.md`, write failing behavior tests first, make the smallest production change, and finish with local verification plus a guideline audit.

No implementation code is written by this planning step.

## Starting State

- Branch: `main`.
- Current local verification: `make verify` passed before this plan update with Ruff, Pyright, Bandit, Pytest (`13 passed`), and Semgrep.
- Selected Hands-On Task path: refund workflow.
- Selected repo-local rule IDs: `PAY-001`, `PAY-002`, `PAY-003`, `PAY-004`, `PAY-005`, `PAY-006`, `PAY-007`, `PAY-009`, `PAY-010`.
- Setup safety guardrail: `PAY-008` remains relevant to Qodo/local credential handling; no credential edits are planned.
- Optional Qodo rules status: not loaded because `qodo-get-rules` is not available on `PATH`; repo-local rules are the baseline.
- Relevant implementation constraint skill: `payment-idempotency`.

## Implementation Skill Handoff

- Planning skill completed: `workshop-plan-from-task`.
- First implementation skill to run: `workshop-tdd-bdd`.
- Required implementation prompt:

  ```text
  Use the workshop TDD/BDD skill and the plan files just created.
  Write the smallest failing tests first for the refund workflow path.
  Cover one happy path and at least one failure path.
  Keep the payment-idempotency skill active as a constraint: require Idempotency-Key, check auth and payments:refund scope before mutation, replay the original response on retry, and emit no duplicate refund event.
  Do not implement production code until the failing tests prove the behavior gap.
  ```

- Conditional skills to keep active during implementation:
  - `payment-idempotency` for idempotency keys, auth scope checks, response replay, event contract shape, and duplicate-event prevention.
  - `workshop-failure-path-testing` for missing-key, missing-scope, invalid-transition, unknown-payment, and duplicate-event gates.
- Review/remediation skills:
  - `workshop-guidelines-audit` before committing or opening the PR.
  - optional `workshop-pythonic-review` for changed Python code.
  - optional `qodo-pr-resolver` only after Qodo posts PR findings.

## Execution Steps

1. Re-open context before editing:
   - `AGENTS.md`
   - `rules/README.md`
   - selected rule docs under `rules/`
   - `.agents/skills/payment-idempotency/SKILL.md`
   - `.plan/workshop-payment-task/plan.md`
2. Confirm the selected path remains refund workflow and capture-retry handling remains out of scope.
3. Run the exact TDD prompt from the Implementation Skill Handoff.
4. Inspect the existing payment API and tests:
   - `src/signalpay_api/app.py`
   - `src/signalpay_api/contracts.py`
   - `tests/test_payments_api.py`
   - `tests/test_contracts.py`
5. Write the smallest failing behavior tests first in `tests/test_payments_api.py`.
6. Run targeted tests and confirm the new tests fail for the expected missing behavior, not because of syntax/import mistakes:

   ```bash
   uv run pytest tests/test_payments_api.py -q
   ```

7. Implement the smallest production change that satisfies the failing tests, preserving existing capture behavior.
8. Re-run targeted tests:

   ```bash
   uv run pytest tests/test_payments_api.py -q
   ```

9. If targeted tests fail, classify the failure as formatting, linting, type checking, security/static analysis, behavior, or repo guideline compliance, then fix without weakening gates.
10. Run the full verification ladder:

    ```bash
    make verify
    ```

11. Run a guidelines audit against `AGENTS.md`, selected `PAY-*` rules, `payment-idempotency`, and the current diff.
12. If Qodo review is available after PR creation, compare findings with the repo-local rules. If Qodo is unavailable or delayed, document the fallback.
13. Commit with Conventional Commits and keep commits reviewable.
14. Push and open the PR with rule selection, tests, and verification evidence in the description.
15. Resolve Qodo findings manually or with PR Resolver only after Qodo posts findings.

## Test Plan

Add or update tests before production code:

- `test_refund_requires_an_idempotency_key`
  - Valid refund token, missing `Idempotency-Key`.
  - Expect `400` and no event/state mutation.
- `test_refund_requires_refund_scope`
  - Known token without `payments:refund`, with an idempotency key.
  - Expect `403` and no event/state mutation.
- `test_refund_captured_payment_returns_contract_shape_and_emits_event`
  - Arrange an eligible captured payment.
  - Refund with valid refund token and a new idempotency key.
  - Expect exact camelCase response shape with `status: "refunded"`.
  - Expect exactly one `payment.refunded` event with stable event keys.
- `test_refund_is_idempotent_and_emits_one_refund_event`
  - Repeat the same refund request with the same idempotency key.
  - Expect first and second responses to match.
  - Expect no duplicate refund event.
- Optional but preferred under `PAY-010`: `test_refund_rejects_non_refundable_payment_status`
  - Attempt to refund a pending or already-refunded payment.
  - Expect a clear failure and no event.

Keep existing tests passing:

```bash
uv run pytest -q
```

## Production Change Constraints

During implementation, preserve these constraints:

- Auth and required-scope validation must happen before idempotency lookup, state mutation, cache writes, or event emission.
- Missing `Idempotency-Key` must be rejected before state mutation or event emission.
- Idempotency key shape must include operation, payment ID, and request key; refund must not share capture's operation key.
- Stored idempotency results should be copied so later mutations cannot change replayed responses.
- Refund event must be built through `build_payment_event`.
- Public responses must keep `response_model_by_alias=True` and camelCase fields.
- No new dependency should be added for small local logic.

## Risk Checks

- Idempotency: same refund request returns same body and one refund event.
- Auth scope: reader/capture tokens cannot refund and cannot mutate or write idempotency results.
- Event contract: refund event has stable keys and `type: "payment.refunded"`.
- Transition safety: only the explicit refundable state transitions to `refunded`; non-refundable states fail without event emission.
- Existing behavior: capture endpoint behavior and tests are not regressed.
- Static analysis: lint, typecheck, security, tests, and Semgrep all pass.
- Secrets: no Qodo API key, `.env`, local config, or generated credential material appears in the diff.

## Verification Commands

Use targeted commands while building:

```bash
uv run pytest tests/test_payments_api.py -q
uv run pytest tests/test_contracts.py -q
```

Use full verification before PR:

```bash
make lint
make typecheck
make security
make test
make semgrep
make verify
```

## Commit Plan

Preferred small commit sequence:

1. `test(payments): cover refund workflow safety`
2. `feat(payments): add idempotent refund workflow`
3. `docs(plan): record refund workflow plan` if plan files are included as a separate documentation change

If the workshop flow prefers one commit, use a single Conventional Commit such as:

```text
feat(payments): add idempotent refund workflow
```

and describe tests plus verification evidence in the PR body.

## Completion Notes Template

Fill this in after implementation and verification:

- Targeted tests:
- Full verification:
- Repo rules applied:
- Qodo rules/review status:
- Findings fixed:
- Findings deferred with rationale:
- Residual risks:
