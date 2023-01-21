:orphan:

.. image:: https://img.shields.io/pypi/v/imdb-rating-classifier
   :target: https://pypi.org/project/imdb-rating-classifier/
   :alt: PyPI

.. image:: https://readthedocs.org/projects/imdb-rating-classifier/badge/?version=latest
   :target: https://readthedocs.org/projects/imdb-rating-classifier/badge/?version=latest
   :alt: Documentation Status

.. image:: https://github.com/marouenes/imdb-rating-classifier/actions/workflows/main.yml/badge.svg
   :target: https://github.com/marouenes/imdb-rating-classifier/actions/workflows/main.yml/badge.svg
   :alt: CI/CD

.. image:: https://img.shields.io/github/license/marouenes/imdb-rating-classifier
   :target: https://img.shields.io/github/license/marouenes/imdb-rating-classifier
   :alt: License

IMDB rating classifier
======================

.. toctree::
   :maxdepth: 2
   :caption: Table of Contents:

.. note::

   This project is under active development.


Table of Contents
-----------------

-  `Overview <#overview>`__
-  `Requirements <#requirements>`__
-  `Installation <#installation>`__
-  `Usage <#usage>`__
-  `Testing <#testing>`__
-  `CI/CD <#cicd>`__
-  `License <#license>`__
-  `Author <#author>`__

This is a simple IMDB rating classifier application that panalizes
reviews in accordance with some pre-defined ruleset.

Overview
--------

The application scrapes data from
`IMDB <https://www.imdb.com/chart/top/>`__ and adjusts the rating system
according to some specific validation rules (review penalization).

The data is scraped from the IMDB charts API using the
`BeautifulSoup <https://www.crummy.com/software/BeautifulSoup/bs4/doc/>`__
library.

The data structure of the parsed and normalized payload is as follows
(example):

.. code:: json

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

We would then, extract the following fields, into a dataframe:

.. code:: python

   - rank (int)
   - title (str)
   - year (int)
   - rating (float)
   - votes (int)
   - url (str)
   - oscars_won (int)
   - penalized (bool)

Using dataclasses, we can then, preprocess the data against some schema
definition.

The rules are as follows:

.. code:: python

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

Requirements
------------

-  Python>=3.8>=3.10
-  BeautifulSoup4
-  requests
-  pytest
-  tox
-  click
-  pre-commit
-  flake8
-  black
-  isort

and more...

Installation
------------

For development purposes:

-  Clone the repository

   .. code:: console

      foo@bar:~$ git clone git@github.com/marouenes/imdb-rating-classifier.git

-  Create a virtual environment

   .. code:: console

      foo@bar:~/imdb-rating-classifier$ virtualenv .venv

-  Activate the virtual environment

   .. code:: console

      foo@bar:~/imdb-rating-classifier$ source .venv/bin/activate

-  Install the dev dependencies

   .. code:: console

      foo@bar:~/imdb-rating-classifier$ pip install -r requirements-dev.txt

-  Install the pre-commit hooks

   .. code:: console

      foo@bar:~/imdb-rating-classifier$ pre-commit install

For usage:

-  Install the dependencies and build the wheel

   .. code:: console

      foo@bar:~/imdb-rating-classifier$ pip install -e .

The application is publicly available and published on
`PyPI <https://pypi.org/project/imdb-rating-classifier/>`__ and can be
installed using pip:

.. code:: console

   foo@bar:~$ pip install imdb-rating-classifier

Usage
-----

-  Display the help message and the available commands

.. code:: console

   foo@bar:~$ imdb-rating-classifier generate --help
   Usage: imdb-rating-classifier generate [OPTIONS]

     Generate the output dataset containing both the original and adjusted
     ratings.

     An extra JSON file will be generated alongside the csv file

   Options:
     --output FILE               The path to the output file.
     --number-of-movies INTEGER  The number of movies to scrape.
     -h, --help                  Show this message and exit.

-  Run the application with the default number of movies (20) and the
   default output file (data.csv)

.. code:: bash

   imdb-rating-classifier generate

-  Run the application with a specific number of movies

.. code:: bash

   imdb-rating-classifier generate --number-of-movies 100

-  Run the application with a specific number of movies and a specific
   output file

.. code:: bash

   imdb-rating-classifier generate --number-of-movies 100 --output some_name.csv

Testing
-------

-  Run tests and pre-commit hooks

.. code:: console

   foo@bar:~/imdb-rating-classifier$ tox

CI/CD
-----

The application is automatically packaged and distributed to PyPI, It is
also automatically tested using tox as an environment orchestrator and
GitHub Actions.

TODO
----

-  ☒ Add more tests
-  ☒ Add more validation rules
-  ☒ Add more documentation
-  ☐ Add more features!
-  ☒ Publish the package on PyPI
-  ☒ Add oscar awards or nominations for the movies
-  ☒ Add a version switch for the cli

License
-------

MIT License

Author
------

`Marouane Skandaji <mailto:marouane.skandaji@gmail.com>`__
