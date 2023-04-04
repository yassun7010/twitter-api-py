from typing_extensions import Literal

from .get_tweets import V2GetTweetsResources
from .post_tweet import V2PostTweetResources

TweetsUrl = Literal["https://api.twitter.com/2/tweets"]


class V2TweetsResources(V2GetTweetsResources, V2PostTweetResources):
    pass
