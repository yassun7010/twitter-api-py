from typing_extensions import Literal

from .delete_v2_tweet import V2DeleteTweetResources
from .get_v2_tweet import V2GetTweetResources

V2TweetUrl = Literal["https://api.twitter.com/2/tweets/:id"]


class V2TweetResources(V2GetTweetResources, V2DeleteTweetResources):
    pass
