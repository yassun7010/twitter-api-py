from typing import Optional

from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.v2_user.username import Username


class TweetEntitiesMention(ExtraPermissiveModel):
    start: Optional[int] = None
    end: Optional[int] = None
    username: Optional[Username] = None
