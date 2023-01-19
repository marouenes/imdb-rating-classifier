"""
Unit tests for imdb_rating_classifier/penalizer.py
"""
from __future__ import annotations

import pytest  # noqa: F401 # imported but unused

from imdb_rating_classifier.penalizer import penalize_reviews


def test_penalize_reviews() -> None:
    """
    Test the penalize_reviews function.
    """
    movies = [
        {
            'rank': 1,
            'title': 'Foo',
            'year': 2020,
            'votes': 2000000,
            'rating': 8.0,
        },
        {
            'rank': 2,
            'title': 'Bar',
            'year': 2020,
            'votes': 1000000,
            'rating': 7.0,
        },
        {
            'rank': 3,
            'title': 'Baz',
            'year': 2020,
            'votes': 1500000,
            'rating': 6.0,
        },
        # edge case where the max number of votes is the same one other movie
        {
            'rank': 4,
            'title': 'Qux',
            'year': 2020,
            'votes': 2000000,
            'rating': 5.0,
        },
    ]

    penalized_movies = penalize_reviews(movies)[0]
    assert penalized_movies == [
        {
            'rank': 2,
            'title': 'Bar',
            'year': 2020,
            'votes': 1000000,
            'rating': 6.0,
            'penalized': True,
        },
        {
            'rank': 3,
            'title': 'Baz',
            'year': 2020,
            'votes': 1500000,
            'rating': 5.5,
            'penalized': True,
        },
    ]


def test_non_penalized_reviews():
    """
    Test the penalize_reviews function, where there are no penalized reviews.
    """
    movies = [
        {
            'rank': 1,
            'title': 'Foo',
            'year': 2020,
            'votes': 2000000,
            'rating': 8.0,
        },
        {
            'rank': 2,
            'title': 'Bar',
            'year': 2020,
            'votes': 2000000,
            'rating': 7.0,
        },
        {
            'rank': 3,
            'title': 'Baz',
            'year': 2020,
            'votes': 2000000,
            'rating': 6.0,
        },
    ]

    penalized_movies = penalize_reviews(movies)[0]
    assert penalized_movies == []


def test_penalized_reviews_with_invalid_data() -> None:
    """
    Test the penalize_reviews function, where the data is invalid.
    @TODO: add more test cases
    """
    movies = [
        {
            'rank': 1,
            'title': 'Foo',
            'year': 2020,
            'votes': None,
            'rating': 8.0,
        },
    ]

    with pytest.raises(TypeError):
        penalize_reviews(movies)[0]
