from typing import Optional

from twitter_api.api.types.v2_tweet.tweet import Tweet
from twitter_api.api.types.v2_tweet.tweet_detail import TweetDetail
from twitter_api.api.types.v2_tweet.tweet_entities_url import TweetEntitiesUrl


class ConvinientTweet(Tweet):
    @property
    def entities_urls(self) -> list[TweetEntitiesUrl]:
        if self.entities is None or self.entities.urls is None:
            return []
        else:
            return self.entities.urls

    @property
    def like_count(self) -> Optional[int]:
        if self.public_metrics is None:
            return None
        else:
            return self.public_metrics.like_count

    @property
    def retweet_count(self) -> Optional[int]:
        if self.public_metrics is None:
            return None
        else:
            return self.public_metrics.retweet_count


class ConvinientTweetDetail(TweetDetail, ConvinientTweet):
    pass
