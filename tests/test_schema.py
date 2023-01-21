"""
Unit tests for imdb_rating_classifier/schema.py

@TODO: add unit tests
"""
from __future__ import annotations

import pandas as pd
import pytest

from imdb_rating_classifier.schema import MovieChart, normalize


@pytest.mark.parametrize(
    'input_data, expected_data',
    [(
        [
            {'rank': 1, 'year': '2000', 'votes': 2000000, 'rating': 8, 'penalized': False},
            {'rank': 1, 'year': '2000', 'votes': 2000000, 'rating': 8, 'penalized': False},
            {'rank': 1, 'year': '2000', 'votes': 2000000, 'rating': 8, 'penalized': False},
        ],
        [
            {'rank': 1, 'year': 2000, 'votes': 2000000, 'rating': 8.0, 'penalized': False},
            {'rank': 1, 'year': 2000, 'votes': 2000000, 'rating': 8.0, 'penalized': False},
            {'rank': 1, 'year': 2000, 'votes': 2000000, 'rating': 8.0, 'penalized': False},
        ],
    )],
)
def test_normalize(input_data: list[dict], expected_data: list[dict]):
    """
    Test the normalize function.
    """
    # create a pandas dataframe from the input data
    input_df = pd.DataFrame(input_data)
    # create a pandas dataframe from the expected data
    expected_df = pd.DataFrame(expected_data)
    # normalize the input data
    normalized_df = normalize(input_df)

    # check that the schema is correct
    assert normalized_df.dtypes['rank'] == 'int64'
    assert normalized_df.dtypes['year'] == 'int64'
    assert normalized_df.dtypes['votes'] == 'int64'
    assert normalized_df.dtypes['rating'] == 'float64'
    assert normalized_df.dtypes['penalized'] == 'bool'

    # compare the normalized data with the expected data
    pd.testing.assert_frame_equal(normalized_df, expected_df)


def test_movie_chart_dataclass():
    """
    Test the MovieChart dataclass.
    """
    # input data
    input_data = {
        'rank': 1,
        'title': 'Foo',
        'year': 2000,
        'votes': 2000000,
        'rating': 8.0,
        'penalized': False,
        'url': 'https://www.imdb.com/title/tt0000001/',
        'oscars_won': 0,
    }
    # create a MovieChart object
    movie_chart = MovieChart(**input_data)

    # check that the dataclass is correct
    assert movie_chart.rank == 1
    assert movie_chart.title == 'Foo'
    assert movie_chart.year == 2000
    assert movie_chart.votes == 2000000
    assert movie_chart.rating == 8.0
    assert movie_chart.penalized is False
    assert movie_chart.url == 'https://www.imdb.com/title/tt0000001/'
    assert movie_chart.oscars_won == 0

    # check that the dataclass is correct when converted to a dictionary
    assert movie_chart.to_dict() == {
        'rank': 1,
        'title': 'Foo',
        'year': 2000,
        'votes': 2000000,
        'rating': 8.0,
        'penalized': False,
        'url': 'https://www.imdb.com/title/tt0000001/',
        'oscars_won': 0,
    }


def test_moviechart_invalid_types():
    """
    Test the MovieChart dataclass with invalid attributes.
    """
    invalid_type = {
        'rank': '1',
        'title': None,
        'year': '2000',
        'votes': '2000000',
        'rating': '8.0',
        'penalized': 'False',
        'url': 'https://www.imdb.com/title/tt0000001/',
        'oscars_won': '0',
    }

    with pytest.raises(TypeError):
        MovieChart(**invalid_type)


def test_moviechart_invalid_values():
    """
    Test the MovieChart dataclass with invalid attributes.
    """
    invalid_value = {
        'rank': 0,
        'title': 'Foo',
        'year': 0,
        'votes': 0,
        'rating': 0,
        'penalized': False,
        'url': 'https://www.imdb.com/title/tt0000001/',
        'oscars_won': -1,
    }

    with pytest.raises(ValueError):
        MovieChart(**invalid_value)
