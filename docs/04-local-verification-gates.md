# 04. Local Verification Gates

Local gates are the cheapest useful place to catch deterministic issues.

## Gates

| Gate | Command | Purpose |
| --- | --- | --- |
| Ruff lint | `make lint` | Imports, style, correctness, maintainability |
| Pyright | `make typecheck` | Static type and interface issues |
| Bandit | `make security` | Common Python security risks |
| Pytest | `make test` | API behavior |
| Semgrep | `make semgrep` | Workshop-specific static analysis |
| Full ladder | `make verify` | All local gates |

## Checkpoint

You are ready to open a PR when:

- targeted tests for the changed behavior pass
- `make verify` passes without disabling or loosening any gate
- any earlier failure is classified and fixed in the implementation or tests
- your notes or PR description include the verification command you ran

## Agent Prompt

```text
Run the full local verification ladder.

If anything fails, classify the failure as formatting, linting, type checking, security/static analysis, behavior, or repo guideline compliance.
Fix the issue without weakening the gate.
Re-run verification.
```

## Principle

Qodo does not replace deterministic gates. Qodo adds context-aware review on top of tests, linters, type checks, and static analysis.
