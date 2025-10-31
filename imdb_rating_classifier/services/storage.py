"""Movie data storage service."""

from __future__ import annotations

import os
from abc import ABC, abstractmethod

import pandas as pd

from imdb_rating_classifier.util.logger import setup_logger

logger = setup_logger(__name__)


class MovieStorageService(ABC):
    """Abstract interface for movie data storage."""

    @abstractmethod
    def save(self, df: pd.DataFrame, output_path: str) -> None:
        """Save movie data to storage."""
        pass


class FileStorageService(MovieStorageService):
    """File-based implementation of movie storage service."""

    def save(self, df: pd.DataFrame, output_path: str) -> None:
        """Save results to CSV and JSON."""
        # Ensure output directory exists
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

        logger.info(
            'Saving dataset',
            location=output_path,
        )
        df.to_csv(output_path, index=False)

        json_path = output_path.replace('.csv', '.json')
        df.to_json(json_path, orient='records', indent=2)
        logger.info(
            'Saved dataset',
            locations=[output_path, json_path],
        )
