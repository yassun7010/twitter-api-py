from dataclasses import dataclass
from typing import Literal

EndpointMethod = Literal["GET", "POST"]
EndpointURI = str


@dataclass
class Endpoint:
    method: EndpointMethod
    uri: EndpointURI
