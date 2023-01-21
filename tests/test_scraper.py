"""
Unit tests for imdb_rating_classifier/scraper.py
"""
from __future__ import annotations

import pytest  # noqa: F401 # imported but unused
from bs4 import BeautifulSoup

from imdb_rating_classifier.scraper import Scraper
from testing.fixtures import load_movies_data  # noqa: F401 # imported but unused


def test_scraper_with_invalid_url() -> None:
    """
    Test the Scraper class with an invalid URL.
    """
    with pytest.raises(Exception):
        scraper = Scraper(url='https://invalid-url')
        scraper.scrape()


def test_scraper_with_no_url() -> None:
    """
    Test the Scraper class with no URL.
    """
    with pytest.raises(Exception):
        scraper = Scraper(url='')
        scraper.scrape()


def test_scraper_with_no_movies() -> None:
    """
    Test the Scraper class with no movies.
    """
    scraper = Scraper(
        url='https://www.imdb.com/chart/top', number_of_movies=0,
    )
    movies = scraper.scrape()
    # since the number of movies doesn't matter, we can just check if the list is empty
    assert movies == []


def test_scraper_with_some_movies(load_movies_data: dict) -> None:  # noqa: F811
    """
    Test the Scraper class with 10 movies.
    """
    scraper = Scraper(
        url='https://www.imdb.com/chart/top', number_of_movies=1,
    )
    movies = scraper.scrape()
    # check if the test data contains the same keys as the scraped data
    assert set(movies[0].keys()) == set(load_movies_data.keys())


def test_load_test_data() -> BeautifulSoup:
    """
    Load the test data.
    """
    with open('tests/test_data/dummy_site.html') as file:
        soup = BeautifulSoup(file.read(), 'html.parser')
        content = soup.find_all('h1')[0].text

    assert content == 'Won 3 Oscars. Another 5 wins & 5 nominations.'
