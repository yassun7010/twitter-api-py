from typing_extensions import Literal

from .delete_v2_tweet import AsyncDeleteV2TweetResources, DeleteV2TweetResources
from .get_v2_tweet import AsyncGetV2TweetResources, GetV2TweetResources

V2TweetUrl = Literal["https://api.twitter.com/2/tweets/:id"]


class V2TweetResources(GetV2TweetResources, DeleteV2TweetResources):
    pass


class AsyncV2TweetResources(AsyncGetV2TweetResources, AsyncDeleteV2TweetResources):
    pass
