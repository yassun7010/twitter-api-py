from typing import Union

from twitter_api.types.v2_place.place_id import PlaceId
from twitter_api.types.v2_place.place_name import PlaceName

from .operator import InvertableOperator, Operator, StandaloneOperator


class PlaceOperator(
    InvertableOperator[Operator],
    StandaloneOperator[Operator],
):
    def __init__(self, place: Union[PlaceId, PlaceName]):
        self._value = place

    def __str__(self) -> str:
        if " " in self._value:
            place = f'"{self._value}"'
        else:
            place = self._value

        return f"place:{place}"
