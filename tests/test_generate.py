"""
Unit tests for imdb_rating_classifier/generate.py
"""
from __future__ import annotations

from typing import Any

import pytest
from click.testing import CliRunner

from imdb_rating_classifier.generate import generate


def test_generate(capsys: Any) -> None:
    """
    Test the generate function.
    """
    runner = CliRunner()
    result = runner.invoke(generate)
    assert result.exit_code == 0
    captured = capsys.readouterr()
    # since we are capturing the log trace, the output would change overtime.
    assert captured.out == ''


@pytest.mark.skip(reason='The verbose flag is not implemented yet')
def test_generate_with_verbose(capsys: Any) -> None:
    """
    Test the generate function with the verbose flag.
    """
    runner = CliRunner()
    result = runner.invoke(generate, ['-v'])
    assert result.exit_code == 0


def test_generate_with_invalid_flag(capsys: Any) -> None:
    """
    Test the generate function with an invalid flag.
    """
    runner = CliRunner()
    result = runner.invoke(generate, ['--invalid'])
    assert result.exit_code == 2
    captured = capsys.readouterr()
    assert captured.out == ''
