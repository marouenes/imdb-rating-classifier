"""
Application entry point for generating the dataset.
"""
from __future__ import annotations

import os
import sys
from concurrent.futures import ThreadPoolExecutor

import click
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from imdb_rating_classifier import __version__  # noqa: E402
from imdb_rating_classifier.penalizer import penalize_reviews  # noqa: E402
from imdb_rating_classifier.schema import MovieChart, normalize  # noqa: E402
from imdb_rating_classifier.scraper import Scraper, get_movie_oscar_data, logger  # noqa: E402

# help context
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
# get the base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@click.group(
    invoke_without_command=True,
    context_settings=CONTEXT_SETTINGS,
    help='Application entry point for IMDB rating classifier.',
)
@click.version_option(version=__version__, prog_name='IMDB Rating Classifier')
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
    default='movies.csv',
    help='The path to the output file.',
)
@click.option(
    '--number-of-movies',
    type=click.INT,
    default=25,
    help='The number of movies to scrape.',
)
def generate(output: str, number_of_movies: int) -> None:
    """
    Generate the output dataset containing both
    the original and adjusted ratings.

    An extra JSON file will be generated alongside the csv file
    """
    # scrape IMDB movie chart data
    scraper = Scraper(
        url='https://www.imdb.com/chart/top',
        number_of_movies=number_of_movies,
    )
    movies = scraper.scrape()

    # get the oscars winners data
    logger.info('Getting the Oscar winners data...')
    # speed up the process
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(get_movie_oscar_data, [movie['url'] for movie in movies])
    # add the oscars data to the movies
    for movie, result in zip(movies, results):
        movie['oscars_won'] = result

    # convert the original set of movies to dataframe
    logger.info('Converting to original set of movies to a dataframe...')
    raw_input_df = pd.DataFrame(movies)

    # normalize the dataframe
    logger.info('Normalizing the dataframe...')
    refined_df = normalize(raw_input_df)

    # recreate the movies dict from the dataframe
    movies_dict = refined_df.to_dict(orient='records')

    # validate the movies
    logger.info('Validating the movies...')
    try:
        valid_movies = [MovieChart(**movie) for movie in movies_dict]
    except Exception as e:
        logger.error(e)
        raise
    logger.info(F'Data validation passed. The number of valid movies: {len(valid_movies)}')

    # penalize the movies based on the ruleset defined in the penalizer module
    logger.info('Penalizing movies...')
    penalized_movies = penalize_reviews(movies_dict)
    # check the number of penalized movies
    number_of_penalized_movies = len(
        [movie for movie in penalized_movies if 'penalized' in movie and movie['penalized'] is True],
    )
    logger.info(f'the number of panalized movies: {number_of_penalized_movies}')

    # convert the penalized set of movies to dataframe
    logger.info('Converting the set of penalized movies to a dataframe...')
    penalized_df = pd.DataFrame(penalized_movies)

    # sort the dataframe by rank in a descending order
    penalized_df.sort_values(by='rank', ascending=False, inplace=True)
    print(penalized_df.head())

    # save to csv
    logger.info('Saving the dataset to csv...')
    penalized_df.to_csv(output, index=False)

    # save to JSON
    logger.info('Saving a copy to JSON...')
    penalized_df.to_json(output.replace('.csv', '.json'), orient='records', indent=2)
    logger.info('Done!')


# add commands to main
main.add_command(generate)


if __name__ == '__main__':
    raise SystemExit(main())  # pragma: no cover
