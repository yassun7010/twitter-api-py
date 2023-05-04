from typing import Literal, Optional, overload

from .operator import InvertableOperator, Operator, StandaloneOperator


class PointRadiusOperator(
    InvertableOperator[Operator],
    StandaloneOperator[Operator],
):
    @overload
    def __init__(
        self,
        *,
        longitude: float,
        latitude: float,
        radius_km: int,
        radius_mi: Literal[None] = None,
    ):
        ...

    @overload
    def __init__(
        self,
        *,
        longitude: float,
        latitude: float,
        radius_km: Literal[None] = None,
        radius_mi: int,
    ):
        ...

    def __init__(
        self,
        *,
        longitude: float,
        latitude: float,
        radius_km: Optional[int] = None,
        radius_mi: Optional[int] = None,
    ):
        self.longitude = longitude
        self.latitude = latitude
        if radius_km is not None:
            self.radius = radius_km
            self.radius_unit = "km"
        elif radius_mi is not None:
            self.radius = radius_mi
            self.radius_unit = "mi"
        else:
            self.radius = 1
            self.radius_unit = "km"

    def __str__(self) -> str:
        return f"point_radius:[{self.longitude} {self.latitude} {self.radius}{self.radius_unit}]"
