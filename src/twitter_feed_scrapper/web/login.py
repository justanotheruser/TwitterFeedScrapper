import logging
import time

from twitter_feed_scrapper.config import Credentials
from twitter_feed_scrapper.driver import get_chromedriver
from twitter_feed_scrapper.web.driver_utils import Utilities

logger = logging.getLogger('TwitterFeedScrapper')

USERNAME_OR_EMAIL_FIELD_XPATH = '//body//input[@autocomplete="username"]'
NEXT_BUTTON_XPATH = '//body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]//div[@role="button"][2]'
PASSWORD_FIELD_XPATH = '//body//input[@name="password"]'
LOGIN_BUTTON_XPATH = '//body/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]'


def login(driver, creds: Credentials) -> bool:
    logger.info(f"Логинимся как {creds.user}")
    driver.get("https://twitter.com/login")
    username_field = Utilities.wait_until_element_appears(driver, USERNAME_OR_EMAIL_FIELD_XPATH,
                                                          'Username/email field', timeout=20)
    if not username_field:
        return False
    username_field.send_keys(creds.user)
    next_button = Utilities.wait_until_element_appears(driver, NEXT_BUTTON_XPATH, "'Next' button")
    if not next_button:
        return False
    next_button.click()
    password_field = Utilities.wait_until_element_appears(driver, PASSWORD_FIELD_XPATH, 'Password field')
    if not password_field:
        return False
    password_field.send_keys(creds.password)
    Utilities.wait_until_completion(driver)
    login_button = Utilities.wait_until_element_appears(driver, LOGIN_BUTTON_XPATH, "'Login' button")
    if not login_button:
        return False
    login_button.click()
    Utilities.wait_until_completion(driver)
    return True


# For testing
def main():
    driver = get_chromedriver(use_proxy=True, headless=False)
    try:
        driver.get("https://twitter.com/login")
        time.sleep(5)
        driver.get("https://twitter.com/login")
        if not login(driver):
            raise Exception('Failed to login')
        print('OK')
    except Exception as e:
        logger.exception(e)
    finally:
        driver.close()
        driver.quit()


if __name__ == '__main__':
    main()
