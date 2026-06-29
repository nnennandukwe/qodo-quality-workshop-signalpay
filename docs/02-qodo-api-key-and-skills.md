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

## Agent Prompt

```text
Configure Qodo Skills for this repo using my Qodo API key.

Do not commit the key.
Use ~/.qodo/config.json or QODO_API_KEY.
Then verify qodo-get-rules can fetch rules for this repository.
```

