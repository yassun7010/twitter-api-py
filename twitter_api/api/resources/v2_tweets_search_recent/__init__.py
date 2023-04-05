from typing import TypeAlias

from typing_extensions import Literal

from .get_v2_tweets_search_recent import GetV2TweetsSearchRecentResources

V2TweetsSearchRecentUrl: TypeAlias = Literal[
    "https://api.twitter.com/2/tweets/search/recent"
]


class TweetRetweetedByRerources(GetV2TweetsSearchRecentResources):
    pass
