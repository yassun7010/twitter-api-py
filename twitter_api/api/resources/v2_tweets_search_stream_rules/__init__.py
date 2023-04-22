from typing import TypeAlias

from typing_extensions import Literal

from .get_v2_tweets_search_stream_rules import (
    AsyncGetV2TweetsSearchStreamRulesResources,
    GetV2TweetsSearchStreamRulesResources,
)
from .post_v2_tweets_search_stream_rules import (
    AsyncPostV2TweetsSearchStreamRulesResources,
    PostV2TweetsSearchStreamRulesResources,
)

V2TweetsSearchStreamRulesUrl: TypeAlias = Literal[
    "https://api.twitter.com/2/tweets/search/stream/rules"
]


class V2TweetsSearchStreamRulesResources(
    GetV2TweetsSearchStreamRulesResources,
    PostV2TweetsSearchStreamRulesResources,
):
    pass


class AsyncV2TweetsSearchStreamRulesResources(
    AsyncGetV2TweetsSearchStreamRulesResources,
    AsyncPostV2TweetsSearchStreamRulesResources,
):
    pass
