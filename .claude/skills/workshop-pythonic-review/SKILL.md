---
name: workshop-pythonic-review
description: "Review changed Python code for clear, modern, maintainable Python without nitpicking style already covered by Ruff."
---

# Workshop Pythonic Review

Use after implementation and before PR.

## Review Focus

- clear function names
- specific exceptions and preserved causes
- no mutable default arguments
- explicit `is None` checks
- simple control flow
- typed public helpers
- no unnecessary abstraction
- no weakening of tests or gates

## Avoid

- nitpicks that Ruff already handles
- broad rewrites unrelated to the workshop task
- production-scale abstractions for the tiny workshop app

## Output

Report only changed Python files and prioritize correctness over style.

