"""Validate command implementation."""

from __future__ import annotations

import os
from typing import Any

import pandas as pd

from imdb_rating_classifier.cli.commands.base import BaseCommand
from imdb_rating_classifier.schema import MovieChart, normalize
from imdb_rating_classifier.util.logger import setup_logger

logger = setup_logger(__name__)


class ValidateCommand(BaseCommand):
    """Command to validate a dataset file against the movie schema."""

    def __init__(self, input_path: str) -> None:
        super().__init__()
        self.input_path = input_path

    def execute(self, **kwargs: Any) -> None:
        """Validate the input file against the schema."""
        if not os.path.exists(self.input_path):
            logger.error(f'File not found: {self.input_path}')
            raise FileNotFoundError(f'File not found: {self.input_path}')
        logger.info(f'Validating file: {self.input_path}')
        if self.input_path.endswith('.csv'):
            df = pd.read_csv(self.input_path)
        elif self.input_path.endswith('.json'):
            df = pd.read_json(self.input_path)
        else:
            logger.error('Unsupported file format. Use .csv or .json.')
            raise ValueError('Unsupported file format. Use .csv or .json.')
        df = normalize(df)
        movies = df.to_dict(orient='records')
        try:
            valid_movies = [MovieChart(**movie) for movie in movies]
        except Exception as e:
            logger.error(f'Validation failed: {e}')
            raise
        logger.info(f'Validation passed. {len(valid_movies)} valid movies.')
        print(f'Validation passed. {len(valid_movies)} valid movies.')
