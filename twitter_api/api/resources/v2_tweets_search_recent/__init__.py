from typing import TypeAlias

from typing_extensions import Literal

from .get_v2_tweets_search_recent import (
    AsyncGetV2TweetsSearchRecentResources,
    GetV2TweetsSearchRecentResources,
)

V2TweetsSearchRecentUrl: TypeAlias = Literal[
    "https://api.twitter.com/2/tweets/search/recent"
]


class V2TweetsSearchRecentResources(GetV2TweetsSearchRecentResources):
    pass


class AsyncV2TweetsSearchRecentResources(AsyncGetV2TweetsSearchRecentResources):
    pass
