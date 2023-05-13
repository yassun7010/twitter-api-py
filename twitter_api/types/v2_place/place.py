from typing import Any, Optional, Union

from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.v2_geo.geo import Geo
from twitter_api.types.v2_place.place_country_code import PlaceCountryCode
from twitter_api.types.v2_place.place_name import PlaceName

from .place_full_name import PlaceFullName
from .place_id import PlaceId


class Place(ExtraPermissiveModel):
    """
    場所情報。

    refer: https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/place
    """

    id: PlaceId
    name: PlaceName
    full_name: PlaceFullName
    contained_within: Optional[list[Any]] = None
    country: Optional[str] = None
    # NOTE: 公式ではない国のコードを返す可能性があるため、 str も受け入れておく。
    country_code: Optional[Union[PlaceCountryCode, str]] = None
    geo: Optional[Geo] = None
    place_type: Optional[str] = None
