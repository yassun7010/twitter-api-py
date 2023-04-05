from typing import Literal

from .post_v2_user_retweets import PostV2UserRetweetsResources

V2UserRetweetsUrl = Literal["https://api.twitter.com/2/users/:id/retweets"]


class V2UserRetweetsResources(PostV2UserRetweetsResources):
    pass
