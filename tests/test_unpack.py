"""
Unit tests for imdb_rating_classifier/util/unpack.py

@TODO: add unit tests
"""
from __future__ import annotations

import typing as t
from unittest.mock import patch

import pytest  # noqa: F401 # imported but unused

from imdb_rating_classifier.util.unpack import unpack_contents


def test_unpack_contents(capsys: t.Any) -> None:
    """
    Test the unpack_contents function, the request object is mocked.
    If the response returns a 200 status code, the content should be printed to the console.
    Else, it will raise an exception.

    :param capsys: pytest fixture
    """
    with patch('imdb_rating_classifier.util.unpack.requests') as mock_requests:
        mock_requests.get.return_value.status_code = 200
        mock_requests.get.return_value.text = 'test'
        unpack_contents(mock_requests.get.return_value)
        captured = capsys.readouterr()
        assert captured.out == ''


def test_unpack_contents_with_invalid_status_code(capsys: t.Any) -> None:
    """
    Test the unpack_contents function, the request object is mocked.
    If the response returns a 200 status code, the content should be printed to the console.
    Else, it will raise an exception.

    :param capsys: pytest fixture
    """
    with patch('imdb_rating_classifier.util.unpack.requests') as mock_requests:
        mock_requests.get.return_value.status_code = 404
        mock_requests.get.return_value.text = 'test'
        with pytest.raises(Exception):
            unpack_contents(mock_requests.get.return_value)
        captured = capsys.readouterr()
        assert captured.out == ''
