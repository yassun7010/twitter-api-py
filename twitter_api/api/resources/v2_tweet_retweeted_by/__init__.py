from typing import TypeAlias

from typing_extensions import Literal

from .get_tweet_retweeted_by import V2GetTweetRetweetedByResources

V2TweetRetweetedByUrl: TypeAlias = Literal[
    "https://api.twitter.com/2/tweets/:id/retweeted_by"
]


class V2TweetRetweetedByRerources(V2GetTweetRetweetedByResources):
    pass
