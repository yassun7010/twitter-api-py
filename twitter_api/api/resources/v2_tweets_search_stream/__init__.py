from typing import TypeAlias

from typing_extensions import Literal

from .get_v2_tweets_search_stream import GetV2TweetsSearchStreamResources

V2TweetsSearchStreamUrl: TypeAlias = Literal[
    "https://api.twitter.com/2/tweets/search/stream"
]


class TweetRetweetedByRerources(GetV2TweetsSearchStreamResources):
    pass
