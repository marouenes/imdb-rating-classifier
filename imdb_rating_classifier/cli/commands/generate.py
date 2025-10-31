"""Generate command implementation."""

from __future__ import annotations

import os
from typing import Any, Dict, List

import pandas as pd

from imdb_rating_classifier.cli.commands.base import BaseCommand
from imdb_rating_classifier.penalizer import penalize_reviews
from imdb_rating_classifier.schema import MovieChart, normalize
from imdb_rating_classifier.services.processor import IMDBProcessingService
from imdb_rating_classifier.services.scraper import IMDBScraperService
from imdb_rating_classifier.services.storage import FileStorageService
from imdb_rating_classifier.services.validator import IMDBValidationService
from imdb_rating_classifier.util.logger import setup_logger

logger = setup_logger(__name__)


class GenerateCommand(BaseCommand):
    """Command to generate the movie dataset with adjusted ratings."""

    def __init__(self, output: str, number_of_movies: int) -> None:
        """Initialize the generate command.

        Args:
            output: Path to the output file.
            number_of_movies: Number of movies to scrape.
        """
        super().__init__()
        self.output = output
        self.number_of_movies = number_of_movies

        # Initialize services
        self.scraper_service = IMDBScraperService()
        self.validation_service = IMDBValidationService()
        self.processing_service = IMDBProcessingService()
        self.storage_service = FileStorageService()

    def _validate_movie_data(self, movie: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and ensure required fields exist in movie data.

        Args:
            movie: Movie data dictionary.

        Returns:
            Validated movie dictionary with required fields.
        """
        required_fields = ['year', 'title', 'url', 'rating', 'votes']
        default_values = {
            'title': 'Unknown',
            'url': '',
            'year': 2000,  # Safe default year within valid range
            'rating': 0.0,
            'votes': 0,
        }

        for field in required_fields:
            if field not in movie or movie[field] is None:
                logger.warning(
                    f"Missing or null required field '{field}' in movie: {movie.get('title', 'Unknown')}"
                )
                movie[field] = default_values[field]

            # Ensure numeric fields are proper types
            if field == 'year':
                try:
                    movie['year'] = int(
                        str(movie['year']).strip('()')
                    )  # Handle year in parentheses
                except (ValueError, TypeError):
                    logger.warning(
                        f'Invalid year format for movie {movie.get("title", "Unknown")}, using default'
                    )
                    movie['year'] = default_values['year']
            elif field in ['rating', 'votes']:
                try:
                    movie[field] = float(movie[field]) if field == 'rating' else int(movie[field])
                except (ValueError, TypeError):
                    logger.warning(
                        f'Invalid {field} format for movie {movie.get("title", "Unknown")}, using default'
                    )
                    movie[field] = default_values[field]

        return movie

    def _validate_movies(self, df: pd.DataFrame) -> List[MovieChart]:
        """Validate movie data against schema.

        Args:
            df: DataFrame of movies.

        Returns:
            List of validated MovieChart objects.
        """
        logger.info('Validating the movies...')
        movies_dict = df.to_dict(orient='records')
        try:
            valid_movies = [MovieChart(**movie) for movie in movies_dict]
        except Exception as e:
            logger.error(f'Validation failed: {e}')
            raise

        logger.info(f'Data validation passed. Valid movies: {len(valid_movies)}')
        return valid_movies

    def _apply_penalties(self, movies_dict: List[Dict[str, Any]]) -> pd.DataFrame:
        """Apply rating penalties according to rules.

        Args:
            movies_dict: List of movie dictionaries.

        Returns:
            DataFrame with penalized ratings.
        """
        logger.info('Applying rating penalties...')
        penalized_movies = penalize_reviews(movies_dict)

        penalized_count = sum(1 for movie in penalized_movies if movie.get('penalized', False))
        logger.info(f'Movies penalized: {penalized_count}')

        return pd.DataFrame(penalized_movies)

    def _save_output(self, df: pd.DataFrame) -> None:
        """Save results to CSV and JSON.

        Args:
            df: DataFrame to save.
        """
        # Ensure output directory exists
        os.makedirs(os.path.dirname(os.path.abspath(self.output)), exist_ok=True)

        logger.info(
            'Saving dataset',
            location=self.output,
            buffer=df.shape[0],
        )
        df.to_csv(self.output, index=False)

        json_path = self.output.replace('.csv', '.json')
        df.to_json(json_path, orient='records', indent=2)
        logger.info(
            'Saved dataset',
            location=self.output,
            json_location=json_path,
        )

    def execute(self, **kwargs: Any) -> None:
        """Execute the generate command.

        Args:
            **kwargs: Command arguments and options.
        """
        try:
            self.output = kwargs.get('output', self.output)
            self.number_of_movies = kwargs.get('number_of_movies', self.number_of_movies)

            # Step 1: Fetch and validate raw movie data
            movies = self.scraper_service.fetch_movies(self.number_of_movies)
            movies = [self.validation_service.validate_movie(movie) for movie in movies]

            # Step 2: Enrich with Oscar data
            movies = self.scraper_service.enrich_with_oscars(movies)

            # Step 3: Convert to DataFrame and normalize
            raw_df = pd.DataFrame(movies)
            refined_df = normalize(raw_df)

            # Step 4: Validate against schema
            validated_movies = self.validation_service.validate_movies(refined_df)

            # Step 5: Convert to dictionaries
            movies_dict = [movie.to_dict() for movie in validated_movies]

            # Step 6: Apply penalties
            penalized_df = self.processing_service.apply_penalties(movies_dict)

            # Step 7: Save results
            self.storage_service.save(penalized_df, self.output)

            # Display preview
            logger.info(
                'Top 5 movies preview',
                movie_data=penalized_df.head().to_dict(orient='records'),
            )

        except Exception as e:
            logger.error(f'Failed to process movies: {e!s}')
            logger.error(f'Error type: {type(e).__name__}')
            logger.error('Full traceback:', exc_info=True)
            raise
