"""Movie data validation service."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, cast

import pandas as pd

from imdb_rating_classifier.schema import MovieChart
from imdb_rating_classifier.util.logger import setup_logger

logger = setup_logger(__name__)


class MovieValidationService(ABC):
    """Abstract interface for movie data validation."""

    @abstractmethod
    def validate_movie(self, movie: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a single movie entry."""
        pass

    @abstractmethod
    def validate_movies(self, df: pd.DataFrame) -> List[MovieChart]:
        """Validate multiple movies."""
        pass


class IMDBValidationService(MovieValidationService):
    """IMDB implementation of movie validation service."""

    def validate_movie(self, movie: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and ensure required fields exist in movie data."""
        required_fields = ['year', 'title', 'url', 'rating', 'votes']
        default_values = {
            'title': 'Unknown',
            'url': '',
            'year': 2000,
            'rating': 0.0,
            'votes': 0,
        }

        for field in required_fields:
            if field not in movie or movie[field] is None:
                logger.warning(
                    f"Missing or null required field '{field}' in movie: {movie.get('title', 'Unknown')}"
                )
                movie[field] = default_values[field]

            # Type conversion
            if field == 'year':
                try:
                    movie['year'] = int(str(movie['year']).strip('()'))
                except (ValueError, TypeError):
                    movie['year'] = default_values['year']
            elif field in ['rating', 'votes']:
                try:
                    movie[field] = float(movie[field]) if field == 'rating' else int(movie[field])
                except (ValueError, TypeError):
                    movie[field] = default_values[field]

        return movie

    def validate_movies(self, df: pd.DataFrame) -> List[MovieChart]:
        """Validate movie data against schema."""
        logger.info('Validating the movies...')
        movies_dict = df.to_dict(orient='records')
        try:
            movies_dict = cast(list[dict[str, Any]], df.to_dict(orient='records'))
            valid_movies = [MovieChart(**movie) for movie in movies_dict]
            logger.info(f'Data validation passed. Valid movies: {len(valid_movies)}')
            return valid_movies
        except Exception as e:
            logger.error(f'Validation failed: {e}')
            raise
