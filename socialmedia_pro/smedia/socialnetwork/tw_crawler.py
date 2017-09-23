from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import date, timedelta, datetime
import pprint


class TwitterTweet:
    def __init__(self, htag):
        self.htag = htag.replace("#", "")

    def get_tweet_month(self):
        driver = webdriver.Chrome()
        # driver = self.driver
        driver.get("https://twitter.com/hashtag/" + self.htag + "?f=tweets")
        # tss = driver.find_elements_by_xpath('//span[contains(@class, "_timestamp js-short-timestamp js-relative-timestamp")]')
        # ts = [datetime.fromtimestamp(int(ts.get_attribute('data-time'))).strftime('%Y-%m-%d') == str(date.today()) for ts in tss]
        chk = True
        while chk:
            tss = driver.find_elements_by_xpath(
                '//span[contains(@class, "_timestamp js-short-timestamp js-relative-timestamp")]')
            for ts in tss:
                ts_time = datetime.fromtimestamp(int(ts.get_attribute('data-time'))).strftime('%Y-%m-%d')
                if ts_time != str(date.today()-timedelta(1)):
                    driver.find_element_by_tag_name("body").send_keys(Keys.END)
                    driver.implicitly_wait(10)
                else:
                    chk = False
        # driver.find_element_by_tag_name("body").send_keys(Keys.END)
        lies = driver.find_elements_by_xpath('//li[contains(@id, "stream-item-tweet-")]')
        tweet = []
        for li in lies:
            tweet.append(li.find_element_by_xpath('.//span[@class="_timestamp js-short-timestamp js-relative-timestamp"]').text)
        return tweet


# tt = TwitterTweet("#lalbaugcharaja")
# pprint.pprint(tt.get_tweet_month())
