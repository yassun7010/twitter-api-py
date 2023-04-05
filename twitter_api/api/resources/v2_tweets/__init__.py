from typing_extensions import Literal

from .get_v2_tweets import V2GetTweetsResources
from .post_v2_tweets import V2PostTweetsResources

V2TweetsUrl = Literal["https://api.twitter.com/2/tweets"]


class V2TweetsResources(V2GetTweetsResources, V2PostTweetsResources):
    pass
