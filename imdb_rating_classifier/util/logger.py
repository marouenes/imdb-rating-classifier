"""Enhanced structured logging configuration using structlog.

This module provides a robust logging setup with:
- Timestamps
- Log levels
- Source code location
- Exception formatting
- Pretty console output
- Performance metrics
- Contextual logging
"""

from __future__ import annotations

import time
from typing import Any

import structlog
from structlog.types import EventDict, WrappedLogger

# Define log levels
DEBUG = 'debug'
INFO = 'info'
WARNING = 'warning'
ERROR = 'error'
CRITICAL = 'critical'


def add_timestamp(_, __, event_dict: EventDict) -> EventDict:
    """Add ISO-formatted timestamp."""
    event_dict['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S')
    return event_dict


def add_caller_info(_, __, event_dict: EventDict) -> EventDict:
    """Add caller information to log entries."""
    frame = structlog._frames._find_first_app_frame_and_name()[0]
    event_dict.update(
        {
            'file': frame.f_code.co_filename,
            'line': frame.f_lineno,
            'function': frame.f_code.co_name,
        }
    )
    return event_dict


def add_process_time(logger: WrappedLogger, name: str, event_dict: EventDict) -> EventDict:
    """Add process time in milliseconds."""
    if 'start_time' in event_dict:
        event_dict['duration_ms'] = (time.time() - event_dict.pop('start_time')) * 1000
    return event_dict


# Configure structlog with enhanced processors
structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        add_timestamp,
        add_caller_info,
        add_process_time,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.dev.ConsoleRenderer(
            colors=True,
            sort_keys=True,
            level_styles={
                'debug': structlog.dev.DIM,
                'info': structlog.dev.GREEN,
                'warning': structlog.dev.YELLOW,
                'error': structlog.dev.RED,
                'critical': structlog.dev.RED,
            },
        ),
    ],
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=True,
)


class Timer:
    """Context manager for timing operations."""

    def __init__(self, logger: structlog.BoundLogger, operation: str):
        self.logger = logger
        self.operation = operation

    def __enter__(self) -> Timer:
        self.start = time.time()
        return self

    def __exit__(self, *args: Any) -> None:
        duration = (time.time() - self.start) * 1000
        self.logger.info(
            f'{self.operation} completed',
            operation=self.operation,
            duration_ms=duration,
        )


def setup_logger(
    name: str | None = None, level: str = INFO, **initial_values: Any
) -> structlog.BoundLogger:
    """Set up an enhanced structured logger.

    Args:
        name: The name of the logger. If None, uses the module name.
        level: The minimum log level to output.
        **initial_values: Additional context values to bind to the logger.

    Returns:
        A configured structlog logger instance with enhanced features.

    Example:
        >>> logger = setup_logger(__name__, level="debug", service="api")
        >>> logger.info("Starting service", version="1.0.0")
        >>> with Timer(logger, "data processing"):
        ...     process_data()
    """
    logger = structlog.get_logger(name or __name__)

    # Bind initial values if provided
    if initial_values:
        logger = logger.bind(**initial_values)

    # Set log level
    logger = logger.bind(level=level)

    return logger
