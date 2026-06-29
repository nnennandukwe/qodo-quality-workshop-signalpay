# Verify Warning Cleanup Build-Session Plan

## Summary
Resolve the pytest warning by installing the dependency expected by Starlette's
test client and adding a narrow verification guard so this warning class cannot
quietly return.

## Starting State
- Branch: existing local branch.
- Current local verification: `.venv/bin/pytest -q` passed with 16 tests and one
  `StarletteDeprecationWarning`.
- Selected repo-local rule IDs: `PAY-007`, `PAY-008`, `PAY-009`
- Optional Qodo rules status: loaded successfully; no conflict with repo-local
  rules.

## Implementation Skill Handoff
- Planning skill completed: `workshop-plan-from-task`
- First implementation skill to run: local TDD/verification loop
- Required implementation prompt:
  ```text
  Add the smallest dependency/config change that removes the Starlette
  TestClient deprecation warning. Do not suppress the warning broadly. Run
  targeted pytest first, then make verify.
  ```

## Execution Steps
1. Inspect the current warning and the installed Starlette `testclient` import
   path.
2. Add `httpx2` through `uv` so `pyproject.toml`, `uv.lock`, and `.venv` remain
   consistent.
3. Add a narrow pytest warning gate for `StarletteDeprecationWarning`.
4. Run `.venv/bin/pytest -q` and confirm zero warnings.
5. Run `make verify`.
6. Review the diff for unrelated changes and secret leakage.

## Test Plan
- Targeted: `.venv/bin/pytest -q`
- Full: `make verify`

## Risk Checks
- Idempotency: no payment mutation behavior changes.
- Auth scope: no auth behavior changes.
- Event contract: no event behavior changes.
- Static analysis: pytest warning handling is tightened, not weakened.
- Secret safety: no Qodo API keys or local credentials are added.

## Completion Notes
- `.venv/bin/pytest -q`: passed with 16 tests and no warnings.
- `make verify`: passed Ruff, Pyright, Bandit, Pytest, and Semgrep.
- Repo rules applied: `PAY-007`, `PAY-008`, `PAY-009`.
- Qodo comparison: loaded successfully; hosted rules aligned with repo-local
  rules and did not require additional changes.
