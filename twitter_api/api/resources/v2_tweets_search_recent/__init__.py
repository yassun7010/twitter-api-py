from typing import TypeAlias

from typing_extensions import Literal

from .get_tweets_search_recent import V2GetTweetsSearchRecentResources

V2TweetsSearchRecentUrl: TypeAlias = Literal[
    "https://api.twitter.com/2/tweets/search/recent"
]


class TweetRetweetedByRerources(V2GetTweetsSearchRecentResources):
    pass
