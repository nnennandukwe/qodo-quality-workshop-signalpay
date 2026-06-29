# Workshop Payment Workflow Build-Session Plan

## Summary
Use one build session to implement the refund workflow path only. The session starts from the completed planning work, writes failing behavior tests first, implements the smallest refund change, verifies locally, then prepares the PR for Qodo review and remediation.

## Starting State
- Branch: `main`
- Current local setup: `make doctor` passed; Qodo API configuration exists at `~/.qodo/config.json`; official Qodo skills and repo-local workshop skills are installed.
- Current local verification: `make verify` passed during setup. Run it again before implementation if the branch has changed.
- Existing working tree note: generated skill-install artifacts are untracked (`.agents/skills/`, `.claude/`, `skills-lock.json`). Do not mix unrelated generated setup files into the refund behavior commit unless the workshop explicitly wants them committed.
- Selected repo-local rule IDs: `PAY-001`, `PAY-002`, `PAY-003`, `PAY-004`, `PAY-005`, `PAY-006`, `PAY-007`, `PAY-009`, `PAY-010`
- Credential safety rule: `PAY-008` applies to setup and review hygiene; do not commit Qodo API keys, `.env`, or local credentials.
- Optional Qodo rules status: loaded with `qodo-get-rules`; 25 hosted rules returned and aligned with the selected repo-local rules.

## Implementation Skill Handoff
- Planning skill completed: `workshop-plan-from-task`
- First implementation skill to run: `workshop-tdd-bdd`
- Required implementation prompt:
  ```text
  Use the workshop TDD/BDD skill and the plan files just created.
  Implement the refund workflow path only; do not implement capture-retry.
  Write the smallest failing tests first for refund behavior.
  Cover one happy path, missing Idempotency-Key, missing required scope, and retry with the same idempotency key.
  Use the payment-idempotency skill as a constraint while designing the tests.
  Do not implement production code until the failing tests prove the behavior gap.
  ```
- Conditional skills to keep active during implementation:
  - `payment-idempotency` for idempotency key requirement, auth-before-mutation, operation-specific cache keys, original response replay, stable event shape, and no duplicate retry event.
  - `workshop-failure-path-testing` for missing key, missing/invalid auth, missing scope, unsupported transition, and duplicate-event negative paths.
- Review/remediation skills:
  - `workshop-guidelines-audit` before committing or opening the PR.
  - optional `workshop-pythonic-review` for changed Python code.
  - optional `qodo-pr-resolver` only after Qodo posts PR findings.

## Execution Steps
1. Confirm the branch and working tree with `git status --short`; avoid mixing unrelated setup artifacts into the refund commit.
2. Re-read `AGENTS.md`, `rules/README.md`, linked rule docs, and `skills/payment-idempotency/SKILL.md` if implementation starts in a fresh session.
3. Run the exact `workshop-tdd-bdd` prompt from the handoff.
4. Inspect the existing FastAPI app, contracts, tests, auth helper, idempotency patterns, event builder, and payment status model.
5. Write failing tests first for refund success, missing `Idempotency-Key`, missing scope/auth, retry replay, event shape, and status transition behavior.
6. Run the targeted test command for the changed test module and confirm the new tests fail for the expected behavior gap.
7. Implement the smallest production change for refund.
8. Keep auth and scope checks before mutation, idempotency cache writes, and event emission.
9. Key idempotency results by operation name, payment ID, and `Idempotency-Key`.
10. Store or replay a stable copy of the original response for retries.
11. Build refund events with `build_payment_event` and stable event keys.
12. Run targeted tests until the refund tests pass.
13. Run the full verification ladder:
    ```bash
    make lint
    make typecheck
    make security
    make test
    make semgrep
    make verify
    ```
14. Run `workshop-guidelines-audit` against the diff and selected rules.
15. Review the diff for secret leakage and ensure no Qodo API key or local credential is present.
16. Commit with a Conventional Commit, likely `feat(payments): add idempotent refund workflow`.
17. Push and open a PR only after local verification passes.
18. Inspect Qodo review evidence and use `qodo-pr-resolver` or manual remediation after Qodo posts findings.

## Test Plan
- Targeted success test: authorized refund with `Idempotency-Key` returns the expected camelCase response, updates the explicit refund status, and emits one refund event.
- Targeted retry test: same operation, payment ID, and idempotency key returns the same payload and emits no second event.
- Targeted missing-key test: absent `Idempotency-Key` returns `400`, names the missing header, and leaves state/events unchanged.
- Targeted auth/scope tests: missing/invalid auth returns `401`; valid token without required scope returns `403`; both paths leave state/events unchanged.
- Targeted transition test: non-refundable payment state fails closed without a refund event if such a state exists in current fixtures.
- Full tests: run `make test`, then `make verify` after lint, typecheck, security, and Semgrep are clean.

## Risk Checks
- Idempotency: refund cache key includes `refund`, payment ID, and `Idempotency-Key`; retry returns original response.
- Auth scope: `verify_session` and scope checks happen before mutation, cache writes, or events.
- Event contract: refund event is built through `build_payment_event`, has workflow-matching type, and preserves stable camelCase keys.
- API contract: public response uses camelCase fields and route serialization preserves aliases.
- Status transition: refund status or transition is explicit in `PaymentStatus` and covered by tests.
- Failure paths: rejected requests do not mutate state, do not write idempotency results, and do not emit events.
- Static analysis: do not weaken Ruff, Pyright, Bandit, Pytest, Semgrep, pre-commit, or commit-msg hooks.
- Secret safety: do not read, print, copy, or commit the Qodo API key.

## Completion Notes
- Planning completed with `workshop-plan-from-task`.
- First implementation skill: `workshop-tdd-bdd`.
- Repo rules to apply: `PAY-001`, `PAY-002`, `PAY-003`, `PAY-004`, `PAY-005`, `PAY-006`, `PAY-007`, `PAY-009`, `PAY-010`; setup safety also observes `PAY-008`.
- Qodo comparison: loaded successfully; no conflict with repo-local rules.
- Verification to record after implementation: targeted refund tests, `make verify`, guidelines audit, PR link, Qodo findings, and remediation decisions.
