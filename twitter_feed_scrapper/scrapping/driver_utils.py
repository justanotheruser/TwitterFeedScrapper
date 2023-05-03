import logging
import time
from random import randint
from typing import Optional

from selenium.common import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

logger = logging.getLogger('TwitterFeedScrapper')


class Utilities:
    """
    this class contains all the method related to driver behaviour,
    like scrolling, waiting for element to appear, it contains all static
    method, which accepts driver instance as a argument

    @staticmethod
    def method_name(parameters):
    """

    @staticmethod
    def wait_until_tweets_appear(driver) -> Optional[WebElement]:
        """Wait for tweet to appear. Helpful to work with the system facing
        slow internet connection issues
        """
        timeline_css_selector = '[aria-label="Timeline: Your Home Timeline"]'
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, timeline_css_selector)))
        except WebDriverException:
            logger.exception(
                "Tweets did not appear!, Try setting headless=False to see what is happening")
            return None
        return driver.find_element(By.CSS_SELECTOR, timeline_css_selector)

    @staticmethod
    def scroll_down(driver) -> None:
        """Helps to scroll down web page"""
        try:
            body = driver.find_element(By.CSS_SELECTOR, 'body')
            for _ in range(randint(1, 3)):
                body.send_keys(Keys.PAGE_DOWN)
        except Exception as ex:
            logger.exception("Error at scroll_down method {}".format(ex))

    @staticmethod
    def wait_until_completion(driver) -> None:
        """waits until the page have completed loading"""
        try:
            state = ""
            while state != "complete":
                time.sleep(randint(3, 5))
                state = driver.execute_script("return document.readyState")
        except Exception as ex:
            logger.exception('Error at wait_until_completion: {}'.format(ex))

    @staticmethod
    def wait_until_element_appears(driver, xpath: str, field_name: str, raise_if_didnt=True,
                                   timeout: int = 10) -> Optional[WebElement]:
        try:
            WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
        except WebDriverException:
            if raise_if_didnt:
                logger.exception(
                    f"{field_name} didn't appear!, Try setting headless=False to see what is happening")
            return None
        return driver.find_element(By.XPATH, xpath)
