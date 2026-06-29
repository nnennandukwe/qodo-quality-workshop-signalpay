# Workshop Payment Workflow Plan

## Summary
Add a payment workflow change, such as refund or capture retry handling, while preserving the system's quality constraints.

This is a workshop task. The goal is to practice the quality workflow more than to expand product scope.

## Skill Routing
- Selected repo-local rules: `PAY-001`, `PAY-002`, `PAY-003`, `PAY-004`, `PAY-005`, `PAY-006`, `PAY-007`, `PAY-009`, `PAY-010`
- Optional Qodo rules: compare with `qodo-get-rules` if available; do not block on portal setup.
- Planning skill used: `workshop-plan-from-task`
- Implementation entry skill: `workshop-tdd-bdd`
- Conditional implementation skills:
  - `payment-idempotency` because refund and capture-retry workflows are payment mutation paths.
  - `workshop-failure-path-testing` because missing keys, missing scopes, and retry behavior must fail closed.
- Pre-PR review skills:
  - `workshop-guidelines-audit`
  - optional `workshop-pythonic-review` for changed Python code
- Post-review skill: optional `qodo-pr-resolver` after Qodo posts PR findings.
- Exact next prompt after planning:
  ```text
  Use the workshop TDD/BDD skill and the plan files just created.
  Write the smallest failing tests first for the selected payment workflow path.
  Cover one happy path and at least one failure path.
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
- Add one small payment mutation endpoint or behavior.
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
