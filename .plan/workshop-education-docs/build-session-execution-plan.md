# Workshop Education Docs Build-Session Plan

## Summary
- Add the education layer promised by the workshop: repository tour, planning explanation, rules and skills teaching, static analysis context, and Qodo review proof boundaries.

## Starting State
- Branch: current working branch.
- Current local verification: not run before this docs pass.
- Selected repo-local rule IDs: `PAY-008`, `PAY-009`.
- Optional Qodo rules status: not loaded; Qodo-hosted rules are optional enrichment.

## Execution Steps
1. Update `tests/test_workshop_structure.py` so missing education docs fail first.
2. Create `.plan/workshop-education-docs/` planning artifacts.
3. Add `docs/07-workshop-teaching-guide.md`.
4. Add `skills/README.md`.
5. Expand `README.md` with repo structure and quality-loop teaching sections.
6. Expand `.plan/README.md` and both templates with section purpose and value notes.
7. Expand rules and workflow docs to explain local rules, optional Qodo-hosted rules and skills, static analysis, CI, PR review evidence, and remediation.
8. Run `uv run pytest tests/test_workshop_structure.py -q`.
9. Run `make verify`.
10. Review the diff for docs-only scope, broken links, secrets, and Qodo proof overclaims.

## Test Plan
- Targeted: `uv run pytest tests/test_workshop_structure.py -q`.
- Full: `make verify`.
- Manual: `git diff --stat`, Markdown link scan by inspection, and app-file check.

## Risk Checks
- Secrets: no API keys, tokens, `.env`, or local Qodo config content in docs.
- App behavior: no edits to `src/signalpay_api/` or payment behavior tests except the workshop structure test.
- Qodo claims: describe hosted rules and skills as optional unless review evidence proves usage.
- Verification: do not skip or weaken gates to make the docs pass.

## Completion Notes
- Local verification:
- Repo rules applied: `PAY-008`, `PAY-009`
- Qodo review:
- Remediation:
