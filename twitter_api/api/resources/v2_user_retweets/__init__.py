from typing import Literal

from .post_v2_user_retweets import (
    AsyncPostV2UserRetweetsResources,
    PostV2UserRetweetsResources,
)

V2UserRetweetsUrl = Literal["https://api.twitter.com/2/users/:id/retweets"]


class V2UserRetweetsResources(PostV2UserRetweetsResources):
    pass


class AsyncV2UserRetweetsResources(AsyncPostV2UserRetweetsResources):
    pass
