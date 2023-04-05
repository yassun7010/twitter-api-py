from typing import TypeAlias

from typing_extensions import Literal

from .get_v2_tweets_search_all import GetV2TweetsSearchAllResources

V2TweetsSearchAllUrl: TypeAlias = Literal["https://api.twitter.com/2/tweets/search/all"]


class V2TweetsSearchAllResources(GetV2TweetsSearchAllResources):
    pass
