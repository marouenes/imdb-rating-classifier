"""Tests for CLI commands."""

from __future__ import annotations

import pandas as pd
import pytest

from imdb_rating_classifier.cli.commands.generate import GenerateCommand
from imdb_rating_classifier.cli.commands.validate import ValidateCommand


class DummyGenerateCommand(GenerateCommand):
    def __init__(self):
        super().__init__(output='dummy.csv', number_of_movies=1)

    def _scrape_movies(self):
        return [
            {
                'rank': 1,
                'title': 'Test Movie',
                'year': 2023,
                'rating': 9.0,
                'votes': 1000,
                'url': '/title/tt0000001/',
                'oscars_won': 0,
                'penalized': False,
            }
        ]

    def _enrich_with_oscars(self, movies):
        for m in movies:
            m['oscars_won'] = 0
        return movies

    def _save_output(self, df):
        # Don't write files in test
        assert not df.empty


def test_generate_command_executes(monkeypatch):
    cmd = DummyGenerateCommand()
    # Patch normalize and penalize_reviews to pass through
    monkeypatch.setattr('imdb_rating_classifier.cli.commands.generate.normalize', lambda df: df)
    monkeypatch.setattr(
        'imdb_rating_classifier.cli.commands.generate.penalize_reviews',
        lambda movies: movies,
    )
    # Should not raise
    cmd.execute()


def make_test_csv(tmp_path):
    df = pd.DataFrame(
        [
            {
                'rank': 1,
                'title': 'Test Movie',
                'year': 2023,
                'rating': 9.0,
                'votes': 1000,
                'url': '/title/tt0000001/',
                'oscars_won': 0,
                'penalized': False,
            }
        ]
    )
    csv_path = tmp_path / 'test_movies.csv'
    df.to_csv(csv_path, index=False)
    return str(csv_path)


def test_validate_command_passes(tmp_path):
    csv_path = make_test_csv(tmp_path)
    cmd = ValidateCommand(input_path=csv_path)
    # Should not raise
    cmd.execute()


def test_validate_command_file_not_found():
    cmd = ValidateCommand(input_path='nonexistent.csv')
    with pytest.raises(FileNotFoundError):
        cmd.execute()


def test_validate_command_invalid_format(tmp_path):
    txt_path = tmp_path / 'test.txt'
    with open(txt_path, 'w') as f:
        f.write('not a csv or json')
    cmd = ValidateCommand(input_path=str(txt_path))
    with pytest.raises(ValueError):
        cmd.execute()
