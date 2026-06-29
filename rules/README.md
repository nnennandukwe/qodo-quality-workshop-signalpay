# Repo-Local Rules

These are the default coding rules for the workshop. Read these before writing
code. Qodo portal rules are optional enrichment, but these committed rules are
always available to humans and coding agents.

## Why These Rules Are in the Repo

Rules are committed as Markdown so the quality standard is visible before any
tooling is configured. Attendees can read them, coding agents can ingest them,
and reviewers can point to the exact rule that shaped a test or implementation
choice.

This is the first quality gate in the workshop. Before an agent writes code, it
should know the payment safety rules that must not regress.

Teams can also host equivalent rules in Qodo so the same standards are available
at review time. In this repo, Qodo-hosted rules are optional enrichment; the
repo-local rules remain the reliable default source of truth.

## How to Use These Rules

1. Read `AGENTS.md`.
2. Read this file.
3. Select the rule IDs that apply to the task.
4. Read the linked rule documents.
5. Explain how the selected rules change the plan and tests.
6. Optionally compare with Qodo rules if `qodo-get-rules` is available.

When teaching this step, ask attendees to connect each selected rule to a test
or review signal. A rule is useful when it changes the plan, changes the test
coverage, or gives reviewers a concrete standard to check.

## How Rules, Skills, and Qodo Fit Together

| Layer | Where it lives | What it contributes |
| --- | --- | --- |
| Repo-local rules | `rules/` | The baseline standards every attendee and agent can read. |
| Repo-local skills | `skills/` | Procedures that tell the agent how to work under those standards. |
| Optional Qodo rules | Qodo portal | Review-time standards that can mirror or extend the repo-local rules. |
| Optional Qodo skills | Qodo Skills | Review or remediation workflows that can use team procedures when configured. |

Only claim Qodo used a hosted skill or rule when the review surface shows that
evidence. Otherwise, describe the local rules and skills as the workshop
baseline and Qodo-hosted context as optional enrichment.

## Rule Index

| Rule ID | Title | Rule document |
| --- | --- | --- |
| `PAY-001` | Payment mutation endpoints require `Idempotency-Key` | [payment-mutations.md](payment-mutations.md) |
| `PAY-002` | Auth and required scope checks happen before mutation | [auth-and-sessions.md](auth-and-sessions.md) |
| `PAY-003` | Idempotency cache keys include operation, payment ID, and idempotency key | [payment-mutations.md](payment-mutations.md) |
| `PAY-004` | Retried mutation returns the original response and emits no duplicate event | [payment-mutations.md](payment-mutations.md) |
| `PAY-005` | Public API responses use stable camelCase JSON fields | [api-and-events.md](api-and-events.md) |
| `PAY-006` | Payment events use `build_payment_event` and preserve stable event keys | [api-and-events.md](api-and-events.md) |
| `PAY-007` | Behavior changes require success and failure-path tests | [testing-and-gates.md](testing-and-gates.md) |
| `PAY-008` | Qodo API keys, tokens, and local credentials must never be committed | [secrets-and-workshop-safety.md](secrets-and-workshop-safety.md) |
| `PAY-009` | Local verification gates must not be weakened to pass a task | [testing-and-gates.md](testing-and-gates.md) |
| `PAY-010` | New payment statuses or transitions must be explicit and tested | [api-and-events.md](api-and-events.md) |

## Task-to-Rule Selection Matrix

| Task type | Required rules |
| --- | --- |
| Add refund workflow | `PAY-001`, `PAY-002`, `PAY-003`, `PAY-004`, `PAY-005`, `PAY-006`, `PAY-007`, `PAY-009`, `PAY-010` |
| Add capture retry behavior | `PAY-001`, `PAY-002`, `PAY-003`, `PAY-004`, `PAY-007`, `PAY-009` |
| Change API response shape | `PAY-005`, `PAY-006`, `PAY-007`, `PAY-009`, `PAY-010` |
| Change auth/session handling | `PAY-002`, `PAY-007`, `PAY-009` |
| Add or edit tests only | `PAY-007`, `PAY-009` |
| Configure Qodo or local agents | `PAY-008`, `PAY-009` |

## Required Agent Summary

Before coding, write a short summary with this shape:

```text
Selected repo rules:
- PAY-001 because ...
- PAY-002 because ...

Optional Qodo rules:
- Loaded: yes/no
- Differences from repo rules: ...

Rule-driven tests:
- ...
```
