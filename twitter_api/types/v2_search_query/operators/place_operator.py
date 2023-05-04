from typing import Union

from twitter_api.types.v2_place.place_full_name import PlaceFullName
from twitter_api.types.v2_place.place_id import PlaceId

from .operator import Operator


class PlaceOperator(Operator[Operator]):
    def __init__(self, place: Union[PlaceId, PlaceFullName]):
        self._value = place

    def __str__(self) -> str:
        if " " in self._value:
            place = f'"{self._value}"'
        else:
            place = self._value

        return f"place:{place}"
