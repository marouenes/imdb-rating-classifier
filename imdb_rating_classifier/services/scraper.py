"""Movie scraping service."""

from __future__ import annotations

from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List

from imdb_rating_classifier.scraper.impl import Scraper, get_movie_oscar_data
from imdb_rating_classifier.util.logger import setup_logger

logger = setup_logger(__name__)


class MovieScraperService(ABC):
    """Abstract interface for movie scraping service."""

    @abstractmethod
    def fetch_movies(self, limit: int) -> List[Dict[str, Any]]:
        """Fetch movies from source."""
        pass

    @abstractmethod
    def enrich_with_oscars(self, movies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Enrich movies with Oscar data."""
        pass


class IMDBScraperService(MovieScraperService):
    """IMDB implementation of movie scraper service."""

    def __init__(self, base_url: str = 'https://www.imdb.com/chart/top'):
        self.base_url = base_url

    def fetch_movies(self, limit: int) -> List[Dict[str, Any]]:
        """Fetch movies from IMDB."""
        logger.info('Scraping IMDB movie chart data...')
        scraper = Scraper(url=self.base_url, number_of_movies=limit)
        return scraper.scrape()

    def enrich_with_oscars(self, movies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Enrich movies with Oscar data."""
        logger.info('Getting the Oscar winners data...')
        with ThreadPoolExecutor(max_workers=10) as executor:
            results = executor.map(get_movie_oscar_data, [movie['url'] for movie in movies])

        for movie, result in zip(movies, results):
            movie['oscars_won'] = 0 if result is None else result

        return movies
