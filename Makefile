.PHONY: setup doctor run test lint format typecheck security semgrep verify install-skills

setup:
	uv sync --all-groups
	uv run pre-commit install
	uv run pre-commit install --hook-type commit-msg

doctor:
	./scripts/workshop-doctor.sh

run:
	uv run uvicorn signalpay_api.app:app --reload

test:
	uv run pytest -q

lint:
	uv run ruff check .

format:
	uv run ruff format .

typecheck:
	uv run pyright

security:
	uv run bandit -q -r src

semgrep:
	uv run semgrep --config .semgrep.yml --error --quiet

verify: lint typecheck security test semgrep

install-skills:
	./scripts/install-local-skills.sh

