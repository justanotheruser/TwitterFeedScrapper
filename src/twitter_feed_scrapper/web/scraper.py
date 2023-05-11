import logging
from datetime import datetime
from typing import Optional

from selenium.common.exceptions import StaleElementReferenceException

from twitter_feed_scrapper.web.driver_utils import Utilities
from twitter_feed_scrapper.web.element_finder import Finder
from twitter_feed_scrapper.web.login import login
from twitter_feed_scrapper.config import Credentials

logger = logging.getLogger('TwitterFeedScrapper')

BOOST_ACCOUNT_SECURITY_CLOSE_BUTTON_XPATH = '//body//div[@aria-label="Close"]'
FOLLOWING_XPATH = '//body//div[@aria-label="Home timeline"]//span[text()="Following"]'


class Scrapper:
    def __init__(self, driver, credentials: Credentials, tweeted_after: datetime, tweeted_before: Optional[datetime]):
        self.driver = driver
        self.credentials = credentials
        self.tweeted_before = tweeted_before
        self.tweeted_after = tweeted_after
        self.posts_data = {}
        self.retry = 10

    def scrape(self):
        if not login(self.driver, self.credentials):
            logger.error('Failed to login')
            return None
        Utilities.wait_until_completion(self.driver)
        boost_account_security_close_button = Utilities.wait_until_element_appears(
            self.driver, BOOST_ACCOUNT_SECURITY_CLOSE_BUTTON_XPATH, '', raise_if_didnt=False, timeout=2)
        if boost_account_security_close_button:
            boost_account_security_close_button.click()
        following_tab = Utilities.wait_until_element_appears(self.driver, FOLLOWING_XPATH, "'Following' tab")
        if not following_tab:
            return None
        try:
            # TODO: check for modal window
            following_tab.click()
        except Exception as e:
            logger.exception(f"Exception on clicking 'Following' tab: {e}")
        timeline = Utilities.wait_until_tweets_appear(self.driver)
        if not timeline:
            return None
        self.__fetch_and_store_data()
        data = dict(list(self.posts_data.items()))
        return data

    def __fetch_and_store_data(self):
        try:
            already_processed_tweets = []
            while self.retry > 0:
                Utilities.wait_until_completion(self.driver)
                Utilities.wait_until_tweets_appear(self.driver)
                all_tweets = Finder.find_all_tweets(self.driver)
                if len(all_tweets) == 0:
                    self.retry -= 1
                    continue
                new_tweets = [post for post in all_tweets if post not in already_processed_tweets]
                try:
                    found_all_new_tweets = self.parse_tweets(new_tweets)
                except StaleElementReferenceException:
                    self.retry -= 1
                    continue
                if found_all_new_tweets:
                    break
                already_processed_tweets.extend(new_tweets)
                Utilities.scroll_down(self.driver)

        except Exception as ex:
            logger.exception(
                "Error at method fetch_and_store_data : {}".format(ex))

    def parse_tweets(self, tweets):
        for tweet in tweets:
            status, tweet_url = Finder.find_status(tweet)
            replies = Finder.find_replies(tweet)
            retweets = Finder.find_shares(tweet)
            status = status[-1]
            username = tweet_url.split("/")[3]
            is_retweet = Finder.is_retweet(tweet)
            posted_time = Finder.find_timestamp(tweet)
            content = Finder.find_content(tweet)
            likes = Finder.find_like(tweet)
            link = Finder.find_external_link(tweet)
            tweet_datetime = Finder.find_timestamp(tweet)
            # self.tweeted_after <= tweet_datetime < self.tweeted_before
            if not is_retweet and self.tweeted_before and tweet_datetime >= self.tweeted_before:
                continue
            if not is_retweet and tweet_datetime < self.tweeted_after:
                return True
            self.posts_data[status] = {
                "tweet_id": status,
                "username": username,
                "replies": replies,
                "retweets": retweets,
                "likes": likes,
                "is_retweet": is_retweet,
                "posted_time": posted_time,
                "content": content,
                "tweet_url": tweet_url,
                "link": link,
                "datetime": tweet_datetime
            }
        return False
