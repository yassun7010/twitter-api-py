from typing_extensions import Literal

from .delete_tweet import V2DeleteTweetResources
from .get_tweet import V2GetTweetResources

TweetUrl = Literal["https://api.twitter.com/2/tweets/:id"]


class V2TweetResources(V2GetTweetResources, V2DeleteTweetResources):
    pass
