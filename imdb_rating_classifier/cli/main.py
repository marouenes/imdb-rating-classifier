"""CLI entrypoint module."""

from __future__ import annotations

import click

from imdb_rating_classifier import __version__
from imdb_rating_classifier.cli.commands.generate import GenerateCommand
from imdb_rating_classifier.cli.commands.validate import ValidateCommand
from imdb_rating_classifier.util.logger import setup_logger

logger = setup_logger(__name__)

# CLI context settings
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(
    invoke_without_command=True,
    context_settings=CONTEXT_SETTINGS,
    help='IMDB rating classifier CLI.',
)
@click.version_option(version=__version__, prog_name='IMDB Rating Classifier')
@click.pass_context
def cli(ctx: click.Context) -> None:
    """IMDB rating classifier command-line interface.

    Process IMDB movie data and apply rating adjustments based on defined rules.
    """
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command()
@click.option(
    '--output',
    type=click.Path(dir_okay=False),
    default='movies.csv',
    help='Output file path for the dataset.',
)
@click.option(
    '--number-of-movies',
    type=click.IntRange(min=1),
    default=25,
    help='Number of top movies to process.',
)
@click.pass_context
def generate(ctx: click.Context, output: str, number_of_movies: int) -> None:
    """Generate dataset with original and adjusted movie ratings.

    Scrapes movie data from IMDB, applies rating adjustments based on
    defined rules, and saves the results to CSV and JSON formats.
    """
    try:
        cmd = GenerateCommand(output=output, number_of_movies=number_of_movies)
        cmd.set_context(ctx)
        cmd.execute()
    except Exception as e:
        logger.error(f'Command failed: {e}')
        raise click.ClickException(str(e))


@cli.command()
@click.argument('input_path', type=click.Path(exists=True, dir_okay=False))
@click.pass_context
def validate(ctx: click.Context, input_path: str) -> None:
    """Validate a dataset file (CSV or JSON) against the movie schema."""
    try:
        cmd = ValidateCommand(input_path=input_path)
        cmd.set_context(ctx)
        cmd.execute()
    except Exception as e:
        logger.error(f'Command failed: {e}')
        raise click.ClickException(str(e))


if __name__ == '__main__':
    raise SystemExit(cli())  # pragma: no cover
