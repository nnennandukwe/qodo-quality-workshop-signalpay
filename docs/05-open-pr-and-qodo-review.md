# 05. Open a PR and Let Qodo Review

Once local gates pass, open a pull request so Qodo can review the change in GitHub.

## Commands

```bash
git checkout -b feat/payment-workflow
git add .
git commit -m "feat(payments): add refund workflow"
git push -u origin feat/payment-workflow
gh pr create --fill
```

## Checkpoint

You are ready for review when:

- the branch is pushed to your fork
- the PR is open against the workshop repo
- local verification has passed before Qodo review starts
- the PR description includes the selected `PAY-*` rules and verification evidence

## What to Look For

In the Qodo review, inspect:

- bugs
- rule violations
- skill insights
- context used
- remediation guidance
- PR summary

## Principle

The PR gate should not be the first time quality is checked. It should be the independent review layer after planning, tests, and local deterministic gates.
