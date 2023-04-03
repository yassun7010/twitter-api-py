from typing_extensions import Literal

from .delete_tweet import V2DeleteTweetResources
from .get_tweet import V2GetTweetResources
from .get_tweets import V2GetTweetsResources
from .post_tweet import V2PostTweetResources

TweetsUrl = Literal["https://api.twitter.com/2/tweets"]
TweetUrl = Literal["https://api.twitter.com/2/tweets/:id"]


class V2Tweets(V2GetTweetsResources, V2PostTweetResources):
    pass


class V2Tweet(V2GetTweetResources, V2DeleteTweetResources):
    pass
