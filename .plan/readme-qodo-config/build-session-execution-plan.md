# Build-Session Execution Plan

## Summary
- Add inline README guidance for creating `~/.qodo/config.json` safely.

## Starting State
- Branch: `main`
- Current local verification: not run before edit
- Selected repo-local rule IDs: `PAY-008`, `PAY-009`
- Optional Qodo rules status: not loaded; portal rules are optional enrichment for this setup-doc edit

## Execution Steps
1. Read `AGENTS.md` and `rules/README.md`.
2. Select the repo-local `PAY-*` rule IDs for the task.
3. Read `PAY-008` and `PAY-009`.
4. Add the minimal README config example.
5. Note that `QODO_API_URL` is optional and instructor-provided only for non-production endpoints.
6. Run `make verify`.
7. Report results and any deferred PR/Qodo review work.

## Test Plan
- Targeted: documentation review for config path, config shape, and optional URL wording.
- Full: `make verify`.

## Risk Checks
- Idempotency: not affected.
- Auth scope: not affected.
- Event contract: not affected.
- Static analysis: `make verify`.

## Completion Notes
- What passed: `make verify`
- What was deferred: commit, push, PR, and Qodo review unless requested
- Which repo rules were applied: `PAY-008`, `PAY-009`
- What Qodo found: not run
