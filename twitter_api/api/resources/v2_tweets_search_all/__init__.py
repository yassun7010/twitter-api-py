from typing import TypeAlias

from typing_extensions import Literal

from .get_tweets_search_all import V2GetTweetsSearchAllResources

V2TweetsSearchAllUrl: TypeAlias = Literal["https://api.twitter.com/2/tweets/search/all"]


class V2TweetsSearchAllResources(V2GetTweetsSearchAllResources):
    pass
