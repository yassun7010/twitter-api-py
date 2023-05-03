from abc import ABCMeta, abstractmethod
from typing import Optional, Self, Union

from pydantic import Field

from twitter_api.types._paging import PageResponseBody
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.pagination_token import PaginationToken
from twitter_api.types.v2_media.media import Media
from twitter_api.types.v2_place.place import Place
from twitter_api.types.v2_poll.poll import Poll
from twitter_api.types.v2_tweet.tweet import Tweet
from twitter_api.types.v2_tweet.tweet_id import TweetId
from twitter_api.types.v2_user.user import User


class TweetsResponseBodyIncludes(ExtraPermissiveModel):
    users: list[User] = Field(default_factory=list)
    tweets: list[Tweet] = Field(default_factory=list)
    places: list[Place] = Field(default_factory=list)
    media: list[Media] = Field(default_factory=list)
    polls: list[Poll] = Field(default_factory=list)

    def extend(self, other: Self) -> None:
        self.users.extend(other.users)
        self.tweets.extend(other.tweets)
        self.places.extend(other.places)
        self.media.extend(other.media)
        self.polls.extend(other.polls)


class FindTweets(ExtraPermissiveModel, metaclass=ABCMeta):
    includes: TweetsResponseBodyIncludes = Field(
        default_factory=TweetsResponseBodyIncludes,
    )
    errors: Optional[list[dict]] = None

    @abstractmethod
    def find_tweet_by(self, id: Union[TweetId, Tweet]) -> Optional[Tweet]:
        """
        TweetId からツイートを検索する。

        Tweet を入力とした場合、入力した Tweet が Response の中にあるかを調べる。
        """
        ...

    def find_retweeted_tweet_by(
        self, retweet: Union[TweetId, Tweet]
    ) -> Optional[Tweet]:
        """
        リツイート元のツイートを検索する。
        """

        target = self.find_tweet_by(retweet)

        if target is None or self.includes is None:
            return None

        if target.retweeted_tweet_id is None:
            return None

        retweeted_id = target.retweeted_tweet_id

        for tweet in self.includes.tweets:
            if retweeted_id == tweet.id:
                return tweet

        return None

    def find_quoted_tweet_by(
        self, quote_tweet: Union[TweetId, Tweet]
    ) -> Optional[Tweet]:
        """
        引用元のツイートを検索する。
        """

        target = self.find_tweet_by(quote_tweet)

        if target is None or self.includes is None:
            return None

        if target.quoted_tweet_id is None:
            return None

        quote_tweet_id = target.quoted_tweet_id

        for tweet in self.includes.tweets:
            if quote_tweet_id == tweet.id:
                return tweet

        return None

    def find_replied_tweet_by(
        self, reply_tweet: Union[TweetId, Tweet]
    ) -> Optional[Tweet]:
        """
        返信元のツイートを検索する。
        """

        target = self.find_tweet_by(reply_tweet)

        if target is None or self.includes is None:
            return None

        if target.replied_tweet_id is None:
            return None

        reply_tweet_id = target.replied_tweet_id

        for tweet in self.includes.tweets:
            if reply_tweet_id == tweet.id:
                return tweet

        return None

    def find_mentioned_users_by(self, tweet: Union[TweetId, Tweet]) -> list[User]:
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


class TweetResponseBodyData(ExtraPermissiveModel):
    data: Tweet


class TweetResponseBody(FindTweets, TweetResponseBodyData):
    def find_tweet_by(self, id: Union[TweetId, Tweet]) -> Optional[Tweet]:
        if isinstance(id, Tweet):
            id = id.id

        if _check_self(id, self.data):
            return self.data

        if self.includes is None:
            return None

        for tweet in self.includes.tweets:
            if _check_self(id, tweet):
                return tweet

        return None


class _TweetsResponseBodyData(ExtraPermissiveModel):
    data: list[Tweet] = Field(default_factory=list)


class TweetsResponseBody(FindTweets, _TweetsResponseBodyData):
    def find_tweet_by(self, id: Union[TweetId, Tweet]) -> Optional[Tweet]:
        if isinstance(id, Tweet):
            id = id.id

        for tweet in self.data:
            if _check_self(id, tweet):
                return tweet

        if self.includes is None:
            return None

        for tweet in self.includes.tweets:
            if _check_self(id, tweet):
                return tweet

        return None


class TweetsResponseBodyMeta(ExtraPermissiveModel):
    result_count: int
    newest_id: Optional[TweetId] = None
    oldest_id: Optional[TweetId] = None
    next_token: Optional[PaginationToken] = None
    previous_token: Optional[PaginationToken] = None

    def extend(self, other: Self) -> None:
        self.result_count += other.result_count

        if self.newest_id is not None and other.newest_id is not None:
            if int(self.newest_id) < int(other.newest_id):
                self.newest_id = other.newest_id
        elif other.newest_id is not None:
            self.newest_id = other.newest_id

        if self.oldest_id is not None and other.oldest_id is not None:
            if int(self.oldest_id) < int(other.oldest_id):
                self.oldest_id = other.oldest_id
        elif other.oldest_id is not None:
            self.oldest_id = other.oldest_id

        self.next_token = None
        self.previous_token = None


class _TweetsSearchResponseBody(ExtraPermissiveModel):
    meta: TweetsResponseBodyMeta


class TweetsSearchResponseBody(
    TweetsResponseBody, _TweetsSearchResponseBody, PageResponseBody
):
    @property
    def meta_next_token(self) -> Optional[PaginationToken]:
        return self.meta.next_token

    def extend(self, other: Self) -> None:
        self.data.extend(other.data)
        self.includes.extend(other.includes)
        self.meta.extend(other.meta)

        if other.errors is not None:
            if self.errors is not None:
                self.errors.extend(other.errors)
            else:
                self.errors = other.errors


def _check_self(origin: TweetId, target: Tweet) -> bool:
    """
    同じツイートを指しているか。

    編集履歴を遡って判定する。
    """

    if target.id == origin:
        return True

    if target.edit_history_tweet_ids is not None:
        for target_id in target.edit_history_tweet_ids:
            if target_id == origin:
                return True
    return False
