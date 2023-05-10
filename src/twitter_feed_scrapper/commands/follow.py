import math

import tqdm

FOLLOW_BUTTON_XPATH = '//body//main//div[@aria-label="Home timeline"]//div[@data-testid="placementTracking"]//span[' \
                      'text()="Follow"]'
import logging
from typing import Optional

from twitter_feed_scrapper.config import read_config, Credentials
from twitter_feed_scrapper.driver import get_chromedriver
from twitter_feed_scrapper.web.login import login
from twitter_feed_scrapper.web.follow import follow

logger = logging.getLogger('TwitterFeedScrapper')


def follow_command(config_path: str, users_file: str, headless: bool, use_proxy: bool):
    if not (config := read_config(config_path)):
        return
    if (users2follow := read_users(users_file)) is None:
        return
    # TODO: write users_above_limit to a file
    users2follow, users_above_limit = chunk(users2follow, len(config.credentials),
                                            max_per_account=config.follow.max_per_account)
    logger.info(f"Chunks: {users2follow}")
    for i in range(len(config.credentials)):
        follow_from_account(creds=config.credentials[i], users2follow=users2follow[i], use_proxy=use_proxy,
                            headless=headless)


def follow_from_account(creds: Credentials, users2follow: list[str], use_proxy: bool, headless: bool):
    logger.info("Запускаем браузер")
    driver = get_chromedriver(use_proxy=use_proxy, headless=headless)
    login(driver, creds)
    logger.info("Подписываемся на аккаунты")
    for user in tqdm.tqdm(users2follow):
        follow(driver, user)


def read_users(input_file: str) -> Optional[list[str]]:
    logger.info("Читаем файл с аккаунтами, на которые нужно подписаться")
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except OSError as e:
        logger.error(e)
        return None
    return [line[:-1] if line[-1] == '\n' else line for line in lines]


def chunk(user2follow: list[str], n_accounts: int, max_per_account: int):
    max_total = n_accounts * max_per_account
    if max_total > len(user2follow):
        users_we_can_follow, users_above_limit = user2follow[:max_total], user2follow[max_total:]
    else:
        users_we_can_follow, users_above_limit = user2follow, None
    chunked_users = []
    chunk_size = math.ceil(len(users_we_can_follow) / n_accounts)
    while users_we_can_follow:
        real_chunk_size = min(chunk_size, len(users_we_can_follow))
        chunked_users.append(users_we_can_follow[:real_chunk_size])
        users_we_can_follow = users_we_can_follow[real_chunk_size:]
    assert len(chunked_users) == n_accounts
    return chunked_users, users_above_limit
