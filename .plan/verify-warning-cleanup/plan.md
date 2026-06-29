# Verify Warning Cleanup Plan

## Summary
Remove the Starlette deprecation warning emitted by `fastapi.testclient` during
pytest collection without suppressing meaningful warnings or weakening local
verification gates.

## Skill Routing
- Selected repo-local rules: `PAY-007`, `PAY-008`, `PAY-009`
- Optional Qodo rules: loaded with `qodo-get-rules`; 13 hosted rules returned
  and aligned with test coverage, gate integrity, and secret safety.
- Planning skill used: `workshop-plan-from-task`
- Implementation entry skill: local TDD/verification loop
- Local verification gates: targeted pytest and `make verify`

## Scope
In:
- Add the dependency Starlette now expects for `TestClient`.
- Keep pytest warning handling strict for Starlette deprecations.
- Preserve all existing payment behavior and tests.

Out:
- Payment workflow behavior changes.
- Suppressing the warning with broad ignore filters.
- Editing unrelated refund workflow files already present in the worktree.

## Behavior Scenarios
- Given the test suite imports `fastapi.testclient.TestClient`, when pytest
  collects and runs tests, then no Starlette deprecation warning is emitted.
- Given a future Starlette deprecation warning appears, when pytest runs, then
  the warning fails the test run instead of being hidden.

## Verification Gates
- Tests: `.venv/bin/pytest -q`
- Full gate: `make verify`
- Repo rule audit: confirm the diff adds no secrets and does not weaken gates.

## Failure and Recovery Rules
- Do not hide the warning with a broad ignore filter.
- Do not remove or loosen existing tests.
- Do not commit local Qodo credentials or generated secret material.

## Commit Plan
- `fix(tests): install starlette testclient dependency`

## Definition of Done
- Pytest passes with zero warnings.
- `make verify` passes.
- Diff contains only the dependency/config/plan changes needed for this warning.

## Assumptions
- `httpx2` is the intended replacement because the installed Starlette
  `testclient` imports `httpx2` first and only warns when falling back to
  `httpx`.
