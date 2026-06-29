# 03. Read Rules Before Coding

Read repo-local rules before editing code so your agent starts with the right
standards in context. Qodo portal rules are optional enrichment.

## Goal

Bring quality expectations into the planning and implementation loop, not only the final PR review.
The planning output must route the attendee into the correct implementation
skills before any tests or production code are written.

This is the first major lesson in the workshop: the agent should not discover
quality standards after it has already produced a diff. Rules and skills belong
in the prompt context before coding starts.

Repo-local rules are always available. Qodo-hosted rules can add review-stage
coverage when configured, but they are not required to complete the learning
loop.

## What This Step Teaches

| Artifact | Teaching value |
| --- | --- |
| `AGENTS.md` | The operating contract for agents in this repo. |
| `rules/README.md` | The index that maps task types to `PAY-*` standards. |
| Linked rule docs | The exact behavior and verification signal for each standard. |
| `skills/payment-idempotency/SKILL.md` | The procedure that keeps payment mutation risk in working memory. |
| `.plan/` | The place where selected rules become scenarios, tests, gates, and handoffs. |

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

Use `workshop-plan-from-task` first. It should produce a high-level plan and a
build-session execution plan. The plan must then hand off to
`workshop-tdd-bdd` so tests come before production code.

## Checkpoint

Before coding, you should have:

- selected repo-local `PAY-*` rule IDs
- optional Qodo rules loaded or documented as unavailable
- a high-level plan
- a build-session plan
- an implementation skill handoff that routes the next prompt to `workshop-tdd-bdd`
- the exact TDD prompt to run before any production code
