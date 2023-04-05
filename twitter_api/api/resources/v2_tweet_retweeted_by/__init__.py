from typing import TypeAlias

from typing_extensions import Literal

from .get_v2_tweet_retweeted_by import GetV2TweetRetweetedByResources

V2TweetRetweetedByUrl: TypeAlias = Literal[
    "https://api.twitter.com/2/tweets/:id/retweeted_by"
]


class V2TweetRetweetedByRerources(GetV2TweetRetweetedByResources):
    pass
