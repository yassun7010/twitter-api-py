from typing import Literal

from .get_v2_user_tweets import AsyncGetV2UserTweetsResources, GetV2UserTweetsResources

V2UserTweetsUrl = Literal["https://api.twitter.com/2/users/:id/tweets"]


class V2UserTweetsResources(GetV2UserTweetsResources):
    pass


class AsyncV2UserTweetsResources(AsyncGetV2UserTweetsResources):
    pass
