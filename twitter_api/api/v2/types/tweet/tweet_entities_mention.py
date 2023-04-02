from typing import Optional

from twitter_api.api.v2.types.username import Username
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel


class TweetEntitiesMention(ExtraPermissiveModel):
    start: Optional[int] = None
    end: Optional[int] = None
    username: Optional[Username] = None
