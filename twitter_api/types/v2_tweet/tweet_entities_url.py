from typing import Optional

from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.http import Url


class TweetEntitiesUrl(ExtraPermissiveModel):
    start: int
    end: int
    url: Url
    expanded_url: Url
    display_url: Url
    status: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    unwound_url: Optional[Url] = None
