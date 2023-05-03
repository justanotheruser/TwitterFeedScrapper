from twitter_feed_scrapper.scrapping.login import login

FOLLOWING_XPATH = '//body//div[@aria-label="Home timeline"]//span[text()="Following"]'


def scrape(driver, tweeted_after, tweeted_before):
    if not login(driver):
        raise Exception('Failed to login')

    data = []
    return data
