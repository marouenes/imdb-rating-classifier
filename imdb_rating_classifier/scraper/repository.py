"""Repository for accessing IMDB data."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from functools import partial
from typing import Sequence

from imdb_rating_classifier.http import DEFAULT_HEADERS, HTTPClient, RequestsClient
from imdb_rating_classifier.models import CleanMovieData, MovieData
from imdb_rating_classifier.scraper.parsers import IMDBMovieParser, IMDBParser
from imdb_rating_classifier.util.logger import setup_logger

logger = setup_logger(__name__)


class IMDBRepository:
    """Repository for accessing IMDB data."""

    BASE_URL = 'https://www.imdb.com'
    CHART_PATH = '/chart/top/'

    def __init__(self, http_client: HTTPClient | None = None, max_workers: int = 10):
        """Initialize repository.

        Args:
            http_client: Optional HTTP client override
            max_workers: Max worker threads for concurrent requests
        """
        self.http_client = http_client or RequestsClient(DEFAULT_HEADERS)
        self.max_workers = max_workers

    def get_top_movies(self, limit: int | None = None) -> Sequence[CleanMovieData]:
        """Get top rated movies from IMDB.

        Args:
            limit: Optional limit on number of movies to return

        Returns:
            List of cleaned movie data objects
        """
        logger.info('Fetching IMDB top movies chart...')

        # Fetch and parse movie list
        response = self.http_client.get(f'{self.BASE_URL}{self.CHART_PATH}')
        parser = IMDBParser(response.text)
        movies = parser.parse_movies()

        logger.info(
            'Total Movies Found',
            total_found=len(movies),
        )
        # If limit is explicitly zero, return empty list per tests' expectation
        if limit == 0:
            return []

        if limit is not None:
            movies = movies[:limit]

        # Enrich with Oscar data concurrently
        logger.info(
            'Enriching with Oscar data',
            total_movies=len(movies),
        )
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            fetch_fn = partial(self._fetch_movie_details, client=self.http_client)
            enriched_movies = list(executor.map(fetch_fn, movies))

        # Clean and normalize data
        logger.info(
            'Cleaning and normalizing data',
            total_movies=len(enriched_movies),
        )
        return [CleanMovieData.from_raw(movie) for movie in enriched_movies]

    def _fetch_movie_details(self, movie: MovieData, client: HTTPClient) -> MovieData:
        """Fetch additional details for a movie."""
        if not movie.imdb_id:
            logger.warning(f'No IMDB ID for movie: {movie.title}')
            movie.oscars_won = 0
            return movie

        try:
            response = client.get(f'{self.BASE_URL}/title/{movie.imdb_id}/')
            parser = IMDBMovieParser(response.text)
            movie.oscars_won = parser.parse_oscar_count()
        except Exception as e:
            logger.error(f'Failed to fetch details for {movie.title}: {e}')
            movie.oscars_won = 0
        return movie
