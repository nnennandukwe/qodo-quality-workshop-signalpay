# 05. Open a PR and Let Qodo Review

Once local gates pass, open a pull request so Qodo can review the change in GitHub.

The teaching point is that the PR is an independent review layer, not the first
quality check. By this point, the change should already have selected rules,
tests, local verification, and a clear PR description.

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

## Evidence Language

Be specific about what the review proves:

- Repo-local rules and skills are present when they are committed in this repo.
- The agent used a local skill when the prompt, plan, or agent notes show that usage.
- Qodo used a skill in review only when the review surface shows evidence such
  as `Skill insights`, a visible skills/context section, or a Qodo comment that
  names the skill.

This keeps the workshop evidence-based. Do not collapse repo-local rules,
Qodo-hosted rules, local skills, and review-stage skill evidence into one claim.

## Principle

The PR gate should not be the first time quality is checked. It should be the independent review layer after planning, tests, and local deterministic gates.
