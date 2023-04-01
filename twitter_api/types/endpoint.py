from dataclasses import dataclass
from typing import Literal, TypeAlias

EndpointMethod = Literal["GET", "POST"]
EndpointURI: TypeAlias = str


@dataclass
class Endpoint:
    method: EndpointMethod
    uri: EndpointURI
