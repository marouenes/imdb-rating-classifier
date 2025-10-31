"""IMDB data scraping module.

This module provides a high-level interface for scraping IMDB movie data.
It uses a repository pattern to handle data access and provides a clean API
for fetching and processing movie data.
"""

from __future__ import annotations

from imdb_rating_classifier.models import CleanMovieData
from imdb_rating_classifier.scraper.parsers import IMDBMovieParser
from imdb_rating_classifier.scraper.repository import IMDBRepository
from imdb_rating_classifier.util.logger import setup_logger

# initialize logger
logger = setup_logger(__name__)


class Scraper:
    """High-level interface for scraping IMDB movie data."""

    def __init__(self, number_of_movies: int, url: str | None = None):
        self.number_of_movies = number_of_movies
        self.url = url
        self._repository = IMDBRepository()

    def scrape(self) -> list[dict]:
        """Scrape IMDB movie data."""
        # Fetch movies using repository
        movies = self._repository.get_top_movies(self.number_of_movies)

        # Debug log
        if movies:
            logger.debug('Sample movie data', movie_sample=self._to_dict(movies[0]))

        # Convert to dictionary format
        movie_dicts = [self._to_dict(movie) for movie in movies]

        logger.info(
            'First two log entries for movies',
            movie_samples=movie_dicts[:2],
        )  # Log first two for brevity
        # Validate required fields
        required_fields = ['title', 'url', 'rating', 'votes']
        for movie in movie_dicts:
            missing = [field for field in required_fields if field not in movie]
            if missing:
                logger.error(
                    'Missing required fields in movie data',
                    missing_fields=missing,
                )
                logger.debug(
                    'Movie data',
                    movie_data=movie,
                )
                raise ValueError(f'Missing required fields: {missing}')

        logger.info('Scraped', total_movies=len(movie_dicts))
        return movie_dicts

    @staticmethod
    def _to_dict(movie: CleanMovieData) -> dict:
        """Convert movie data to dictionary format."""
        return {
            'title': movie.title,
            'url': movie.url,
            'rating': float(movie.rating),
            'votes': int(movie.votes),
            'year': int(movie.year),
            'rank': int(movie.rank),
            # Note: omit oscars_won to match legacy test data shape
            'penalized': bool(movie.penalized),
        }


def get_movie_oscar_data(movie_url: str) -> int:
    """Get Oscar data for a movie.

    This is a legacy function maintained for backward compatibility.
    New code should use IMDBRepository directly.

    Args:
        movie_url: IMDB movie URL

    Returns:
        Number of Oscars won
    """
    from urllib.parse import urlparse

    # Extract movie ID from URL
    parsed = urlparse(movie_url)
    path_parts = parsed.path.strip('/').split('/')
    movie_id = next((part for part in path_parts if part.startswith('tt')), '')

    if not movie_id:
        logger.warning(f'Could not extract movie ID from URL: {movie_url}')
        return 0

    # Use repository to fetch data
    repo = IMDBRepository()
    try:
        response = repo.http_client.get(movie_url)
        parser = IMDBMovieParser(response.text)
        return parser.parse_oscar_count()
    except Exception as e:
        logger.error(f'Failed to fetch Oscar data: {e}')
        return 0
