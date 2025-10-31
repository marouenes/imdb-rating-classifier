.PHONY: help dev test clean compile-deps sync-deps update-deps

default: help

help:
	@echo 'Makefile for the project'
	@echo
	@echo 'Usage:'
	@echo '    make dev             install the packages in development mode'
	@echo '    make lint            run ruff linter and formatter'
	@echo '    make test            run tests'
	@echo '    make clean           clean all auxiliary files, build and test compiled files'
	@echo
	@echo 'Dependency Management:'
	@echo '    make compile-deps    lock current dependencies without upgrading'
	@echo '    make sync-deps       sync environment to match constraints.txt exactly'
	@echo '    make update-deps     upgrade all dependencies to latest versions'
	@echo '    make update-dep dep=<package>  upgrade specific package to latest version'
	@echo

ensure-uv:
	python -m pip install -U uv

compile-deps: ensure-uv
	# Lock current dependencies without upgrading versions
	uv pip compile requirements.in -o constraints.txt

sync-deps: ensure-uv
	# Sync virtual environment to exactly match constraints.txt
	uv pip sync constraints.txt

update-deps: ensure-uv
	# Upgrade all dependencies to their latest versions and recompile
	uv pip compile --upgrade requirements.in -o constraints.txt
	@echo "Run 'make sync-deps' to apply the updates to your environment"

update-dep: ensure-uv
	# Update a specific dependency. Usage: make update-dep dep=<package-name>
	@if [ "$(dep)" = "" ]; then \
		echo "Usage: make update-dep dep=<package-name>"; \
		exit 1; \
	fi
	uv pip compile requirements.in --upgrade-package $(dep) -o constraints.txt
	@echo "Run 'make sync-deps' to apply the update to your environment"

dev: ensure-uv compile-deps
	# Install package in development mode with all dev dependencies
	uv pip sync constraints.txt
	uv pip install -e .[dev]

test:
	# run unit tests and generate coverage report
	python -m pytest tests/ -vv --cov=. --cov-report=html --cov-report=term-missing --junitxml=junit/coverage-results.xml

lint:
	# run ruff linter and formatter
	ruff check .
	ruff format .

clean:
	# clean all auxiliary files, build and test compiled files
	@rm -rf .pytest_cache/ */.pytest_cache/ junit/ build/ dist/ htmlcov/ .coverage .ruff_cache/
	@find . -not -path './.venv*' -path '*/__pycache__*' -delete
	@find . -not -path './.venv*' -path '*/*.egg-info*' -delete
