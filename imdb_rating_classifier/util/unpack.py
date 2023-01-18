"""
Helpers and utilities for the imdb_rating_classifier app.
"""
from __future__ import annotations

import json
import typing as t

import requests


def unpack_contents(response: requests.Response, cutoff: str = None) -> list[dict[str, t.Any]]:
    """
    Helper method to unpack the contents from request response,
    reporting errors in a helpful manner, if any.
    """
    try:
        if response.status_code == 200 and cutoff is None:
            return response
        elif response.status_code == 200 and cutoff == 'dict':
            return response.json()
        else:
            raise Exception(
                f'Exception: {response.status_code} - {response.reason}',
                f'Traceback: {response.text}',
            )

    except json.decoder.JSONDecodeError as err:
        raise Exception(f'Error: {err}') from err
