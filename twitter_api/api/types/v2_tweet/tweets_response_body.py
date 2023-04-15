from typing import Optional

from pydantic import Field

from twitter_api.api.types.v2_media.media import Media
from twitter_api.api.types.v2_place.place import Place
from twitter_api.api.types.v2_poll.poll import Poll
from twitter_api.api.types.v2_tweet.tweet import Tweet
from twitter_api.api.types.v2_tweet.tweet_id import TweetId
from twitter_api.api.types.v2_user.user import User
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel


class TweetsResponseBodyIncludes(ExtraPermissiveModel):
    users: list[User] = Field(default_factory=list)
    tweets: list[Tweet] = Field(default_factory=list)
    places: list[Place] = Field(default_factory=list)
    media: list[Media] = Field(default_factory=list)
    polls: list[Poll] = Field(default_factory=list)


class TweetsResponseBody(ExtraPermissiveModel):
    data: list[Tweet] = Field(default_factory=list)
    includes: Optional[TweetsResponseBodyIncludes] = None
    errors: Optional[list[dict]] = None

    def find_tweet_by(self, id: TweetId | Tweet) -> Optional[Tweet]:
        """
        TweetId からツイートを検索する。

        Tweet を入力とした場合、入力した Tweet が Response の中にあるかを調べる。
        """

        if isinstance(id, Tweet):
            id = id.id

        for tweet in self.data:
            if tweet.id == id:
                return tweet

            if tweet.edit_history_tweet_ids is None:
                continue

            for tweet_id in tweet.edit_history_tweet_ids:
                if tweet_id == id:
                    return tweet

        if self.includes is None:
            return None

        for tweet in self.includes.tweets:
            if tweet.id == id:
                return tweet

            if tweet.edit_history_tweet_ids is None:
                continue

            for tweet_id in tweet.edit_history_tweet_ids:
                if tweet_id == id:
                    return tweet

        return None

    def find_retweeted_tweet_by(self, retweet: TweetId | Tweet) -> Optional[Tweet]:
        """
        リツイート元のツイートを検索する。
        """

        target = self.find_tweet_by(retweet)

        if target is None or self.includes is None:
            return None

        if target.retweeted_target is None:
            return None

        retweeted_id = target.retweeted_target

        for tweet in self.includes.tweets:
            if retweeted_id == tweet.id:
                return tweet

        return None

    def find_quoted_tweet_by(self, quote_tweet: TweetId | Tweet) -> Optional[Tweet]:
        """
        引用元のツイートを検索する。
        """

        target = self.find_tweet_by(quote_tweet)

        if target is None or self.includes is None:
            return None

        if target.quoted_target is None:
            return None

        quote_tweet_id = target.quoted_target

        for tweet in self.includes.tweets:
            if quote_tweet_id == tweet.id:
                return tweet

        return None

    def find_replied_tweet_by(self, reply_tweet: TweetId | Tweet) -> Optional[Tweet]:
        """
        返信元のツイートを検索する。
        """

        target = self.find_tweet_by(reply_tweet)

        if target is None or self.includes is None:
            return None

        if target.replied_target is None:
            return None

        reply_tweet_id = target.replied_target

        for tweet in self.includes.tweets:
            if reply_tweet_id == tweet.id:
                return tweet

        return None

    def find_mentioned_users_by(self, tweet: TweetId | Tweet) -> list[User]:
        """
        メンションしているユーザのリストを検索する。
        """

        target = self.find_tweet_by(tweet)

        if target is None or self.includes is None:
            return []

        users: list[User] = []

        for user in self.includes.users:
            for mentioned in target.entities_mentions:
                if mentioned.username == user.username:
                    users.append(user)

        return users


class TweetsResponseBodyMeta(ExtraPermissiveModel):
    result_count: int
    next_token: Optional[str] = None
    previous_token: Optional[str] = None
    newest_id: Optional[TweetId] = None
    oldest_id: Optional[TweetId] = None


class TweetsSearchResponseBody(TweetsResponseBody):
    meta: TweetsResponseBodyMeta
