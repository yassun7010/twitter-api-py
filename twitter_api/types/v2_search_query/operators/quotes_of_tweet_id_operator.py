from twitter_api.types.v2_tweet.tweet_id import TweetId

from .operator import Operator


class QuotesOfTweetIdOperator(Operator[Operator]):
    def __init__(self, id: TweetId) -> None:
        self._value = id

    def __str__(self) -> str:
        return f"quotes_of_tweet_id:{self._value}"