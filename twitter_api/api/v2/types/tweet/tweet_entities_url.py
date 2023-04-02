from typing import Optional

from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.http import Url


class TweetEntitiesUrl(ExtraPermissiveModel):
    start: Optional[int] = None
    end: Optional[int] = None
    url: Optional[Url] = None
    expanded_url: Optional[Url] = None
    display_url: Optional[Url] = None
    status: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    unwound_url: Optional[Url] = None
