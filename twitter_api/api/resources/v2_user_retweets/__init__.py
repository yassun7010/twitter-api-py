from typing import Literal

from .post_user_retweets import V2PostUserRetweetsResources

UserRetweetsUrl = Literal["https://api.twitter.com/2/users/:id/retweets"]


class V2UserRetweetsResources(V2PostUserRetweetsResources):
    pass
