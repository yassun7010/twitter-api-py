from typing import Optional

from twitter_api.types.extra_permissive_model import ExtraPermissiveModel


class TweetEntitiesAnnotation(ExtraPermissiveModel):
    start: Optional[int] = None
    end: Optional[int] = None
    probability: Optional[float] = None
    type: Optional[str] = None
    normalized_text: Optional[str] = None
