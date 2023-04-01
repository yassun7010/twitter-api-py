from typing import Optional

from twitter_api.types.extra_permissive_model import ExtraPermissiveModel


class TweetEntitiesUrl(ExtraPermissiveModel):
    start: Optional[int] = None
    end: Optional[int] = None
    url: Optional[str] = None
    expanded_url: Optional[str] = None
    display_url: Optional[str] = None
    status: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    unwound_url: Optional[str] = None
