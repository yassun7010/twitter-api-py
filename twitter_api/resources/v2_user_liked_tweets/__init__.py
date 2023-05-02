from typing import Literal

from .get_v2_user_liked_tweets import (
    AsyncGetV2UserLikedTweetsResources,
    GetV2UserLikedTweetsResources,
)

V2UserLikedTweetsUrl = Literal["https://api.twitter.com/2/users/:id/liked_tweets"]


class V2UserLikedTweetsResources(GetV2UserLikedTweetsResources):
    pass


class AsyncV2UserLikedTweetsResources(AsyncGetV2UserLikedTweetsResources):
    pass
