from __future__ import annotations

import re
import sys
from pathlib import Path

PATTERN = re.compile(r"^(build|chore|ci|docs|feat|fix|refactor|test|perf)(\([a-z0-9-]+\))?: .+")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_commit_msg.py <commit-msg-file>", file=sys.stderr)
        return 2

    message = Path(sys.argv[1]).read_text(encoding="utf-8").splitlines()[0].strip()
    if PATTERN.match(message):
        return 0

    print(
        "Commit message must use Conventional Commits, e.g. `feat(payments): add refund workflow`.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
