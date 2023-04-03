from typing import Literal

from .get_user_tweets import V2GetUserTweetsResources

UserTweetsUrl = Literal["https://api.twitter.com/2/users/:id/tweets"]


class V2UserTweetsResources(V2GetUserTweetsResources):
    pass
