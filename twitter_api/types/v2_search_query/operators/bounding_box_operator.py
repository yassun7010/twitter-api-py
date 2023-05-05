from .operator import InvertibleOperator, StandaloneOperator


class BoundingBoxOperator(
    InvertibleOperator,
    StandaloneOperator,
):
    def __init__(
        self,
        west_longitude: float,
        south_latitude: float,
        east_longitude: float,
        north_latitude: float,
    ):
        self.west_longitude = west_longitude
        self.south_latitude = south_latitude
        self.east_longitude = east_longitude
        self.north_latitude = north_latitude

    def __str__(self) -> str:
        return f"bounding_box:[{self.west_longitude} {self.south_latitude} {self.east_longitude} {self.north_latitude}]"
