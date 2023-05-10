import configparser
import logging
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger('TwitterFeedScrapper')


@dataclass(repr=False)
class Credentials:
    user: str
    password: str


@dataclass
class Follow:
    max_per_account: int


@dataclass
class Config:
    credentials: list[Credentials]
    follow: Follow


def read_config(config_path: str) -> Optional[Config]:
    raw_config = configparser.ConfigParser()
    if not raw_config.read(config_path, encoding='utf-8'):
        logger.critical(f"Can't read config {config_path}")
        return None
    try:
        if 'credentials' not in raw_config:
            raise ValueError('No credentials for Twitter authorization provided')
        credentials = read_credentials(raw_config['credentials'])
        follow = read_follow(raw_config['follow'])
        return Config(credentials=credentials, follow=follow)
    except ValueError as e:
        logger.critical(f'Failed to read config: {e}')
        return None


def read_credentials(cfg) -> list[Credentials]:
    users = get_list(cfg, 'users')
    passwords = get_list(cfg, 'passwords')
    if len(users) != len(passwords):
        raise ValueError('Number of users is not equal to number of passwords')
    return [Credentials(user=user, password=password) for user, password in zip(users, passwords)]


def read_follow(cfg) -> Follow:
    try:
        return Follow(max_per_account=int(cfg.get('max_per_account')))
    except Exception:
        raise ValueError('Failed to read [follow] from config')


def get_list(cfg, list_name):
    if not (single_line_list := cfg.get(list_name, '')):
        return []
    return [x.strip() for x in single_line_list.split(',')]
