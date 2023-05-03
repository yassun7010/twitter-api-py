from twitter_api.types.v2_tweet.tweet_id import TweetId

from ._specific_keyword import SpecificKeyword
from .operator import Operator


class RetweetsOfTweetId(SpecificKeyword, Operator[Operator]):
    def __init__(self, id: TweetId):
        super().__init__(id, "retweets_of_tweet_id:")
