#!/usr/bin/env bash
set -euo pipefail

missing=0

check() {
  local label="$1"
  local command="$2"
  if command -v "$command" >/dev/null 2>&1; then
    printf "ok: %s (%s)\n" "$label" "$("$command" --version 2>/dev/null | head -1)"
  else
    printf "missing: %s (%s)\n" "$label" "$command"
    missing=1
  fi
}

check "git" git
check "GitHub CLI" gh
check "uv" uv
check "node" node
check "npm" npm

if [ -n "${QODO_API_KEY:-}" ]; then
  echo "ok: QODO_API_KEY is set in the environment"
elif [ -f "$HOME/.qodo/config.json" ]; then
  echo "ok: ~/.qodo/config.json exists"
else
  echo "missing: Qodo API key configuration"
  echo "  Generate a key in the Qodo portal and ask your coding agent to configure it safely."
fi

if [ -d ".agents/skills" ]; then
  echo "ok: repo-local .agents/skills directory exists"
else
  echo "missing: .agents/skills directory"
fi

if [ "$missing" -ne 0 ]; then
  echo
  echo "Paste this output into your coding agent and ask it to fix the local setup."
  exit 1
fi

echo
echo "Workshop doctor passed. Next: make setup && make verify"

