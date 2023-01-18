# IMDB rating classifer

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

- Install the requirements in dev mode

```bash
pip install -r requirements-dev.txt
```

## Usage

- Run the application

```console
foo@bar:~/imdb-rating-classifier$ python imdb_rating_classifier/generate.py
```

- Run the application with a specific number of movies

```console
foo@bar:~/imdb-rating-classifier$ python imdb_rating_classifier/generate.py --number-of-movies 10
```

- Run the application with a specific number of movies and a specific output file

```console
foo@bar:~/imdb-rating-classifier$ python imdb_rating_classifier/generate.py --output data.csv
```

## Testing

- Run tests and pre-commit hooks

```console
foo@bar:~/imdb-rating-classifier$ tox
```

## License

MIT

## Author

[Marouane Skandaji](mailto:marouane.skandaji@gmail.com)
