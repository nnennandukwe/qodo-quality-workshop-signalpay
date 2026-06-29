# Troubleshooting

## `make doctor` fails

Paste the output into your coding agent and ask it to fix missing local dependencies.

## Qodo API key is missing

Generate a key in the Qodo portal. Then store it in `~/.qodo/config.json` or `QODO_API_KEY`.

Never commit secrets.

## Qodo rules cannot load

Continue with repo-local skills and visible standards:

- `AGENTS.md`
- `skills/payment-idempotency/SKILL.md`
- `.plan/workshop-payment-task/plan.md`

Document the fallback in your PR.

## Qodo review is delayed

Wait a few minutes and refresh the PR. If it still has not posted, follow the instructor PR walkthrough and finish asynchronously.

## Semgrep is slow or unavailable

Semgrep is an optional advanced gate. Run the rest of the ladder:

```bash
make lint
make typecheck
make security
make test
```

## FastAPI `/docs` does not load

Confirm the server is running:

```bash
make run
```

Open:

```text
http://127.0.0.1:8000/docs
```

