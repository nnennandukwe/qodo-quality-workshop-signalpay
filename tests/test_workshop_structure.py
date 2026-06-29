from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_workshop_docs_are_present() -> None:
    expected = [
        "docs/00-prerequisites.md",
        "docs/01-qodo-portal-github.md",
        "docs/02-qodo-api-key-and-skills.md",
        "docs/03-run-rules-before-coding.md",
        "docs/04-local-verification-gates.md",
        "docs/05-open-pr-and-qodo-review.md",
        "docs/06-pr-resolver-remediation.md",
        "docs/troubleshooting.md",
    ]

    for path in expected:
        assert (ROOT / path).is_file(), path


def test_workshop_skills_are_present() -> None:
    expected = [
        "skills/workshop-plan-from-task/SKILL.md",
        "skills/workshop-tdd-bdd/SKILL.md",
        "skills/workshop-failure-path-testing/SKILL.md",
        "skills/workshop-guidelines-audit/SKILL.md",
        "skills/workshop-pythonic-review/SKILL.md",
        "skills/payment-idempotency/SKILL.md",
    ]

    for path in expected:
        assert (ROOT / path).is_file(), path


def test_planning_templates_are_present() -> None:
    expected = [
        ".plan/README.md",
        ".plan/templates/high-level-plan.md",
        ".plan/templates/build-session-execution-plan.md",
        ".plan/workshop-payment-task/plan.md",
        ".plan/workshop-payment-task/build-session-execution-plan.md",
    ]

    for path in expected:
        assert (ROOT / path).is_file(), path


def test_workshop_rules_are_present() -> None:
    expected = [
        "rules/README.md",
        "rules/payment-mutations.md",
        "rules/auth-and-sessions.md",
        "rules/api-and-events.md",
        "rules/testing-and-gates.md",
        "rules/secrets-and-workshop-safety.md",
    ]

    for path in expected:
        assert (ROOT / path).is_file(), path


def test_rules_index_lists_required_rule_ids() -> None:
    rules_index = (ROOT / "rules/README.md").read_text(encoding="utf-8")

    for number in range(1, 11):
        assert f"PAY-{number:03d}" in rules_index
