from typing import Optional

from twitter_api.types.extra_permissive_model import ExtraPermissiveModel

from .tweet_geo_coordinates import TweetGeoCoordinates


class TweetGeo(ExtraPermissiveModel):
    coordinates: Optional[TweetGeoCoordinates] = None
    place_id: Optional[str] = None
