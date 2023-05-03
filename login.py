import logging
import time
import typing

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from driver_with_proxy import get_chromedriver
from twitter_acc_config import twitter_acc_config

logger = logging.getLogger('TwitterScrapper')
format = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch = logging.StreamHandler()
ch.setFormatter(format)
logger.addHandler(ch)

USERNAME_OR_EMAIL_FIELD_XPATH = '//body//input[@autocomplete="username"]'
NEXT_BUTTON_XPATH = '//body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]//div[@role="button"][2]'
PASSWORD_FIELD_XPATH = '//body//input[@name="password"]'
LOGIN_BUTTON_XPATH = '//body/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]'
BOOST_ACCOUNT_SECURITY_CLOSE_BUTTON_XPATH = '//body//div[@aria-label="Close"]'


def wait_until_element_appears(driver, xpath: str, field_name: str, raise_if_didnt=True,
                               timeout: int = 10) -> typing.Optional[WebElement]:
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
    except WebDriverException:
        if raise_if_didnt:
            logger.exception(
                f"{field_name} didn't appear!, Try setting headless=False to see what is happening")
        return None
    return driver.find_element(By.XPATH, xpath)


def main():
    driver = get_chromedriver()
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


def login(driver) -> bool:
    username_field = wait_until_element_appears(driver, USERNAME_OR_EMAIL_FIELD_XPATH, 'Username/email field')
    if not username_field:
        return False
    username_field.send_keys(twitter_acc_config.user.get_secret_value())
    next_button = wait_until_element_appears(driver, NEXT_BUTTON_XPATH, "'Next' button")
    if not next_button:
        return False
    next_button.click()
    password_field = wait_until_element_appears(driver, PASSWORD_FIELD_XPATH, 'Password field')
    if not password_field:
        return False
    password_field.send_keys(twitter_acc_config.password.get_secret_value())
    login_button = wait_until_element_appears(driver, LOGIN_BUTTON_XPATH, "'Login' button")
    if not login_button:
        return False
    login_button.click()
    return True


if __name__ == '__main__':
    main()
