from typing import Optional

from twitter_api.api.types.v2_tweet.tweet import Tweet
from twitter_api.api.types.v2_tweet.tweet_entities_mention import TweetEntitiesMention
from twitter_api.api.types.v2_tweet.tweet_entities_url import TweetEntitiesUrl
from twitter_api.api.types.v2_tweet.tweet_id import TweetId


class ConvinientTweet(Tweet):
    @property
    def entities_urls(self) -> list[TweetEntitiesUrl]:
        if self.entities is None or self.entities.urls is None:
            return []
        else:
            return self.entities.urls

    @property
    def entities_mentions(self) -> list[TweetEntitiesMention]:
        if self.entities is None or self.entities.mentions is None:
            return []
        else:
            return self.entities.mentions

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

    @property
    def retweeted_target(self) -> Optional[TweetId]:
        """
        リツイート元の TweetID を取得する。
        """
        if self.referenced_tweets is None:
            return None

        for tweet in self.referenced_tweets:
            if tweet.type == "retweeted":
                return tweet.id

        return None

    @property
    def is_retweet(self) -> bool:
        """
        リツイートかどうか。
        """
        return self.retweeted_target is not None

    @property
    def quoted_target(self) -> Optional[TweetId]:
        """
        引用元の TweetID を取得する。
        """
        if self.referenced_tweets is None:
            return None

        for tweet in self.referenced_tweets:
            if tweet.type == "quoted":
                return tweet.id

        return None

    @property
    def is_quote(self) -> bool:
        """
        引用ツイートであるかどうか。
        """
        return self.quoted_target is not None

    @property
    def replied_target(self) -> Optional[TweetId]:
        """
        リプライ元の TweetId を取得する。
        """
        if self.referenced_tweets is None:
            return None

        for tweet in self.referenced_tweets:
            if tweet.type == "replied_to":
                return tweet.id

        return None

    @property
    def is_reply(self) -> bool:
        """
        リプライツイートであるかどうか。
        """
        return self.replied_target is not None
