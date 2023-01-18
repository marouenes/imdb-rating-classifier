# IMDB rating classifier

This is a simple IMDB rating classifier using the IMDB charts API.

## Overview

The application scrapes data from IMDB and adjusts the rating system according to some specific validation rules.

## Requirements

- Python>=3.8>=3.10
- BeautifulSoup4
- requests
- pytest
- tox
- click
- pre-commit
- flake8
- black
- isort

and more...

## Installation

- Clone the repository

  ```console
  foo@bar:~$ git clone git@github.com/marouenes/imdb-rating-classifier.git
  ```

- Create a virtual environment

  ```console
  foo@bar:~/imdb-rating-classifier$ virtualenv .venv
  ```

- Activate the virtual environment

  ```console
  foo@bar:~/imdb-rating-classifier$ source .venv/bin/activate
  ```

For development:

- Install the dependencies

  ```console
  foo@bar:~/imdb-rating-classifier$ pip install -r requirements-dev.txt
  ```

- Install the pre-commit hooks

  ```console
    foo@bar:~/imdb-rating-classifier$ pre-commit install
  ```

For usage:

- Install the dependencies and build the wheel

  ```console
    foo@bar:~/imdb-rating-classifier$ pip install -e .
  ```

## Usage

- Display the help message and the available commands

```console
foo@bar:~$ imdb-rating-classifier generate --help
Usage: imdb-rating-classifier generate [OPTIONS]

  Generate the output dataset containing both the original and adjusted
  ratings.

  Args:     output (str): The path to the output file.

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

## Testing

- Run tests and pre-commit hooks

```console
foo@bar:~/imdb-rating-classifier$ tox
```

## CI/CD

The application is automatically packaged and distributed to PyPI, It is also automatically
tested using tox as an environment orchestrator and GitHub Actions.

## TODO

- [ ] Add more tests
- [ ] Add more validation rules
- [ ] Add more documentation
- [ ] Add more features
- [ ] Publish the package on PyPI

## License

MIT License

## Author

[Marouane Skandaji](mailto:marouane.skandaji@gmail.com)
