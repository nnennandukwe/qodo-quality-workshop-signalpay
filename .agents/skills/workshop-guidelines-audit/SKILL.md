---
name: workshop-guidelines-audit
description: "Audit the current diff against AGENTS.md, repo-local rules, repo-local skills, optional Qodo rules, and workshop quality gates before opening a PR."
---

# Workshop Guidelines Audit

Use this skill before committing and before opening a PR.

## Sources

Read:

- `AGENTS.md`
- `rules/README.md`
- selected linked rule documents under `rules/`
- `skills/payment-idempotency/SKILL.md`
- optional loaded Qodo rules
- `.plan/workshop-payment-task/plan.md`

## Audit Checklist

- Did the change preserve idempotency?
- Did the plan identify the selected repo-local `PAY-*` rules?
- Did the change preserve event contract shape?
- Did tests cover success and failure paths?
- Did local gates run?
- Did the plan capture assumptions and verification evidence?
- Are secrets absent from the diff?

## Report Format

```markdown
## Workshop Guidelines Audit

### Must Fix
- ...

### Should Fix
- ...

### Passing
- ...

### Verification Evidence
- ...
```

Do not modify code unless explicitly asked.
