# 00. Prerequisites

This workshop is local-first. You will use your own machine and your own coding agent.

## Required Tools

- Git
- GitHub account
- GitHub CLI authenticated with `gh auth login`
- Python 3.11+
- `uv`
- Node.js and npm
- A compatible coding agent, such as Codex or Claude Code
- Qodo account

## Verify Setup

Run:

```bash
make doctor
```

If anything fails, paste the output into your coding agent and ask it to fix your local setup.

## Why Local First

The workshop intentionally avoids Codespaces. Real developer workflows happen in local environments with real agent setup, shell quirks, credentials, and toolchain drift. Part of the exercise is learning how to make quality gates explicit enough that your agent can help recover from setup problems without bypassing the workflow.

