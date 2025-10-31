"""Movie data processing service."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List

import pandas as pd

from imdb_rating_classifier.penalizer import penalize_reviews
from imdb_rating_classifier.util.logger import setup_logger

logger = setup_logger(__name__)


class MovieProcessingService(ABC):
    """Abstract interface for movie data processing."""

    @abstractmethod
    def apply_penalties(self, movies: List[Dict[str, Any]]) -> pd.DataFrame:
        """Apply penalties to movie ratings."""
        pass


class IMDBProcessingService(MovieProcessingService):
    """IMDB implementation of movie processing service."""

    def apply_penalties(self, movies: List[Dict[str, Any]]) -> pd.DataFrame:
        """Apply rating penalties according to rules."""
        logger.info('Applying rating penalties...')
        penalized_movies = penalize_reviews(movies)

        penalized_count = sum(1 for movie in penalized_movies if movie.get('penalized', False))
        logger.info(
            'Movies penalized',
            penalized_count=penalized_count,
        )

        return pd.DataFrame(penalized_movies)
