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
	@echo '    make compile-deps    compile dependencies into requirements/*.txt'
	@echo '    make sync-deps       sync current environment with compiled requirements'
	@echo '    make update-deps     update and compile dependencies to newest versions'
	@echo

compile-deps:
	python -m pip install -U uv
	uv pip compile requirements.in -o constraints.txt

sync-deps:
	uv pip sync constraints.txt

update-deps:
	python -m pip install -U uv
	uv pip compile --upgrade requirements.in -o constraints.txt

dev: compile-deps sync-deps
	# install the package in development mode
	python -m pip install --upgrade pip
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
