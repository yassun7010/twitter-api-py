from typing import Optional

from twitter_api.types.extra_permissive_model import ExtraPermissiveModel


class TweetEntitiesCashtag(ExtraPermissiveModel):
    start: Optional[int] = None
    end: Optional[int] = None
    tag: Optional[str] = None
