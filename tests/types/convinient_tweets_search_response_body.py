from typing import Optional

from pydantic import Field

from tests.types.convinient_tweet import ConvinientTweetDetail
from twitter_api.api.types.v2_tweet.tweet_id import TweetId
from twitter_api.api.types.v2_user.user import User
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel


class ConvinientTweetsSearchResponseBodyIncludes(ExtraPermissiveModel):
    users: list[User] = Field(default_factory=list)
    tweets: list[ConvinientTweetDetail] = Field(default_factory=list)


class ConvinientTweetsSearchResponseBodyMeta(ExtraPermissiveModel):
    result_count: int
    next_token: Optional[str] = None
    newest_id: Optional[TweetId] = None
    oldest_id: Optional[TweetId] = None


class ConvinientTweetsSearchResponseBody(ExtraPermissiveModel):
    data: list[ConvinientTweetDetail] = Field(default_factory=list)
    includes: Optional[ConvinientTweetsSearchResponseBodyIncludes] = None
    meta: ConvinientTweetsSearchResponseBodyMeta
    errors: Optional[list[dict]] = None

    def find_tweet(self, id: TweetId) -> Optional[ConvinientTweetDetail]:
        """
        TweetId からツイートを検索する。
        """

        for tweet in self.data:
            if tweet.id == id:
                return tweet

        if self.includes is None:
            return None

        for tweet in self.includes.tweets:
            if tweet.id == id:
                return tweet

        return None

    def retweeted_by(
        self, retweet: TweetId | ConvinientTweetDetail
    ) -> Optional[ConvinientTweetDetail]:
        """
        リツイート元のツイートを返す。
        """

        if self.includes is None:
            return None

        if isinstance(retweet, str):
            retweeted_id = retweet
        else:
            if retweet.retweeted_target is None:
                return None
            retweeted_id = retweet.retweeted_target

        for tweet in self.includes.tweets:
            if retweeted_id == tweet.id:
                return tweet

        return None

    def quoted_by(
        self, quote_tweet: TweetId | ConvinientTweetDetail
    ) -> Optional[ConvinientTweetDetail]:
        """
        引用元のツイートを返す。
        """

        if self.includes is None:
            return None

        if isinstance(quote_tweet, str):
            quote_tweet_id = quote_tweet
        else:
            if quote_tweet.quoted_target is None:
                return None
            quote_tweet_id = quote_tweet.quoted_target

        for tweet in self.includes.tweets:
            if quote_tweet_id == tweet.id:
                return tweet

        return None

    def replied_by(
        self, reply_tweet: TweetId | ConvinientTweetDetail
    ) -> Optional[ConvinientTweetDetail]:
        """
        返信元のツイートを返す。
        """

        if self.includes is None:
            return None

        if isinstance(reply_tweet, str):
            reply_tweet_id = reply_tweet
        else:
            if reply_tweet.replied_target is None:
                return None
            reply_tweet_id = reply_tweet.replied_target

        for tweet in self.includes.tweets:
            if reply_tweet_id == tweet.id:
                return tweet

        return None
