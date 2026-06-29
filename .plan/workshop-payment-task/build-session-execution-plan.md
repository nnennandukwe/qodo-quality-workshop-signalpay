# Workshop Payment Workflow Build-Session Plan

## Summary
Use one short build session to implement a payment workflow change under quality gates.

## Execution Steps
1. Run `make doctor`.
2. Run `make verify` on the clean starter.
3. Run Qodo rules for the task.
4. Ask the agent to summarize relevant repo skills.
5. Write failing tests for the new behavior.
6. Implement the smallest code change.
7. Run targeted tests.
8. Run `make verify`.
9. Commit with a Conventional Commit.
10. Push and open a PR.
11. Inspect Qodo findings.
12. Run PR Resolver or manually fix findings.

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
- Qodo review:
- Remediation:

