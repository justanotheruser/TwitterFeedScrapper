import logging
import os.path

import click

from twitter_feed_scrapper.commands.manual_login import manual_login_command
from twitter_feed_scrapper.commands.scrape import scrape_command
from twitter_feed_scrapper.mutually_exclusive_option import MutuallyExclusiveOption

logger = logging.getLogger('TwitterFeedScrapper')


@click.group()
def cli():
    pass


@click.command()
@click.option('--use-proxy', is_flag=True, default=False)
def manual_login(**kwargs):
    manual_login_command(kwargs['use_proxy'])


@cli.command()
@click.option("-c", "--config", default=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.ini'))
@click.option("-o", "--output", required=True)
@click.option("--last-hours", cls=MutuallyExclusiveOption, mutually_exclusive=['date', 'from-date', 'to-date'])
@click.option("--date", cls=MutuallyExclusiveOption, mutually_exclusive=['last-hours', 'from-date', 'to-date'])
@click.option("--from-date", cls=MutuallyExclusiveOption, mutually_exclusive=['last-hours', 'date'])
@click.option("--to-date", cls=MutuallyExclusiveOption, mutually_exclusive=['last-hours', 'date'])
@click.option('--headless', is_flag=True, default=False)
@click.option('--use-proxy', is_flag=True, default=False)
def scrape(**kwargs):
    scrape_command(kwargs['config'], kwargs['output'], kwargs['last_hours'], kwargs['date'], kwargs['from_date'],
                   kwargs['to_date'], kwargs['headless'], kwargs['use_proxy'])


def setup_file_logger():
    ch = logging.FileHandler('TwitterFeedScrapper.log', encoding='utf-8')
    ch.setLevel(logging.ERROR)
    ch_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    ch.setFormatter(ch_formatter)
    logger.addHandler(ch)


def setup_console_logger():
    fmt = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch = logging.StreamHandler()
    ch.setFormatter(fmt)
    logger.addHandler(ch)


if __name__ == '__main__':
    logger.setLevel(logging.INFO)
    setup_file_logger()
    setup_console_logger()

    cli.add_command(manual_login)
    cli.add_command(scrape)
    cli()
