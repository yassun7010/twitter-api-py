from twitter_api.types.v2_tweet.tweet_id import TweetId

from .operator import InvertibleOperator, StandaloneOperator


class InReplyToTweetIdOperator(
    InvertibleOperator,
    StandaloneOperator,
):
    def __init__(self, id: TweetId):
        self._value = id

    def __str__(self) -> str:
        return f"in_reply_to_tweet_id:{self._value}"
