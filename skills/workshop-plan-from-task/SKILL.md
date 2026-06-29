---
name: workshop-plan-from-task
description: "Turn a coding task into a high-level plan and a build-session execution plan before implementation starts."
---

# Workshop Plan From Task

Use this skill before writing production code.

## Workflow

1. Read the task.
2. Read `AGENTS.md`.
3. Read relevant domain skills, especially `skills/payment-idempotency/SKILL.md`.
4. Run or request Qodo rules if available.
5. Create or update:
   - `.plan/workshop-payment-task/plan.md`
   - `.plan/workshop-payment-task/build-session-execution-plan.md`

## Plan Requirements

Include:

- Summary
- Skills used
- Scope and out-of-scope items
- Given/When/Then behavior scenarios
- Verification gates
- Failure and recovery rules
- Commit plan
- Definition of done
- Assumptions

## Guardrails

- Do not write implementation code during planning.
- Do not skip tests because the task seems small.
- Do not weaken local gates.
- Do not store secrets in plan files.

