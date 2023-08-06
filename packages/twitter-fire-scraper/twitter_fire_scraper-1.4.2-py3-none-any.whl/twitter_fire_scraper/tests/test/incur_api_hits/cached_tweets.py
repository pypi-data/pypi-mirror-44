"""
This is a utility to provide a large amount of tweets to unit tests WITHOUT repeatedly incurring API hits.

This is cached in MEMORY, not to disk.

The idea here is this file gets run once and its data used repeatedly, instead of scraping the same terms again and again.

This is not strictly necessary, but will decrease API calls significantly if you don't care about reusing tweets.
"""
from typing import Dict, List

from tweepy import Status

from twitter_fire_scraper.scraper import TwitterAuthentication, Scraper

from functools import lru_cache

class CachedTweets:

    scraper = Scraper(twitter_authentication=TwitterAuthentication.autodetect_twitter_auth())

    @staticmethod
    @lru_cache(maxsize=None)
    def tweets_small():
        # type: () -> Dict[str, List[Status]]
        """Return a static list of 9 tweets that is generated once and re-used throughout the module's lifetime."""
        return CachedTweets.scraper.scrape_terms({"flood", "fire", "house fire"}, count=3)

    @staticmethod
    @lru_cache(maxsize=None)
    def tweets_medium():
        # type: () -> Dict[str, List[Status]]
        """Return a static list of 60 tweets that is generated once and re-used throughout the module's lifetime."""
        return CachedTweets.scraper.scrape_terms({"flood", "fire", "house fire"}, count=20)

    @staticmethod
    @lru_cache(maxsize=None)
    def tweets_large():
        # type: () -> Dict[str, List[Status]]
        """Return a static list of 300 tweets that is generated once and re-used throughout the module's lifetime."""
        return CachedTweets.scraper.scrape_terms({"flood", "fire", "house fire"}, count=100)