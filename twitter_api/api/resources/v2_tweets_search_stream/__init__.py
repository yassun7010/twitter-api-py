from typing import TypeAlias

from typing_extensions import Literal

from .get_v2_tweets_search_stream import (
    AsyncGetV2TweetsSearchStreamResources,
    GetV2TweetsSearchStreamResources,
)

V2TweetsSearchStreamUrl: TypeAlias = Literal[
    "https://api.twitter.com/2/tweets/search/stream"
]


class V2TweetsSearchStreamResources(GetV2TweetsSearchStreamResources):
    pass


class AsyncV2TweetsSearchStreamResources(AsyncGetV2TweetsSearchStreamResources):
    pass
