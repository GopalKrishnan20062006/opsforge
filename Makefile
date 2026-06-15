.PHONY: setup check test lint format clean

setup:
	pip install -e .
	pip install pytest pytest-mock ruff black pre-commit

check:
	ruff check .
	black --check .

test:
	pytest -v

format:
	black .
	ruff check . --fix

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
