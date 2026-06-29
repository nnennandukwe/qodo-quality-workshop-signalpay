# Agent Skill Install Target

Run this from the repo root:

```bash
make install-skills
```

That copies the curated workshop skills from `skills/` into this directory for Codex-style project-local discovery and into `.claude/skills/` for Claude Code-style project-local discovery.

Official Qodo Skills are installed separately:

```bash
npx skills add qodo-ai/qodo-skills/skills
```

