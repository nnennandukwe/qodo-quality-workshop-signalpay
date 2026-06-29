---
name: workshop-tdd-bdd
description: "Guide workshop participants through behavior-first TDD: scenarios, failing tests, minimal implementation, and refactor under verification gates."
---

# Workshop TDD BDD

Drive changes from observable behavior, not speculative implementation.

## Workflow

1. Translate the task into Given/When/Then scenarios.
2. Choose the lowest useful test layer.
3. Write one failing test first.
4. Confirm the test fails for the right reason.
5. Implement the minimum code to pass.
6. Repeat for the next behavior.
7. Run `make verify`.

## Scenario Template

```text
Given <starting state>
When <action>
Then <observable result>
```

## Guardrails

- Do not write production code before a targeted failing test.
- Keep failure meaningful; syntax errors are not useful red states.
- Cover at least one happy path and one failure path.
- Assert behavior: response payloads, status codes, emitted events, and persisted state.

## Output

Report:

- scenarios added
- test files changed
- red/green validation
- local gates run
- remaining gaps

