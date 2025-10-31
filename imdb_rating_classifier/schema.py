"""
Module for predefined table/JSON schemas

The intent of this module is to define the schema for the IMDB movie chart data.
@TODO: - Validate the schema using a dataclass?
"""

from __future__ import annotations

import typing as t
from dataclasses import dataclass

import pandas as pd

from imdb_rating_classifier.util.logger import setup_logger

logger = setup_logger(__name__)


@dataclass
class MovieChart:
    """Movie chart data model."""

    title: str
    url: str
    rating: float
    votes: int
    year: int
    rank: int
    oscars_won: int = 0
    penalized: bool = False

    def __post_init__(self):  # noqa: C901
        # Strict type checks to catch invalid types early
        if not isinstance(self.rank, int):
            raise TypeError(f'Invalid type for rank: {type(self.rank).__name__}')
        if not isinstance(self.title, str):
            raise TypeError(f'Invalid type for title: {type(self.title).__name__}')
        if not isinstance(self.year, int):
            raise TypeError(f'Invalid type for year: {type(self.year).__name__}')
        # Allow int or float for rating (tests may provide ints)
        if not isinstance(self.rating, (int, float)):
            raise TypeError(f'Invalid type for rating: {type(self.rating).__name__}')
        if not isinstance(self.votes, int):
            raise TypeError(f'Invalid type for votes: {type(self.votes).__name__}')
        if not isinstance(self.url, str):
            raise TypeError(f'Invalid type for url: {type(self.url).__name__}')
        if not isinstance(self.oscars_won, int):
            raise TypeError(f'Invalid type for oscars_won: {type(self.oscars_won).__name__}')
        if not isinstance(self.penalized, bool):
            raise TypeError(f'Invalid type for penalized: {type(self.penalized).__name__}')

        # Value checks
        if not 1 <= self.rank <= 250:
            raise ValueError(f'Invalid rank: {self.rank}')
        if not 1900 <= self.year <= 2023:
            raise ValueError(f'Invalid year: {self.year}')
        if not 0.0 <= self.rating <= 10.0:
            raise ValueError(f'Invalid rating: {self.rating}')
        if not self.votes > 0:
            raise ValueError(f'Invalid votes: {self.votes}')

    def to_dict(self) -> dict[str, t.Any]:
        """Convert MovieChart to dictionary."""
        return {
            'title': self.title,
            'url': self.url,
            'rating': float(self.rating),
            'votes': int(self.votes),
            'year': int(self.year),
            'rank': int(self.rank),
            'oscars_won': int(self.oscars_won),
            'penalized': bool(self.penalized),
        }


def normalize(movies_df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize the movies dataframe.

    Args:
        movies_df (pd.DataFrame): Raw movie data DataFrame.

    Returns:
        pd.DataFrame: Normalized DataFrame with proper types.

    Raises:
        KeyError: If required columns are missing.
        ValueError: If data normalization fails.
    """
    # Create a copy
    df = movies_df.copy()

    # Check required columns
    required_columns = ['rating', 'votes']
    missing_columns = [col for col in required_columns if col not in df.columns]

    logger.debug(
        'Input DataFrame columns',
        columns=df.columns.tolist(),
    )
    if missing_columns:
        logger.error(
            'Missing required columns',
            missing_columns=missing_columns,
        )
        logger.error(
            'Available columns',
            available_columns=df.columns.tolist(),
        )
        raise KeyError(f'Missing required columns: {missing_columns}')

    try:
        # Convert types safely with proper error handling
        if 'year' in df.columns:
            df['year'] = (
                pd.to_numeric(df['year'].astype(str).str.strip('()'), errors='coerce')
                .fillna(2000)
                .astype(int)
            )

        df['rating'] = pd.to_numeric(df['rating'], errors='coerce').fillna(0.0).astype(float)
        df['votes'] = (
            pd.to_numeric(df['votes'].astype(str).str.replace(',', ''), errors='coerce')
            .fillna(0)
            .astype(int)
        )

        if 'rank' in df.columns:
            df['rank'] = pd.to_numeric(df['rank'], errors='coerce').fillna(0).astype(int)

        if 'oscars_won' in df.columns:
            df['oscars_won'] = (
                pd.to_numeric(df['oscars_won'], errors='coerce').fillna(0).astype(int)
            )

        # Ensure penalized is boolean
        if 'penalized' in df.columns:
            df['penalized'] = df['penalized'].astype(bool)
        else:
            df['penalized'] = False

        logger.debug(f'Normalized DataFrame columns: {df.columns.tolist()}')
        return df

    except Exception as e:
        logger.error(f'Error normalizing data: {e!s}')
        raise ValueError(f'Error normalizing data: {e!s}')
