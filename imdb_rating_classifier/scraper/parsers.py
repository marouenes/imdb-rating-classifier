"""HTML parsers for IMDB data."""

from __future__ import annotations

from typing import Sequence

from bs4 import BeautifulSoup, Tag

from imdb_rating_classifier.models import MovieData
from imdb_rating_classifier.util.logger import setup_logger

logger = setup_logger(__name__)


class IMDBParser:
    """Parser for IMDB movie chart HTML."""

    # Updated selectors for the new IMDB layout
    MOVIE_CHART_SELECTOR = 'ul.ipc-metadata-list li.ipc-metadata-list-summary-item'
    MOVIE_TITLE_SELECTOR = 'h3.ipc-title__text'
    MOVIE_RATING_SELECTOR = 'span.ipc-rating-star--imdb'
    MOVIE_VOTES_SELECTOR = 'span.ipc-rating-star--voteCount'
    MOVIE_YEAR_SELECTOR = 'span.cli-title-metadata-item'

    def __init__(self, html_content: str):
        """Initialize parser with HTML content."""
        self.soup = BeautifulSoup(html_content, 'html.parser')

    def parse_movies(self) -> Sequence[MovieData]:
        """Parse movie data from HTML."""
        logger.info('Parsing IMDB movie chart data...')
        movies = []
        chart_items = self.soup.select(self.MOVIE_CHART_SELECTOR)

        logger.debug(f'Found {len(chart_items)} movie items')
        if not chart_items:
            logger.debug('HTML content preview:')
            logger.debug(self.soup.prettify()[:500])  # First 500 chars for debug
        # First try the new layout
        for idx, item in enumerate(chart_items, 1):
            try:
                movie = self._parse_movie_row(item, idx)
                if movie:
                    movies.append(movie)
            except Exception as e:
                logger.error(f'Error parsing movie {idx}: {e!s}')
                continue

        # If nothing found using the new layout, try legacy table-based layout
        if not movies:
            legacy_rows = self.soup.select('tbody.lister-list tr')
            logger.debug(f'Found {len(legacy_rows)} legacy rows')
            for idx, row in enumerate(legacy_rows, 1):
                movie = self._parse_movie_row_legacy(row)
                if movie:
                    movies.append(movie)

        return movies

    def _parse_movie_row(self, item: Tag, rank: int) -> MovieData | None:
        """Parse a single movie item.

        Args:
            item: The movie item element
            rank: The movie's rank in the list

        Returns:
            MovieData object or None if parsing fails
        """
        try:
            # Get title and URL
            title_elem = item.select_one(self.MOVIE_TITLE_SELECTOR)
            if not title_elem:
                logger.error(f'No title found for movie {rank}')
                return None

            # Title format is typically "1. Movie Title"
            title = title_elem.text.split('. ', 1)[-1].strip()
            url = title_elem.parent.get('href', '')

            # Get year from metadata
            year = self._get_year(item)

            # Get rating and votes
            rating_elem = item.select_one(self.MOVIE_RATING_SELECTOR)
            rating = rating_elem.get('aria-label', '0').split(' ')[0] if rating_elem else '0'

            votes_elem = item.select_one(self.MOVIE_VOTES_SELECTOR)
            votes = votes_elem.text.strip('()').replace(',', '') if votes_elem else '0'

            return MovieData(
                rank=str(rank),
                title=title,
                year=year,
                rating=rating,
                votes=votes,
                url=f'https://www.imdb.com{url}' if url else '',
            )

        except Exception as e:
            logger.error(f'Failed to parse movie {rank}: {e!s}')
            logger.debug(f'Item HTML: {item.prettify()}')
            return None

    def _get_year(self, item: Tag) -> str:
        """Extract year from metadata items."""
        try:
            metadata_items = item.select(self.MOVIE_YEAR_SELECTOR)
            for meta in metadata_items:
                text = meta.text.strip()
                if text.isdigit() and len(text) == 4:
                    return text
        except Exception as e:
            logger.error(f'Error extracting year: {e!s}')
        return '0'

    # --- Legacy parsing helpers ---
    def _parse_movie_row_legacy(self, row: Tag) -> MovieData | None:
        """Parse movie row from legacy table layout."""
        try:
            rank = row.select_one('td.titleColumn')
            title_elem = row.select_one('td.titleColumn a')
            year_elem = row.select_one('td.titleColumn span.secondaryInfo')
            rating_elem = row.select_one('td.ratingColumn strong')

            if not title_elem:
                return None

            title = title_elem.text.strip()
            # keep year as-is (including parentheses) to match legacy HTML expectations
            year = year_elem.text.strip() if year_elem else '(0)'
            url = title_elem.get('href', '')

            # rating text is inside the strong tag
            rating = rating_elem.text.strip() if rating_elem else '0'

            # votes may be inside the title attribute of the strong tag
            votes_attr = rating_elem.get('title', '') if rating_elem else ''
            # extract the first number found (e.g. 2,456,789) and keep commas
            import re

            votes_matches = re.findall(r'(\d[\d,]*)', votes_attr)
            # pick the last numeric group (typically the votes with commas)
            votes = votes_matches[-1] if votes_matches else '0'

            return MovieData(
                rank=(rank.text.strip().split('.')[0] if rank is not None else '0'),
                title=title,
                year=year,
                rating=rating,
                votes=votes,
                url=url,
            )
        except Exception as e:
            logger.error(f'Failed to parse legacy row: {e!s}')
            logger.debug(f'Row HTML: {row.prettify()}')
            return None


class IMDBMovieParser:
    """Parser for individual IMDB movie pages."""

    OSCAR_SELECTOR = '.ipc-metadata-list-item__label'

    def __init__(self, html_content: str):
        """Initialize parser with HTML content."""
        self.soup = BeautifulSoup(html_content, 'html.parser')

    def parse_oscar_count(self) -> int:
        """Parse number of Oscar wins."""
        try:
            # Use CSS selector to find relevant metadata label elements
            elements = self.soup.select(self.OSCAR_SELECTOR)
            for element in elements:
                text = element.get_text(strip=True).split()
                # Expect patterns like: ['Won', '7', 'Oscars.'] or similar
                if (
                    len(text) >= 2
                    and text[0].lower() == 'won'
                    and any('oscar' in s.lower() for s in text)
                ):
                    try:
                        return int(text[1])
                    except (ValueError, IndexError):
                        # not an int, continue searching
                        continue
        except Exception as e:
            logger.error(f'Failed to parse Oscar count: {e}')

        return 0
