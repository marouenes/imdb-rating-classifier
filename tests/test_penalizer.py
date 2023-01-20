"""
Unit tests for imdb_rating_classifier/penalizer.py
@TODO: parametrize the test_penalize_reviews function?
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

    penalized_movies = penalize_reviews(movies)
    for movie in penalized_movies:
        assert movie['penalized'] is False if movie['votes'] == max(
            movie['votes'] for movie in movies
        ) else True


@pytest.mark.parametrize(
    'movies, expected',
    [(
        [
            {'rank': 1, 'title': 'Foo', 'year': 2020, 'votes': 2000000, 'rating': 8.0},
            {'rank': 2, 'title': 'Bar', 'year': 2020, 'votes': 1000000, 'rating': 7.0},
            # edge case where the max number of votes is the same one other movie
            {'rank': 3, 'title': 'Qux', 'year': 2020, 'votes': 2000000, 'rating': 5.0},
        ],
        [
            {
                'rank': 1,
                'title': 'Foo',
                'year': 2020,
                'votes': 2000000,
                'rating': 8.0,
                'penalized': False,
                'penalized_rating': None,
            },
            {
                'rank': 2,
                'title': 'Bar',
                'year': 2020,
                'votes': 1000000,
                'rating': 7.0,
                'penalized': True,
                'penalized_rating': 6.0,
            },
            {
                'rank': 3,
                'title': 'Qux',
                'year': 2020,
                'votes': 2000000,
                'rating': 5.0,
                'penalized': False,
                'penalized_rating': None,
            },
        ],
    )],
)
def test_penalized_movie_reviews(movies: list, expected: list) -> None:
    """
    Test the penalize_reviews function with a list of movies and expected results.
    """
    penalized_movies = penalize_reviews(movies)
    assert penalized_movies == expected


@pytest.mark.parametrize(
    'movies, expected',
    [(
        [
            {'rank': 1, 'title': 'Foo', 'year': 2020, 'votes': 2000000, 'rating': 8.0},
            {'rank': 2, 'title': 'Bar', 'year': 2020, 'votes': 2000000, 'rating': 7.0},
        ],
        [
            {
                'rank': 1,
                'title': 'Foo',
                'year': 2020,
                'votes': 2000000,
                'rating': 8.0,
                'penalized': False,
                'penalized_rating': None,
            },
            {
                'rank': 2,
                'title': 'Bar',
                'year': 2020,
                'votes': 2000000,
                'rating': 7.0,
                'penalized': False,
                'penalized_rating': None,
            },
        ],
    )],
)
def test_non_penalized_reviews(movies: list, expected: list) -> None:
    """
    Test the penalize_reviews function, where there are no penalized reviews.
    """
    penalized_movies = penalize_reviews(movies)

    for movie in penalized_movies:
        assert movie['penalized'] is False

    assert penalized_movies == expected


def test_penalized_reviews_with_invalid_data() -> None:
    """
    Test the penalize_reviews function, where the data is invalid.
    @TODO: add more test cases
    """
    movies = {
        'rank': 1,
        'title': 'Foo',
        'year': 2020,
        'votes': None,
        'rating': 8.0,
    },

    with pytest.raises(ValueError):
        penalize_reviews(movies)
