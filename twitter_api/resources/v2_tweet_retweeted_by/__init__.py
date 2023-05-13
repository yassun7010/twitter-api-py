from typing_extensions import Literal, TypeAlias

from .get_v2_tweet_retweeted_by import (
    AsyncGetV2TweetRetweetedByResources,
    GetV2TweetRetweetedByResources,
)

V2TweetRetweetedByUrl: TypeAlias = Literal[
    "https://api.twitter.com/2/tweets/:id/retweeted_by"
]


class V2TweetRetweetedByRerources(GetV2TweetRetweetedByResources):
    pass


class AsyncV2TweetRetweetedByRerources(AsyncGetV2TweetRetweetedByResources):
    pass
