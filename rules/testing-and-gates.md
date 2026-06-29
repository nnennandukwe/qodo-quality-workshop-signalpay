# Testing and Verification Gate Rules

Use these rules for every implementation task in the workshop.

## PAY-007: Behavior changes require success and failure-path tests

- Trigger: changing endpoint behavior, state transitions, auth behavior, or
  emitted events.
- Required behavior: write tests before production code for at least one happy
  path and one failure path. Payment mutation tasks must include missing or
  invalid auth, missing idempotency key, and retry behavior where relevant.
- Verification signal: targeted tests fail before implementation and pass after
  implementation.

## PAY-009: Local verification gates must not be weakened to pass a task

- Trigger: any failing local gate.
- Required behavior: fix the implementation or tests without disabling Ruff,
  Pyright, Bandit, Pytest, Semgrep, pre-commit, or Conventional Commit checks.
- Verification signal: `make verify` passes and any gate failure is explained
  in the PR or workshop notes.

## Verification Ladder

Run the full ladder before opening a PR:

```bash
make lint
make typecheck
make security
make test
make semgrep
make verify
```
