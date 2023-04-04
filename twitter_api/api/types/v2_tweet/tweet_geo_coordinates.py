from typing import Optional

from twitter_api.types.extra_permissive_model import ExtraPermissiveModel


class TweetGeoCoordinates(ExtraPermissiveModel):
    type: Optional[str] = None
    coordinates: Optional[list[float]] = None
