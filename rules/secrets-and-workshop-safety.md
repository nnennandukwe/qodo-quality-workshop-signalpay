# Secrets and Workshop Safety Rules

Use these rules when configuring Qodo, agent skills, local environments, or
setup docs.

## PAY-008: Qodo API keys, tokens, and local credentials must never be committed

- Trigger: editing setup, Qodo, local-agent, or credential-related files.
- Required behavior: store Qodo API keys only in local config such as
  `~/.qodo/config.json` or a local environment variable. Do not commit keys,
  `.env` files, local config, or generated secret material.
- Verification signal: git diff contains no API keys, `.env` remains ignored,
  and setup docs tell participants how to store keys safely.

## Workshop Safety Notes

- Do not put local secrets under `rules/`.
- Do not depend on `.qodo/` for committed rules because `.qodo/` is ignored for
  local configuration.
- Treat Qodo portal rules as optional enrichment. The committed repo-local
  rules are the default source of truth for this workshop.
