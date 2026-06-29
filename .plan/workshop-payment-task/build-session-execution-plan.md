# Workshop Payment Workflow Build-Session Plan

## Summary
Use one short build session to implement a payment workflow change under quality gates.

## Implementation Skill Handoff
- Planning skill completed: `workshop-plan-from-task`
- First implementation skill to run: `workshop-tdd-bdd`
- Required implementation prompt:
  ```text
  Use the workshop TDD/BDD skill and the plan files just created.
  Write the smallest failing tests first for the selected payment workflow path.
  Cover one happy path and at least one failure path.
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
8. Write failing tests for the new behavior.
9. Implement the smallest code change.
10. Run targeted tests.
11. Run `make verify`.
12. Run `workshop-guidelines-audit`.
13. Commit with a Conventional Commit.
14. Push and open a PR.
15. Inspect Qodo findings.
16. Run PR Resolver or manually fix findings.

## Test Plan
- Add one success-path test.
- Add one idempotency retry test.
- Add one missing-key or missing-scope failure test.
- Keep existing capture tests passing.

## Risk Checks
- No state mutation before auth and idempotency checks.
- No duplicate event for a retried idempotency key.
- No changed event field names.
- No committed secrets.

## Completion Notes
- Local verification:
- Repo rules applied:
- Qodo review:
- Remediation:
