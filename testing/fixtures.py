"""
Fixtures for testing
"""
from __future__ import annotations

import json
import tempfile
from typing import Any

import pytest


@pytest.fixture
def temp_dir():
    """
    Fixture to set up a temporary directory that is deleted on exit.
    """
    with tempfile.TemporaryDirectory() as directory:
        yield directory


@pytest.fixture
def assert_json_equal(left: dict[str, Any], right: dict[str, Any]):
    """
    Helper function to assert dictionary equality after sorting their keys
    """
    assert json.dumps(left, sort_keys=True) == json.dumps(right, sort_keys=True)
