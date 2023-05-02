from typing import Literal

from twitter_api.types.extra_permissive_model import ExtraPermissiveModel


class Geo(ExtraPermissiveModel):
    type: Literal["Feature"]
    bbox: list[float]
    properties: dict
