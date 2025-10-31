"""Tests for HTML parsers."""

from __future__ import annotations

from imdb_rating_classifier.scraper.parsers import IMDBMovieParser, IMDBParser


def test_imdb_parser_extracts_movie_data():
    """Test that movie data is correctly extracted from HTML."""
    html = """
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

    parser = IMDBParser(html)
    movies = parser.parse_movies()

    assert len(movies) == 1
    movie = movies[0]
    assert movie.rank == '1'
    assert movie.title == 'The Shawshank Redemption'
    assert movie.year == '(1994)'
    assert movie.rating == '9.3'
    assert movie.votes == '2,456,789'
    assert movie.url == '/title/tt0111161/'


def test_imdb_movie_parser_extracts_oscars():
    """Test that Oscar count is correctly extracted."""
    html = """
    <div>
        <span class="ipc-metadata-list-item__label">Won 7 Oscars.</span>
    </div>
    """

    parser = IMDBMovieParser(html)
    oscar_count = parser.parse_oscar_count()

    assert oscar_count == 7


def test_imdb_movie_parser_handles_no_oscars():
    """Test that zero is returned when no Oscars found."""
    html = '<div></div>'

    parser = IMDBMovieParser(html)
    oscar_count = parser.parse_oscar_count()

    assert oscar_count == 0
