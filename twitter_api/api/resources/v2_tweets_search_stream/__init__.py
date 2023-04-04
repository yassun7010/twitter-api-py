from typing import TypeAlias

from typing_extensions import Literal

from .get_tweets_search_stream import V2GetTweetsSearchStreamResources

V2TweetsSearchStreamUrl: TypeAlias = Literal[
    "https://api.twitter.com/2/tweets/search/stream"
]


class TweetRetweetedByRerources(V2GetTweetsSearchStreamResources):
    pass
