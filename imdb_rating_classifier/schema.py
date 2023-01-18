"""
Module for predefined table/JSON schemas

The intent of this module is to define the schema for the IMDB movie chart data.
@TODO: - Validate the schema using a dataclass?
"""
from __future__ import annotations

movie_chart_schema = {
    'type': 'object',  # the schema is an object
    'properties': {  # the schema has the following properties
        'rank': {
            'type': 'integer',
        },
        'title': {
            'type': 'string',
        },
        'year': {
            'type': 'integer',
        },
        'rating': {
            'type': 'number',
        },
        'url': {
            'type': 'string',
        },
        'poster_url': {
            'type': 'string',
        },
    },
    'required': ['rank', 'title', 'year', 'rating', 'url', 'poster_url'],  # nice to have
}
