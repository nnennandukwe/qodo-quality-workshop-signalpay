# 03. Read Rules Before Coding

Read repo-local rules before editing code so your agent starts with the right
standards in context. Qodo portal rules are optional enrichment.

## Goal

Bring quality expectations into the planning and implementation loop, not only the final PR review.
The planning output must route the attendee into the correct implementation
skills before any tests or production code are written.

## Prompt

```text
Before writing code, read AGENTS.md and rules/README.md.
Select the relevant PAY-* rule IDs and explain why each applies.
Then read the linked rule documents and repo skills.

Task:
Add a refund or capture-retry workflow while preserving idempotency, auth scope checks, event contract shape, and one-event-per-idempotency-key behavior.

After selecting repo-local rules, optionally compare them with qodo-get-rules if Qodo rules are available.
Summarize which standards must guide the implementation and tests.
Then produce an implementation skill handoff that names workshop-tdd-bdd as the
first implementation skill and includes the exact TDD prompt to run next.
```

## Local Skills to Use

- `workshop-plan-from-task`
- `workshop-tdd-bdd`
- `payment-idempotency`

## Checkpoint

Before coding, you should have:

- selected repo-local `PAY-*` rule IDs
- optional Qodo rules loaded or documented as unavailable
- a high-level plan
- a build-session plan
- an implementation skill handoff that routes the next prompt to `workshop-tdd-bdd`
- the exact TDD prompt to run before any production code
