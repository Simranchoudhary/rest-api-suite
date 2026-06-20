.PHONY: install test lint report clean

install:
	python3 -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt

test:
	.venv/bin/pytest

test-auth:
	.venv/bin/pytest -m auth

test-users:
	.venv/bin/pytest -m users

test-contract:
	.venv/bin/pytest -m contract

test-slow:
	.venv/bin/pytest -m slow

lint:
	.venv/bin/ruff check .

lint-fix:
	.venv/bin/ruff check . --fix

report:
	open reports/report.html

clean:
	rm -rf .pytest_cache __pycache__ reports/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
