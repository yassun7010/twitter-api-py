from twitter_api.types.v2_place.place_country_code import PlaceCountryCode

from .operator import InvertibleOperator, Operator, StandaloneOperator


class PlaceCountryOperator(
    InvertibleOperator[Operator],
    StandaloneOperator[Operator],
):
    def __init__(self, code: PlaceCountryCode):
        self._value = code

    def __str__(self) -> str:
        return f"place_country:{self._value}"
