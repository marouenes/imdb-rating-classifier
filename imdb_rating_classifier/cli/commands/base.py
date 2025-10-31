"""Base command class for CLI commands."""

from __future__ import annotations

import abc
from typing import Any

import click


class BaseCommand(abc.ABC):
    """Base command class that all commands should inherit from."""

    def __init__(self) -> None:
        """Initialize the command."""
        self.ctx: click.Context | None = None

    def set_context(self, ctx: click.Context) -> None:
        """Set the click context.

        Args:
            ctx: The click context object.
        """
        self.ctx = ctx

    @abc.abstractmethod
    def execute(self, **kwargs: Any) -> Any:
        """Execute the command.

        Args:
            **kwargs: Command arguments and options.

        Returns:
            Any: Command result.
        """
        raise NotImplementedError('Command must implement execute method')
