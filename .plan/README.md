# Planning Templates

Use this directory to make implementation structure explicit before writing code.

In this workshop, planning is a teaching artifact. It shows attendees how to
turn an AI coding task into a quality-controlled work session before an agent
starts editing files.

The plan should answer:

- What behavior are we changing?
- Which repo-local rules apply?
- Which skills should guide the agent?
- Which tests prove the expected behavior?
- Which gates must pass before review?
- What evidence belongs in the PR?

Start with:

- `templates/high-level-plan.md`
- `templates/build-session-execution-plan.md`

Workshop task example:

- `workshop-payment-task/plan.md`
- `workshop-payment-task/build-session-execution-plan.md`

Education docs example:

- `workshop-education-docs/plan.md`
- `workshop-education-docs/build-session-execution-plan.md`

This directory is committed for the workshop even though many production repos keep `.plan/` gitignored.

## What Each Plan Type Teaches

| File | What it is for | Why it matters |
| --- | --- | --- |
| `high-level-plan.md` | Captures intent, rules, scenarios, risks, gates, and done criteria. | Keeps the agent aligned to the system contract, not only the next code edit. |
| `build-session-execution-plan.md` | Converts the plan into an ordered implementation session. | Gives the agent a concrete path from setup to tests, implementation, verification, and PR review. |

The plans are not meant to be long for their own sake. They are meant to be decision-complete enough that an attendee or agent can explain the next step and the quality reason behind it.
