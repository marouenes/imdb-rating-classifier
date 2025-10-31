"""Tests for IMDB repository."""

from __future__ import annotations

from unittest.mock import Mock

from imdb_rating_classifier.http import HTTPClient
from imdb_rating_classifier.scraper.repository import IMDBRepository


class MockHTTPClient(HTTPClient):
    def __init__(self, responses):
        self.responses = responses
        self.calls = []

    def get(self, url, headers=None):
        self.calls.append((url, headers))
        return Mock(text=self.responses.get(url, ''))


def test_repository_fetches_and_processes_movies():
    """Test that repository fetches and processes movies correctly."""
    chart_html = """
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
    </tbody>
    """

    movie_html = """
    <div>
        <span class="ipc-metadata-list-item__label">Won 7 Oscars.</span>
    </div>
    """

    client = MockHTTPClient(
        {
            'https://www.imdb.com/chart/top/': chart_html,
            'https://www.imdb.com/title/tt0111161/': movie_html,
        }
    )

    repo = IMDBRepository(http_client=client)
    movies = repo.get_top_movies(limit=1)

    assert len(movies) == 1
    movie = movies[0]
    assert movie.title == 'The Shawshank Redemption'
    assert movie.year == 1994
    assert movie.rating == 9.3
    assert movie.votes == 2456789
    assert movie.oscars_won == 7


def test_repository_handles_errors():
    """Test that repository handles errors gracefully."""
    client = MockHTTPClient(
        {
            'https://www.imdb.com/chart/top/': '<html></html>',
            'https://www.imdb.com/title/tt0111161/': '<html></html>',
        }
    )

    repo = IMDBRepository(http_client=client)
    movies = repo.get_top_movies(limit=1)

    assert len(movies) == 0
