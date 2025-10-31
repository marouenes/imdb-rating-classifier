"""Tests for the ValidateCommand class in validate.py."""

from __future__ import annotations

import pandas as pd
import pytest

from imdb_rating_classifier.cli.commands.validate import ValidateCommand


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
