"""
Fixtures for testing
"""

from __future__ import annotations

import json
import tempfile
from typing import Dict, List

import pytest

from imdb_rating_classifier.http import HTTPClient
from imdb_rating_classifier.models import CleanMovieData, MovieData


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


class MockHTTPClient(HTTPClient):
    """Mock HTTP client for testing."""

    def __init__(self, responses: Dict[str, str]) -> None:
        self.responses = responses
        self.calls: List[tuple[str, dict | None]] = []

    def get(self, url: str, headers: dict | None = None) -> MockResponse:  # type: ignore
        """Record call and return mock response."""
        self.calls.append((url, headers))
        if url not in self.responses:
            raise ValueError(f'No mock response for {url}')
        return MockResponse(self.responses[url])


class MockResponse:
    """Mock response object."""

    def __init__(self, text: str) -> None:
        self.text = text

    def raise_for_status(self) -> None:
        """Mock successful response."""
        pass


@pytest.fixture
def mock_http_client() -> MockHTTPClient:
    """Create a mock HTTP client with sample responses."""
    return MockHTTPClient(
        {
            'https://www.imdb.com/chart/top/': """
            <tbody class="lister-list">
                <tr>
                    <td class="titleColumn">
                        1.<a href="/title/tt0111161/">The Shawshank Redemption</a>
                        <span class="secondaryInfo">(1994)</span>
                    </td>
                    <td class="ratingColumn">
                        <strong title="9.3 based on 2,456,789 user ratings">9.3</strong>
                    </td>
                </tr>
                <tr>
                    <td class="titleColumn">
                        2.<a href="/title/tt0068646/">The Godfather</a>
                        <span class="secondaryInfo">(1972)</span>
                    </td>
                    <td class="ratingColumn">
                        <strong title="9.2 based on 1,789,456 user ratings">9.2</strong>
                    </td>
                </tr>
            </tbody>
        """,
            'https://www.imdb.com/title/tt0111161/': """
            <div>
                <span class="ipc-metadata-list-item__label">Won 7 Oscars.</span>
            </div>
        """,
            'https://www.imdb.com/title/tt0068646/': """
            <div>
                <span class="ipc-metadata-list-item__label">Won 3 Oscars.</span>
            </div>
        """,
        }
    )


@pytest.fixture
def sample_raw_movie() -> MovieData:
    """Create a sample raw movie data object."""
    return MovieData(
        rank='1',
        title='The Shawshank Redemption',
        year='(1994)',
        rating='9.3',
        votes='2,456,789',
        url='/title/tt0111161/',
        penalized=False,
    )


@pytest.fixture
def sample_clean_movie() -> CleanMovieData:
    """Create a sample clean movie data object."""
    return CleanMovieData(
        rank=1,
        title='The Shawshank Redemption',
        year=1994,
        rating=9.3,
        votes=2456789,
        url='https://www.imdb.com/title/tt0111161/',
        penalized=False,
        oscars_won=7,
    )
