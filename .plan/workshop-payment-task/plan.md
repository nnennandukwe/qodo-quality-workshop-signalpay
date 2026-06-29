# Workshop Payment Workflow Plan

## Summary
Add a payment workflow change, such as refund or capture retry handling, while preserving the system's quality constraints.

This is a workshop task. The goal is to practice the quality workflow more than to expand product scope.

## Skills Used
- `qodo-get-rules`
- `workshop-plan-from-task`
- `workshop-tdd-bdd`
- `workshop-failure-path-testing`
- `payment-idempotency`
- `workshop-guidelines-audit`
- `qodo-pr-resolver`

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
- Qodo PR review

## Definition of Done
- Behavior tests cover success and failure paths.
- Local gates pass.
- Qodo findings are fixed or explicitly deferred with rationale.
- The PR explains the verification evidence.

