# 06. PR Resolver Remediation

Use Qodo PR Resolver after Qodo has commented on your pull request.

## Prerequisites

- Current branch has an open PR.
- Qodo has posted review findings.
- GitHub CLI is authenticated.

## Invocation

Codex:

```text
$qodo-pr-resolver
```

Claude Code:

```text
/qodo-pr-resolver
```

## What PR Resolver Should Do

- fetch Qodo findings
- preserve Qodo issue titles and severity
- apply fixes or help you defer with a reason
- reply to inline comments
- post a remediation summary

## Checkpoint

You are done with remediation when:

- every Qodo finding is fixed or explicitly deferred with a reason
- any PR Resolver changes are reviewed before they are kept
- `make verify` passes again after remediation
- the PR includes a short summary of what changed after review

## Human Judgment

You are still accountable for the code. Review the proposed fixes before merge and rerun:

```bash
make verify
```
