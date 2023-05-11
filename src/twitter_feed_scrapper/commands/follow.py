import logging
import math
from typing import Optional

import tqdm

from twitter_feed_scrapper.config import read_config, Credentials
from twitter_feed_scrapper.driver import get_chromedriver
from twitter_feed_scrapper.web.follow import follow
from twitter_feed_scrapper.web.login import login

logger = logging.getLogger('TwitterFeedScrapper')


def follow_command(config_path: str, users_file: str, output_file: str, headless: bool, use_proxy: bool):
    if not (config := read_config(config_path)):
        return
    if (users2follow := read_users(users_file)) is None:
        return
    users2follow, users_above_limit = chunk(users2follow, len(config.credentials),
                                            max_per_account=config.follow.max_per_account)
    logger.info(f"Chunks: {users2follow}")
    following, not_following = [], []
    for i in tqdm.tqdm(range(len(config.credentials))):
        following_i, failed_i, non_existing_i = follow_from_account(creds=config.credentials[i],
                                                                  users2follow=users2follow[i],
                                                                  use_proxy=use_proxy, headless=headless)
        following.extend(following_i)
        logger.info(f"Подписались на {len(following_i)} аккаунтов")
        logger.info(f"Аккаунты {non_existing_i} не существуют")
        not_following.extend(failed_i)
    if users_above_limit:
        not_following.extend(users_above_limit)
    write_output(output_file, not_following)


def follow_from_account(creds: Credentials, users2follow: list[str], use_proxy: bool, headless: bool) -> (
        list[str], list[str]):
    logger.info("Запускаем браузер")
    driver = get_chromedriver(use_proxy=use_proxy, headless=headless)
    login(driver, creds)
    logger.info("Подписываемся на аккаунты")
    following, failed, non_existing = [], [], []
    for user in tqdm.tqdm(users2follow):
        if result := follow(driver, user):
            following.append(user)
        elif result is False:
            failed.append(user)
        else:
            non_existing.append(user)
    driver.close()
    driver.quit()
    return following, failed, non_existing


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
    if max_total < len(user2follow):
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


def write_output(file: str, not_following_users: list[str]):
    with open(file, mode='w', encoding='utf-8') as f:
        for user in not_following_users:
            f.write(user + '\n')
