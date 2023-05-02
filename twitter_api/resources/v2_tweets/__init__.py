from typing_extensions import Literal

from .get_v2_tweets import AsyncGetV2TweetsResources, GetV2TweetsResources
from .post_v2_tweets import AsyncPostV2TweetsResources, PostV2TweetsResources

V2TweetsUrl = Literal["https://api.twitter.com/2/tweets"]


class V2TweetsResources(GetV2TweetsResources, PostV2TweetsResources):
    pass


class AsyncV2TweetsResources(AsyncGetV2TweetsResources, AsyncPostV2TweetsResources):
    pass
