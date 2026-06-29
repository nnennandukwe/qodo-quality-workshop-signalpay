# Workshop Education Docs Plan

## Summary
- Convert the workshop docs from a setup runbook into a guided lesson on quality-first AI coding.
- Keep the change documentation-only: no FastAPI routes, payment contracts, tests for payment behavior, or credential handling code changes.
- Teach how planning, repo-local rules, repo-local skills, deterministic gates, CI, Qodo review, and PR Resolver form one quality loop across the SDLC and ADLC.

## Selected Repo Rules
- `PAY-008` because this pass explains Qodo API keys, local credentials, and safe skill setup.
- `PAY-009` because the docs must preserve the expectation that local gates are not weakened or skipped to make progress.

## Optional Qodo Rules
- Loaded: no.
- Differences from repo rules: not compared for this docs-only pass. Repo-local rules remain the default workshop source of truth; Qodo-hosted rules are optional enrichment for attendees with portal access.

## Skill Routing
- Planning skill used: `workshop-plan-from-task`.
- Implementation entry skill: not required because this is a documentation-only education pass.
- Review skills:
  - `workshop-guidelines-audit` for checking the diff against `AGENTS.md`, `rules/`, and the docs-only scope.
  - `workshop-pythonic-review` is not applicable because no Python application code should change.
- Optional post-review skill: `qodo-pr-resolver` only after Qodo posts PR findings.

## Scope
In:
- Add teaching docs that explain repo structure, planning templates, local rules, local skills, static analysis, CI, Qodo review, and remediation.
- Add structural tests for the new education artifacts.
- Keep claims about Qodo skill usage tied to review evidence such as `Skill insights`, visible skills/context sections, or Qodo comments.

Out:
- Payment workflow implementation.
- API response or event-contract changes.
- Qodo portal configuration or committed credentials.
- Slide deck edits.

## Behavior Scenarios
- Given an attendee opens the repo, when they read the README, then they understand what each top-level directory contributes to the quality loop.
- Given an attendee opens `.plan/templates/`, when they read a template, then they understand what each section is for and why it matters before coding.
- Given an attendee wants Qodo-hosted rules or skills, when they read the docs, then they understand that local rules and skills are the default source and Qodo hosting is optional enrichment.
- Given a presenter explains review-stage evidence, when they describe Qodo skill usage, then they avoid claiming a skill influenced review unless the review surface shows that evidence.

## Verification Gates
- Targeted: `uv run pytest tests/test_workshop_structure.py -q`.
- Full: `make verify`.
- Manual: inspect Markdown links, verify no secrets in the diff, and confirm the app code remains untouched.

## Failure and Recovery Rules
- If a docs link points to a missing file, add or correct the linked file rather than removing the learning path.
- If a verification gate fails, fix the docs or tests without weakening the gate.
- If Qodo setup is unavailable, keep the fallback path explicit: local rules, local skills, local gates, and instructor PR walkthrough.

## Commit Plan
- `test(workshop): require education docs`
- `docs(workshop): add quality-loop teaching guide`

## Definition of Done
- The repo includes a presenter-ready teaching guide and skill index.
- The README explains the repo structure and SDLC/ADLC quality loop.
- Plan templates teach the value of each section.
- Structure tests and `make verify` pass.

## Assumptions
- The workshop should support live facilitation and async catch-up.
- The educational layer should be concise enough to present in a few minutes, with deeper detail available in docs.
