# Qodo Quality-First AI Coding Workshop

This repo is the source of truth for a one-hour hands-on workshop on building a quality-first AI coding workflow with Qodo.

You will practice this loop:

```text
plan -> read repo rules -> use repo skills -> write tests -> implement -> run local gates -> open PR -> Qodo review -> PR Resolver remediation
```

## What You Are Building

This is a self-contained FastAPI payments API used to practice quality-first AI coding.

It has no separate frontend and no external service dependencies. You will interact with the app through FastAPI's browser docs at `/docs`.

The goal is not to build a production payment system. The goal is to practice a repeatable workflow:

```text
plan -> read repo rules -> write tests -> implement -> run local gates -> open PR -> review with Qodo -> resolve findings
```

## Workshop App

Run the app locally:

```bash
make setup
make run
```

Open:

```text
http://127.0.0.1:8000/docs
```

Also available:

```text
http://127.0.0.1:8000/redoc
http://127.0.0.1:8000/openapi.json
```

This workshop app is API-first. The browser UI is FastAPI `/docs`, not a separate React dashboard.

## Choose Your Lane

- **Hands-on:** fork, clone, configure Qodo, make the change, open a PR.
- **Pair/observe:** follow the README and inspect the gates while someone else codes.
- **Async later:** use this repo as a complete guided workshop after the session.

## One-Hour Flow

| Time | Activity |
| --- | --- |
| 0-5 min | Frame quality-first AI coding: deterministic gates + repo rules/skills + Qodo PR review. |
| 5-10 min | Open this README, choose a lane, fork and clone. |
| 10-15 min | Run `make doctor`; let your coding agent troubleshoot setup. |
| 15-22 min | Sign into Qodo, connect GitHub, generate a Qodo API key. |
| 22-28 min | Configure Qodo Skills safely with agent help. |
| 28-34 min | Read repo-local rules, optionally compare Qodo rules, and use repo skills before coding. |
| 34-43 min | Write behavior tests and implement the payment workflow change. |
| 43-50 min | Run lint, typecheck, static analysis, tests, and pre-commit. |
| 50-56 min | Commit, push, open PR, inspect Qodo review. |
| 56-60 min | Run PR Resolver or inspect the prepared remediation flow. |

## Quality Gate Checkpoints

Use these checkpoints to know what you have completed at each step. Each gate
should leave behind visible proof that the workflow is moving forward.

- **Setup gate:** `make doctor`, `make setup`, and starter `make verify` run
  successfully. You have a working local repo before asking an agent to change
  application behavior.
- **Qodo access gate:** your fork is connected to Qodo, your API key is stored
  outside git, and official plus repo-local skills are installed or documented
  as unavailable. You have a review layer ready without committing credentials.
- **Standards gate:** the relevant `PAY-*` rules are selected, linked rule docs
  are read, repo skills are identified, and optional Qodo rule status is
  recorded. You have turned the task into explicit quality constraints.
- **Planning and TDD gate:** the high-level plan, build-session execution plan,
  and smallest useful failing behavior tests are identified or written. You
  have made the expected behavior observable before production code changes.
- **Local verification gate:** targeted tests and `make verify` pass without
  disabling Ruff, Pyright, Bandit, Pytest, Semgrep, or commit checks. You have
  deterministic evidence that the change preserves the local contract.
- **PR review and remediation gate:** the PR is open, Qodo findings are
  inspected, fixes or deferrals are documented, and `make verify` is rerun after
  remediation. You have completed the review loop rather than stopping at a
  passing local run.

## Prerequisites

Read [docs/00-prerequisites.md](docs/00-prerequisites.md).

Required:

- Git
- GitHub account
- GitHub CLI authenticated with `gh auth login`
- Python 3.11+
- `uv`
- Node.js and npm
- A coding agent such as Codex, Claude Code, Cursor, Windsurf, or Cline
- Qodo account

## Setup

```bash
git clone <your-fork-url>
cd qodo-quality-workshop-signalpay
make doctor
make setup
make verify
```

If setup fails, paste the `make doctor` output into your coding agent and ask it to fix your local environment.

## Qodo Setup

1. Sign into the [Qodo portal](https://app.qodo.ai/).
2. Connect GitHub to your fork.
3. Generate an API key from the Qodo portal.
4. Ask your coding agent to configure Qodo Skills.

For normal workshop use, store the key in a local-only Qodo config file:

```json
{
  "API_KEY": "sk-..."
}
```

Save it at:

```text
~/.qodo/config.json
```

Qodo Skills default to the production Qodo API. Set `QODO_API_URL` in this
file only if your instructor gives you a non-production Qodo API endpoint.

Read:

- [docs/01-qodo-portal-github.md](docs/01-qodo-portal-github.md)
- [docs/02-qodo-api-key-and-skills.md](docs/02-qodo-api-key-and-skills.md)

Install official Qodo Skills:

```bash
npx skills add qodo-ai/qodo-skills/skills
```

Install repo-local workshop skills:

```bash
make install-skills
```

## Repo-Local Rules

The default pre-coding context is committed in [rules/README.md](rules/README.md).
Qodo portal rules are optional enrichment. Do not block the workshop on portal
rule setup.

## Hands-On Task: Payment Workflow Safety

Your task is to add one small payment workflow: either a refund workflow or capture-retry handling. Choose one path for the workshop; do not try to build both.

This is intentionally a small change with production-shaped risk. Payment mutations are where AI-generated code can look correct while quietly breaking system guarantees. A retry can emit a duplicate event, a missing idempotency key can create duplicate work, an auth check can happen after state changes, or a response can drift from the public API contract.

The point of this exercise is to practice making an agent work inside a quality system before it writes code. You will force the agent to read local rules, select the `PAY-*` standards that apply, use the payment-idempotency skill, write behavior tests first, run deterministic gates, and then compare the result with Qodo review feedback.

By the end, you should be able to see the difference between "the agent changed files" and "the agent produced a change that preserved the system contract." The expected output is a small PR with tests, verification evidence, and a review/remediation loop, not a large feature.

Preserve these guarantees:

- idempotency
- auth scope checks
- event contract shape
- one-event-per-idempotency-key behavior

Use this task as the input for the setup, planning, TDD, and verification prompts below.

Read [docs/03-run-rules-before-coding.md](docs/03-run-rules-before-coding.md), then start from:

- [.plan/workshop-payment-task/plan.md](.plan/workshop-payment-task/plan.md)
- [.plan/workshop-payment-task/build-session-execution-plan.md](.plan/workshop-payment-task/build-session-execution-plan.md)

## Definition of Done

The workshop task is complete when you have a small PR that includes:

- selected repo-local rules and optional Qodo rule status
- behavior tests and verification evidence
- a passing `make verify` run without weakened gates
- Qodo review evidence or the documented fallback path
- remediation notes for fixed or intentionally deferred findings

## Copy/Paste Agent Prompts

### Setup Prompt

```text
Help me configure this repo for the Qodo workshop.

I have a Qodo API key from the Qodo portal.

Requirements:
- Do not commit the API key.
- Store it only in a safe local developer location or environment variable.
- Install or verify Qodo Skills.
- Read `AGENTS.md` and `rules/README.md`.
- Select the relevant repo-local rule IDs for the Hands-On Task and explain why each applies.
- Optionally compare those rules with qodo-get-rules if Qodo rules are available.
- If my local environment is missing dependencies, diagnose and fix them.
```

### Planning Prompt

```text
Use the repo-local workshop planning skill to turn the Hands-On Task in README.md into:
1. a high-level implementation plan
2. a build-session execution plan

Use `AGENTS.md`, `rules/README.md`, selected `PAY-*` rules, and the
payment-idempotency skill as constraints.
The plan must include an implementation skill handoff that names the first
implementation skill and the exact TDD prompt to run next.
Treat qodo-get-rules as optional enrichment if available.
Do not write code yet.
```

### TDD Prompt

Run this only after the planning prompt has produced the high-level plan,
build-session execution plan, and implementation skill handoff.

```text
Use the workshop TDD/BDD skill.

Use the plan files just created.
Write the smallest failing tests first for the selected payment workflow path.
Cover one happy path and at least one failure path.
Do not implement production code until the failing tests prove the behavior gap.
```

### Verification Prompt

```text
Run the full local verification ladder.

If anything fails, classify the failure as formatting, linting, type checking, security/static analysis, behavior, or repo guideline compliance.
Fix the issue without weakening the gate.
Re-run verification.
```

## Local Verification Gates

Run individual gates:

```bash
make lint
make typecheck
make security
make test
make semgrep
```

Run the full ladder:

```bash
make verify
```

Read [docs/04-local-verification-gates.md](docs/04-local-verification-gates.md).

## Open a PR and Let Qodo Review

```bash
git checkout -b feat/payment-workflow
git add .
git commit -m "feat(payments): add refund workflow"
git push -u origin feat/payment-workflow
gh pr create --fill
```

Read:

- [docs/05-open-pr-and-qodo-review.md](docs/05-open-pr-and-qodo-review.md)
- [docs/06-pr-resolver-remediation.md](docs/06-pr-resolver-remediation.md)

## Slides

The live companion deck is linked from [slides/README.md](slides/README.md).

## Fallbacks

- Local setup failing? Paste `make doctor` output into your coding agent.
- Qodo API setup failing? Continue with repo skills, local gates, and the instructor demo.
- Qodo review delayed? Use the prepared instructor PR: [Instructor demo: red refund workflow gate](https://github.com/nnennandukwe/qodo-quality-workshop-signalpay/pull/1).
- Behind the room? Continue asynchronously from this README.
