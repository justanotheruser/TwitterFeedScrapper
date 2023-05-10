import tqdm

FOLLOW_BUTTON_XPATH = '//body//main//div[@aria-label="Home timeline"]//div[@data-testid="placementTracking"]//span[' \
                      'text()="Follow"]'
import logging
from typing import Optional

from twitter_feed_scrapper.config import read_config
from twitter_feed_scrapper.driver import get_chromedriver
from twitter_feed_scrapper.web.login import login
from twitter_feed_scrapper.web.follower import follow

logger = logging.getLogger('TwitterFeedScrapper')


def follow_command(config_path: str, users_file: str, headless: bool, use_proxy: bool):
    if not (config := read_config(config_path)):
        return
    if (users := read_users(users_file)) is None:
        return
    logger.info("Запускаем браузер")
    driver = get_chromedriver(use_proxy=use_proxy, headless=headless)
    login(driver, config.credentials[0])
    logger.info("Подписываемся на аккаунты")
    for user in tqdm.tqdm(users):
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
