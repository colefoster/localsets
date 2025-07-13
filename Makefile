.PHONY: help install install-dev test lint format clean build dist upload

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install the package in development mode
	pip install -e .

install-dev:  ## Install the package with development dependencies
	pip install -e ".[dev]"

test:  ## Run tests
	pytest tests/ -v

test-cov:  ## Run tests with coverage
	pytest tests/ --cov=localsets --cov-report=html --cov-report=term-missing

lint:  ## Run linting checks
	flake8 localsets/ tests/
	mypy localsets/

format:  ## Format code with black
	black localsets/ tests/ examples/

format-check:  ## Check code formatting
	black --check localsets/ tests/ examples/

clean:  ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

build: clean  ## Build the package
	python setup.py build

dist: clean  ## Create distribution packages
	python setup.py sdist bdist_wheel

upload: dist  ## Upload to PyPI (requires twine)
	twine upload dist/*

download-data:  ## Download data files during development
	python setup.py download_data

example:  ## Run the basic usage example
	python examples/basic_usage.py

cli-help:  ## Show CLI help
	localsets --help

cli-formats:  ## Show available formats
	localsets formats

cli-info:  ## Show package info
	localsets info

check: format-check lint test  ## Run all checks (format, lint, test)

all: clean install-dev check  ## Run full development setup and checks 