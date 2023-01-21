"""
Fixtures for testing
"""
from __future__ import annotations

import json
import tempfile

import pytest


@pytest.fixture
def temp_dir():
    """
    Fixture to set up a temporary directory that is deleted on exit.
    """
    with tempfile.TemporaryDirectory() as directory:
        yield directory


@pytest.fixture
def load_movies_data():
    example_movies = 'tests/test_data/dummy_movie.json'
    with open(example_movies) as f:
        movies = json.load(f)

    yield movies
