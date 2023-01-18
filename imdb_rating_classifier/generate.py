"""
Application entry point for generating the dataset.
"""
from __future__ import annotations

import os
import sys

import click
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from imdb_rating_classifier.scraper import Scraper, logger  # noqa: E402

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


@click.command()
@click.option(
    '--output',
    type=click.Path(exists=False, file_okay=True, dir_okay=False),
    default='data.csv',
    help='The path to the output file.',
)
@click.option(
    '--number-of-movies',
    type=click.INT,
    default=25,
    help='The number of movies to scrape.',
)
def generate(output: str, number_of_movies: int = 20) -> None:
    """
    Generate the output dataset containing both
    the original and adjusted ratings.

    Args:
        output (str): The path to the output file.
    """
    # scrape IMDB movie chart data
    scraper = Scraper(
        url='https://www.imdb.com/chart/top',
        number_of_movies=number_of_movies,
    )
    movies = scraper.scrape()

    # convert to dataframe
    logger.info('Converting to dataframe...')
    output_df = pd.DataFrame(movies)

    # save to csv
    logger.info('Saving to csv...')
    output_df.to_csv(output, index=False)

    # save to JSON
    logger.info('Saving to JSON...')
    output_df.to_json(output.replace('.csv', '.json'), orient='records', indent=2)
    logger.info('Done!')


main.add_command(generate)


if __name__ == '__main__':
    raise SystemExit(main())  # pragma: no cover
