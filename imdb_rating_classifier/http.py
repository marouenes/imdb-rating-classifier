"""HTTP client abstraction for making requests."""

from __future__ import annotations

import abc
from typing import Dict

import requests
from requests import Response


class HTTPClient(abc.ABC):
    """Abstract base class for HTTP clients."""

    @abc.abstractmethod
    def get(self, url: str, headers: Dict[str, str] | None = None) -> Response:
        """Make a GET request."""
        pass


class RequestsClient(HTTPClient):
    """Implementation using requests library."""

    def __init__(self, default_headers: Dict[str, str] | None = None):
        self.default_headers = default_headers or {}

    def get(self, url: str, headers: Dict[str, str] | None = None) -> Response:
        """Make a GET request with optional headers."""
        all_headers = {**self.default_headers, **(headers or {})}
        response = requests.get(url, headers=all_headers)
        response.raise_for_status()
        return response


DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
