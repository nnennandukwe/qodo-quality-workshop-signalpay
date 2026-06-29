# Agent Instructions

This repo is a Qodo workshop app. Treat it as an exercise in quality-first AI coding.

## Core Workflow

Follow this loop for implementation tasks:

1. Read the task and relevant docs.
2. Read `rules/README.md` and select the repo-local rule IDs that apply.
3. Use `.plan/templates/` to create a high-level plan and execution plan.
4. Write behavior tests before production code when behavior changes.
5. Implement the smallest useful change.
6. Run `make verify`.
7. Do not weaken verification gates to make a change pass.
8. Open a PR and use Qodo review plus PR Resolver for remediation.

Qodo portal rules are optional enrichment. If `qodo-get-rules` is available,
compare those results with the selected repo-local rules, but do not block
planning or implementation on portal rule setup.

## Quality Rules

- Preserve idempotency for payment mutation endpoints.
- Preserve the public API contract shape: camelCase JSON fields and stable event keys.
- Keep authentication and scope checks before state mutation.
- Add or update tests for every behavior change.
- Keep secrets out of git. Never commit Qodo API keys.
- Use Conventional Commits for commit messages.
- Keep `rules/` as committed Markdown. Do not move workshop rules into `.qodo/`.

## Local Commands

- `make run`: start the FastAPI app.
- `make verify`: run lint, typecheck, static analysis, tests, and Semgrep.
- `make doctor`: diagnose local workshop setup.
