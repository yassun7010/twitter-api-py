from twitter_api.types.v2_place.place_country_code import PlaceCountryCode

from .operator import InvertableOperator, Operator


class PlaceCountryOperator(InvertableOperator[Operator]):
    def __init__(self, code: PlaceCountryCode):
        self._value = code

    def __str__(self) -> str:
        return f"place_country:{self._value}"
