# 03. Run Rules Before Coding

Run Qodo rules before editing code so your agent starts with the right standards in context.

## Goal

Bring quality expectations into the planning and implementation loop, not only the final PR review.

## Prompt

```text
Before writing code, use Qodo rules and the repo skills to understand the quality standards for this task.

Task:
Add a refund or capture-retry workflow while preserving idempotency, auth scope checks, event contract shape, and one-event-per-idempotency-key behavior.

After loading the rules, summarize which standards must guide the implementation.
```

## Local Skills to Use

- `workshop-plan-from-task`
- `workshop-tdd-bdd`
- `payment-idempotency`

## Checkpoint

Before coding, you should have:

- Qodo rules loaded or a documented fallback if Qodo access is blocked
- a high-level plan
- a build-session plan
- failing tests identified or written

