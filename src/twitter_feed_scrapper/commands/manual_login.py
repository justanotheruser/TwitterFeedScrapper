from twitter_feed_scrapper.driver import get_chromedriver


def manual_login_command(use_proxy):
    driver = get_chromedriver(use_proxy=use_proxy, headless=False)
    driver.get('https://twitter.com/login')
    input()
