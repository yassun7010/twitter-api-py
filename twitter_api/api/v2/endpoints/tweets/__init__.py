from typing_extensions import Literal

from .delete_tweet import V2DeleteTweet
from .get_tweet import V2GetTweet
from .get_tweets import V2GetTweets
from .post_tweet import V2PostTweet

TweetsUri = Literal["https://api.twitter.com/2/tweets"]
TweetUri = Literal["https://api.twitter.com/2/tweets/:id"]


class V2Tweets(V2GetTweets, V2PostTweet):
    pass


class V2Tweet(V2GetTweet, V2DeleteTweet):
    pass
