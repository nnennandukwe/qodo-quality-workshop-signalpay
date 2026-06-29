# High-Level Plan

## Summary
- Clarify the README instructions for creating the local Qodo config file.
- Keep secrets out of committed files and avoid implying that `QODO_API_URL` is required for normal workshop use.

## Skills Used
- Selected repo-local rules: `PAY-008`, `PAY-009`
- Optional Qodo rules: not loaded; portal rules are optional enrichment for this setup-doc edit
- Repo skills: none
- Local verification gates: `make verify`

## Scope
- In: README Qodo setup copy and local planning artifacts.
- Out: production code, API behavior, credential creation, Qodo portal configuration.

## Behavior Scenarios
- Given a participant has a Qodo API key, when they read the README, then they can create `~/.qodo/config.json` with the expected `API_KEY` shape.
- Given the participant uses the default workshop environment, when they configure Qodo Skills, then they are not told to set `QODO_API_URL`.
- Given an instructor provides a non-production endpoint, when the participant reads the README, then they know `QODO_API_URL` is an optional override.

## Verification Gates
- Tests: not applicable; documentation-only change.
- Lint: covered by `make verify`.
- Typecheck: covered by `make verify`.
- Security/static analysis: covered by `make verify`.
- Repo rule audit: confirm no secrets or local config files are committed.
- Qodo PR review: deferred until PR workflow.

## Failure and Recovery Rules
- Local credentials must fail closed by staying outside git.
- Setup copy must guide recovery by pointing to the safe config file path and optional environment override.

## Commit Plan
- `docs(setup): document qodo config file format`

## Definition of Done
- README shows the minimal local config format.
- README says `QODO_API_URL` is optional for non-production endpoints.
- Local gates pass or failures are reported without weakening gates.

## Assumptions
- The official Qodo Skills default to the production Qodo API when `QODO_API_URL` is not present.
