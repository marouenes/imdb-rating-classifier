"""Domain models for IMDB data."""

from __future__ import annotations

import re
from dataclasses import dataclass

from imdb_rating_classifier.util.logger import setup_logger

logger = setup_logger(__name__)


@dataclass
class MovieData:
    """Raw movie data from IMDB."""

    title: str
    url: str
    rating: str
    votes: str
    year: str
    rank: str
    imdb_id: str = ''
    oscars_won: int = 0
    penalized: bool = False

    def __post_init__(self):
        """Extract IMDB ID and clean data after initialization."""
        # Only extract IMDB id here. Keep rating/votes as raw strings so
        # parser tests can assert the original values. Cleaning/conversion
        # happens in CleanMovieData.from_raw.
        self.imdb_id = self.extract_imdb_id(self.url)

    @staticmethod
    def clean_rating(rating: str) -> str:
        """Clean rating string to numeric value."""
        if not rating:
            return '0.0'
        match = re.search(r'(\d+\.?\d*)', str(rating))
        return match.group(1) if match else '0.0'

    @staticmethod
    def clean_votes(votes: str) -> str:
        """Clean votes string to numeric value."""
        if not votes:
            return '0'
        return re.sub(r'[^\d]', '', str(votes))

    @staticmethod
    def extract_imdb_id(url: str) -> str:
        """Extract IMDB ID from URL."""
        match = re.search(r'/title/(tt\d+)/', url)
        return match.group(1) if match else ''


@dataclass
class CleanMovieData:
    """Normalized movie data."""

    title: str
    url: str
    rating: float
    votes: int
    year: int
    rank: int
    imdb_id: str = ''
    oscars_won: int = 0
    penalized: bool = False

    @classmethod
    def from_raw(cls, raw: MovieData) -> CleanMovieData:
        """Create clean movie data from raw data."""
        try:
            # Clean and parse rating and votes from raw strings
            # rating: extract numeric part like '9.3' from '9.3' or '9.3 out of 10'
            rating_match = re.search(r'(\d+\.?\d*)', str(raw.rating))
            rating_val = float(rating_match.group(1)) if rating_match else 0.0

            # votes: remove non-digits and parse
            votes_val = int(re.sub(r'[^\d]', '', str(raw.votes))) if raw.votes else 0

            # year: strip non-digits (handles '(1994)')
            year_match = re.search(r'(\d{4})', str(raw.year))
            year_val = int(year_match.group(1)) if year_match else 0

            return cls(
                title=str(raw.title).strip(),
                url=str(raw.url).strip(),
                rating=rating_val,
                votes=votes_val,
                year=year_val,
                rank=int(raw.rank),
                imdb_id=raw.imdb_id,
                oscars_won=raw.oscars_won,
                penalized=raw.penalized,
            )
        except (ValueError, TypeError) as e:
            logger.error(f'Error converting movie data: {e}')
            return cls(
                title=raw.title,
                url=raw.url,
                rating=0.0,
                votes=0,
                year=0,
                rank=0,
                imdb_id=raw.imdb_id,
            )
