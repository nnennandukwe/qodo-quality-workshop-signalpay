# High-Level Plan Template

## Summary
- What problem are we solving?
- What quality constraints matter?

## Skill Routing
- Selected repo-local rules:
- Optional Qodo rules:
- Planning skill used: `workshop-plan-from-task`
- Implementation entry skill: `workshop-tdd-bdd`
- Conditional implementation skills:
  - `payment-idempotency` when changing payment mutation workflows.
  - `workshop-failure-path-testing` when adding or changing failure gates.
- Pre-PR review skills:
  - `workshop-guidelines-audit`
  - optional `workshop-pythonic-review` for changed Python code
- Post-review skill: optional `qodo-pr-resolver` after Qodo posts PR findings.
- Exact next prompt after planning:
  ```text
  Use the workshop TDD/BDD skill and the plan files just created.
  Write the smallest failing tests first for the selected behavior.
  Do not implement production code until the failing tests prove the behavior gap.
  ```
- Local verification gates:

## Scope
- In:
- Out:

## Behavior Scenarios
- Given ...
- When ...
- Then ...

## Verification Gates
- Tests:
- Lint:
- Typecheck:
- Security/static analysis:
- Repo rule audit:
- Qodo PR review:

## Failure and Recovery Rules
- What must fail closed?
- What error message should guide recovery?

## Commit Plan
- `test(scope): ...`
- `feat(scope): ...`
- `docs(scope): ...`

## Definition of Done
- Local gates pass.
- PR review is addressed.
- Human reviewer can understand the risk.

## Assumptions
- ...
