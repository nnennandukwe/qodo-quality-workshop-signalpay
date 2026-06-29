# 04. Local Verification Gates

Local gates are the cheapest useful place to catch deterministic issues.

This step teaches early-and-often verification. Qodo review adds contextual
feedback later, but deterministic issues should be caught before the PR is
opened.

## Gates

| Gate | Command | Purpose |
| --- | --- | --- |
| Ruff lint | `make lint` | Imports, style, correctness, maintainability |
| Pyright | `make typecheck` | Static type and interface issues |
| Bandit | `make security` | Common Python security risks |
| Pytest | `make test` | API behavior |
| Semgrep | `make semgrep` | Workshop-specific static analysis |
| Full ladder | `make verify` | All local gates |

## Static Analysis in This Repo

Static analysis is not one tool. It is a stack of checks with different jobs:

- Ruff catches Python lint, import, naming, and maintainability issues.
- Pyright catches type and interface drift.
- Bandit catches common Python security risks.
- Semgrep catches workshop-specific patterns such as unsafe payment mutation
  behavior.
- Pre-commit reruns selected checks before commits.
- GitHub Actions runs `make verify` again on PRs.

The teaching point is that no single gate understands the whole system. The
workflow layers deterministic checks with behavior tests and then adds Qodo
review for context-aware findings.

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

Do not weaken a gate to keep the workshop moving. If a gate fails, treat the
failure as useful feedback and fix the implementation, tests, or docs.
