# Build-Session Execution Plan Template

## Summary
- What will be completed in this session?

## Starting State
- Branch:
- Current local verification:
- Selected repo-local rule IDs:
- Optional Qodo rules status:

## Implementation Skill Handoff
- Planning skill completed: `workshop-plan-from-task`
- First implementation skill to run: `workshop-tdd-bdd`
- Required implementation prompt:
  ```text
  Use the workshop TDD/BDD skill and the plan files just created.
  Write the smallest failing tests first for the selected behavior.
  Cover one happy path and at least one failure path.
  Do not implement production code until the failing tests prove the behavior gap.
  ```
- Conditional skills to keep active during implementation:
  - `payment-idempotency` when changing payment mutation workflows.
  - `workshop-failure-path-testing` when adding or changing failure gates.
- Review/remediation skills:
  - `workshop-guidelines-audit` before committing or opening the PR.
  - optional `workshop-pythonic-review` for changed Python code.
  - optional `qodo-pr-resolver` only after Qodo posts PR findings.

## Execution Steps
1. Read `AGENTS.md` and `rules/README.md`.
2. Select the repo-local `PAY-*` rule IDs for the task.
3. Optionally compare with Qodo rules if available.
4. Choose implementation skills and fill in the Implementation Skill Handoff.
5. Run the `workshop-tdd-bdd` prompt from the handoff.
6. Write failing tests.
7. Implement the smallest production change.
8. Run targeted tests.
9. Run `make verify`.
10. Run `workshop-guidelines-audit`.
11. Commit with Conventional Commits.
12. Push and open PR.
13. Resolve Qodo findings after review.

## Test Plan
- Targeted:
- Full:

## Risk Checks
- Idempotency:
- Auth scope:
- Event contract:
- Static analysis:

## Completion Notes
- What passed:
- What was deferred:
- Which repo rules were applied:
- What Qodo found:
