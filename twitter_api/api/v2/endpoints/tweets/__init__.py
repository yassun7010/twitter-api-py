from typing_extensions import Literal

from .get_tweet import V2GetTweet
from .get_tweets import V2GetTweets
from .post_tweet import V2PostTweet

TweetsUri = Literal["/2/tweets"]
TweetUri = Literal["/2/tweets/:id"]


class V2Tweets(V2GetTweets, V2PostTweet):
    pass


class V2Tweet(V2GetTweet):
    pass
