from typing import Optional

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from twitter_feed_scrapper.web.driver_utils import Utilities

FOLLOW_BUTTON_XPATH = '//body//main//div[@data-testid="placementTracking"]//div[@role="button"]'
ACCOUNT_DOESNT_EXIST_BANNER_XPATH = '//body//main//div[@data-testid="empty_state_header_text"]'


def follow(driver, user: str) -> Optional[bool]:
    try:
        driver.get(f'https://twitter.com/{user}')
        Utilities.wait_until_completion(driver)
        try:
            follow_btn = driver.find_element(By.XPATH, FOLLOW_BUTTON_XPATH)
            if 'unfollow' in follow_btn.get_attribute('data-testid'):
                return True
            follow_btn.click()
            Utilities.wait_until_completion(driver)
            if 'unfollow' in follow_btn.get_attribute('data-testid'):
                return True
            return False
        except NoSuchElementException:
            if driver.find_element(By.XPATH, ACCOUNT_DOESNT_EXIST_BANNER_XPATH):
                return None
    except Exception:
        return False
