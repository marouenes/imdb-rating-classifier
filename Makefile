.PHONY: help dev test clean

default: help

help:
	@echo 'Makefile for the project'
	@echo
	@echo 'Usage:'
	@echo '    make dev        install the packages in development mode'
	@echo '    make lint       run linter'
	@echo '    make test       run tests'
	@echo '    make clean      clean all auxiliary files, build and test compiled files'
	@echo

dev:
	# install the package in development mode
	python -m pip install --upgrade pip
	pip install -e .[dev]

test:
	# run unit tests and generate coverage report
	python -m pytest tests/ -vv --cov=. --cov-report=html --cov-report=term-missing --junitxml=junit/coverage-results.xml

clean:
	# clean all auxiliary files, build and test compiled files
	@rm -rf .pytest_cache/ */.pytest_cache/ junit/ build/ dist/ htmlcov/ .coverage
	@find . -not -path './.venv*' -path '*/__pycache__*' -delete
	@find . -not -path './.venv*' -path '*/*.egg-info*' -delete
