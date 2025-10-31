"""Tests for HTTP client implementations."""

from __future__ import annotations

from unittest.mock import Mock, patch

import pytest
import requests

from imdb_rating_classifier.http import RequestsClient


class TestRequestsClient:
    """Test suite for RequestsClient."""

    def setup_method(self) -> None:
        """Set up test environment."""
        self.default_headers = {'User-Agent': 'Test'}
        self.client = RequestsClient(self.default_headers)

    def test_init_with_headers(self) -> None:
        """Test client initialization with headers."""
        assert self.client.default_headers == self.default_headers

    def test_init_without_headers(self) -> None:
        """Test client initialization without headers."""
        client = RequestsClient()
        assert client.default_headers == {}

    def test_headers_merge(self) -> None:
        """Test that request headers are properly merged."""
        with patch('requests.get') as mock_get:
            mock_get.return_value = Mock(status_code=200)

            self.client.get('http://test.com', headers={'Accept': 'application/json'})

            mock_get.assert_called_once_with(
                'http://test.com',
                headers={'User-Agent': 'Test', 'Accept': 'application/json'},
            )

    def test_default_headers_not_modified(self) -> None:
        """Test that default headers are not modified by requests."""
        original_headers = self.default_headers.copy()

        with patch('requests.get') as mock_get:
            mock_get.return_value = Mock(status_code=200)

            self.client.get('http://test.com', headers={'Accept': 'application/json'})

            assert self.client.default_headers == original_headers

    def test_raises_http_error(self) -> None:
        """Test that HTTP errors are properly raised."""
        with patch('requests.get') as mock_get:
            mock_get.return_value = Mock(
                status_code=404,
                raise_for_status=Mock(side_effect=requests.HTTPError('404 Not Found')),
            )

            with pytest.raises(requests.HTTPError) as exc_info:
                self.client.get('http://test.com')

            assert '404 Not Found' in str(exc_info.value)

    @pytest.mark.parametrize(
        'status_code,response_text', [(200, 'OK'), (201, 'Created'), (204, '')]
    )
    def test_successful_responses(self, status_code: int, response_text: str) -> None:
        """Test handling of various successful response codes."""
        with patch('requests.get') as mock_get:
            mock_get.return_value = Mock(status_code=status_code, text=response_text)

            response = self.client.get('http://test.com')
            assert response.text == response_text
