# IMDB rating classifier

[![Documentation Status](https://readthedocs.org/projects/imdb-rating-classifier/badge/?version=latest)](https://imdb-rating-classifier.readthedocs.io/en/latest/?badge=latest)
[![main](https://github.com/marouenes/imdb-rating-classifier/actions/workflows/main.yml/badge.svg)](https://github.com/marouenes/imdb-rating-classifier/actions/workflows/main.yml)
![PyPI](https://img.shields.io/pypi/v/imdb-rating-classifier)

## Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [CI/CD](#cicd)
- [TODO](#todo)
- [License](#license)
- [Author](#author)

This is a simple [IMDB rating classifier](https://imdb-rating-classifier.readthedocs.io/en/latest/) application that panalizes reviews in accordance with some pre-defined ruleset.

## Overview

The application scrapes data from [IMDB](https://www.imdb.com/chart/top/) and adjusts the rating system according to some specific validation rules (review penalization).

The data is scraped from the IMDB charts API using the [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) library.

The data structure of the parsed and normalized payload is as follows (example):

```json
{
  "rank": "1",
  "title": "The Shawshank Redemption",
  "year": "1994",
  "rating": "9.2",
  "votes": "2,223,000",
  "url": "/title/tt0111161/",
  "oscars_won": 0,
  "penalized": false
}
```

We would then, extract the following fields, into a dataframe:

```python
- rank (int)
- title (str)
- year (int)
- rating (float)
- votes (int)
- url (str)
- oscars_won (int)
- penalized (bool)
```

Using dataclasses, we can then, preprocess the data against some schema definition.

The rules are as follows:

```python
schema = {
    "rank": {
        "type": "int",
        "min": 1,
        "max": 250,
        "required": True,
    },
    "title": {
        "type": "str",
        "required": True,
    },
    "year": {
        "type": "int",
        "min": 1900,
        "max": 2023,
        "required": True,
    },
    "rating": {
        "type": "float",
        "min": 0.0,
        "max": 10.0,
        "required": True,
    },
    "votes": {
        "type": "int",
        "min": 0,
        "required": True,
    },
    "url": {
        "type": "str",
        "required": True,
    },
    "oscars_won": {
        "type": "int",
        "min": 0,
        "required": True,
    },
    "penalized": {
        "type": "bool",
        "required": True,
    },
}
```

## Requirements

- Python >=3.10
- `uv` for modern dependency management

## Installation

### Development Setup

1. Clone the repository:

   ```console
   git clone git@github.com/marouenes/imdb-rating-classifier.git
   cd imdb-rating-classifier
   ```

2. Create and activate a virtual environment:

   ```console
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Install the package in development mode:

   ```console
   make dev
   ```

   This will:
   - Lock dependencies in constraints.txt
   - Install all dependencies
   - Install the package in editable mode
   - Set up development tools

4. Install pre-commit hooks:

   ```console
   pre-commit install
   ```

### Managing Dependencies

We use `uv` with full dependency tree locking:

- `requirements.in` defines our direct dependencies
- `constraints.txt` contains the full locked dependency tree
- `pyproject.toml` defines build system and project metadata

Available dependency management commands:

- `make compile-deps` - Lock current dependencies without upgrading
- `make sync-deps` - Sync environment to exactly match constraints.txt
- `make update-deps` - Upgrade all dependencies to latest versions
- `make update-dep dep=<package>` - Upgrade specific package to latest version

After any update to dependencies, run `make sync-deps` to apply changes to your environment.

### For Users

The application is publicly available on [PyPI](https://pypi.org/project/imdb-rating-classifier/). Install using uv (recommended):

```console
uv pip install imdb-rating-classifier -c constraints.txt
```

Or using pip:

```console
pip install imdb-rating-classifier
```

## Usage

- Display the help message and the available commands

```console
foo@bar:~$ imdb-rating-classifier generate --help
Usage: imdb-rating-classifier generate [OPTIONS]

  Generate the output dataset containing both the original and adjusted
  ratings.

  An extra JSON file will be generated alongside the csv file

Options:
  --output FILE               The path to the output file.
  --number-of-movies INTEGER  The number of movies to scrape.
  -h, --help                  Show this message and exit.
```

- Run the application with the default number of movies (20) and the default output file (data.csv)

```bash
imdb-rating-classifier generate
```

- Run the application with a specific number of movies

```bash
imdb-rating-classifier generate --number-of-movies 100
```

- Run the application with a specific number of movies and a specific output file

```bash
imdb-rating-classifier generate --number-of-movies 100 --output some_name.csv
```

## Development Workflow

### Testing

Run the test suite:

```console
pytest
```

### Code Quality

Format and lint your code:

```console
# Run linting and formatting
make lint

# Or run commands directly
ruff check .   # for linting
ruff format .  # for formatting
```

### Documentation

Build the documentation locally:

```console
cd docs
make html
```

### Dependency Management

We use `uv` with `constraints.txt` for deterministic builds. To add or update dependencies:

1. Add unpinned dependencies to `pyproject.toml` or `requirements.in`
2. Run `make compile-deps` to update constraints.txt
3. Run `make sync-deps` to apply changes to your environment

To upgrade dependencies:

```console
# Upgrade all dependencies
make update-deps
make sync-deps

# Upgrade specific package
make update-dep dep=requests
make sync-deps
```

## CI/CD

The application is automatically packaged and distributed to PyPI, It is also automatically
tested using tox as an environment orchestrator and GitHub Actions.

## TODO

- [x] Add more tests
- [x] Add more validation rules
- [x] Add more documentation
- [ ] Add more features!
- [x] Add a readthedocs page
- [ ] Describe code in readthedocs
- [x] Publish the package on PyPI
- [x] Add oscar awards or nominations for the movies
- [x] Add a version switch for the cli

## License

MIT License

## Author

[Marouane Skandaji](mailto:marouane.skandaji@gmail.com)
