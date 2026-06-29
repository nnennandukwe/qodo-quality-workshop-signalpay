# 03. Read Rules Before Coding

Read repo-local rules before editing code so your agent starts with the right
standards in context. Qodo portal rules are optional enrichment.

## Goal

Bring quality expectations into the planning and implementation loop, not only the final PR review.

## Prompt

```text
Before writing code, read AGENTS.md and rules/README.md.
Select the relevant PAY-* rule IDs and explain why each applies.
Then read the linked rule documents and repo skills.

Task:
Add a refund or capture-retry workflow while preserving idempotency, auth scope checks, event contract shape, and one-event-per-idempotency-key behavior.

After selecting repo-local rules, optionally compare them with qodo-get-rules if Qodo rules are available.
Summarize which standards must guide the implementation and tests.
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
- failing tests identified or written
