from .operator import InvertibleOperator, StandaloneOperator


class BoundingBoxOperator(
    InvertibleOperator,
    StandaloneOperator,
):
    def __init__(
        self,
        west_longitude_deg: float,
        south_latitude_deg: float,
        east_longitude_deg: float,
        north_latitude_deg: float,
    ):
        self.west_longitude_deg = west_longitude_deg
        self.south_latitude_deg = south_latitude_deg
        self.east_longitude_deg = east_longitude_deg
        self.north_latitude_deg = north_latitude_deg

    def __str__(self) -> str:
        return f"bounding_box:[{self.west_longitude_deg} {self.south_latitude_deg} {self.east_longitude_deg} {self.north_latitude_deg}]"
