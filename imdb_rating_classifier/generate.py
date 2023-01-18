"""
Application entry point for generating the dataset.
"""
from __future__ import annotations

import os
import sys

import click
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from imdb_rating_classifier.scraper import Scraper  # noqa: E402

# help context
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(
    invoke_without_command=True,
    context_settings=CONTEXT_SETTINGS,
    help='Application entry point for IMDB rating classifier.',
)
@click.pass_context
def main(ctx: click.Context) -> None:
    """
    Application entry point for IMDB rating classifier.

    Args:
        ctx (click.Context): The click context.
    """
    if ctx.invoked_subcommand is None:
        print(ctx.get_help())


@click.command('generate')
@click.option(
    '--output',
    '-o',
    type=click.Path(exists=False, file_okay=True, dir_okay=False),
    default='data.csv',
    help='The path to the output file.',
)
def generate(output: str) -> None:
    """
    Generate the output dataset containing both the original and adjusted ratings.

    Args:
        output (str): The path to the output file.
    """
    # scrape IMDB movie chart data
    scraper = Scraper(
        url='https://www.imdb.com/chart/top',
        number_of_movies=25,
    )
    movies = scraper.scrape()

    # convert to dataframe
    output_df = pd.DataFrame(movies)

    # save to csv
    output_df.to_csv(output, index=False)


main.add_command(generate)


if __name__ == '__main__':
    raise SystemExit(main())  # pragma: no cover
