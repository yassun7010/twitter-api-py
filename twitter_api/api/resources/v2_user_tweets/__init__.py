from typing import Literal

from .get_v2_user_tweets import V2GetUserTweetsResources

V2UserTweetsUrl = Literal["https://api.twitter.com/2/users/:id/tweets"]


class V2UserTweetsResources(V2GetUserTweetsResources):
    pass
