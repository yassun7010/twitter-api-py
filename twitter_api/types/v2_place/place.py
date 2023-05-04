from typing import Any, Optional

from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.v2_geo.geo import Geo

from .place_full_name import PlaceFullName
from .place_id import PlaceId


class Place(ExtraPermissiveModel):
    """
    場所情報。

    refer: https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/place
    """

    id: PlaceId
    full_name: PlaceFullName
    name: Optional[str] = None
    contained_within: Optional[list[Any]] = None
    country: Optional[str] = None
    country_code: Optional[str] = None
    geo: Optional[Geo] = None
    place_type: Optional[str] = None
