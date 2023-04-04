from twitter_api.api.types.v2_tweet.tweet import Tweet
from twitter_api.api.types.v2_tweet.tweet_id import TweetId


class TweetDetail(Tweet):
    """
    詳細な情報を持ったツイート。

    現状、edit_history_tweet_ids が必須となっている API の箇所で用いる。
    """

    edit_history_tweet_ids: list[TweetId]
