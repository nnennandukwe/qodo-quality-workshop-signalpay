# 02. Qodo API Key and Skills

Qodo Skills let your coding agent pull Qodo context before implementation and resolve Qodo PR findings after review.

## Generate an API Key

1. Open the [Qodo portal](https://app.qodo.ai/).
2. Go to your account/API key settings.
3. Generate a personal API key.
4. Do not commit the key.

## Configure Safely

Recommended local config:

```json
{
  "API_KEY": "sk-..."
}
```

Save that as:

```text
~/.qodo/config.json
```

Environment variable alternative:

```bash
export QODO_API_KEY="sk-..."
```

## Install Official Qodo Skills

```bash
npx skills add qodo-ai/qodo-skills/skills
```

Codex invocation:

```text
$qodo-get-rules
$qodo-pr-resolver
```

Claude Code invocation:

```text
/qodo-get-rules
/qodo-pr-resolver
```

## Install Workshop Skills

```bash
make install-skills
```

This copies repo-local skills into `.agents/skills/` and `.claude/skills/`.

## Rules Default

The workshop does not require Qodo portal rules setup. The default rules are
committed in:

```text
rules/README.md
```

Use `qodo-get-rules` only as optional enrichment when it is available.

## Agent Prompt

```text
Configure Qodo Skills for this repo using my Qodo API key.

Do not commit the key.
Use ~/.qodo/config.json or QODO_API_KEY.
Read AGENTS.md and rules/README.md.
Select the relevant repo-local PAY-* rule IDs for the task.
Optionally compare them with qodo-get-rules if Qodo rules are available.
```
