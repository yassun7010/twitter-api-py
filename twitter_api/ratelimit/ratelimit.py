from attr import dataclass

from twitter_api.ratelimit.ratelimit_target import RatelimitTarget
from twitter_api.types.endpoint import Endpoint


@dataclass
class Ratelimit:
    target: RatelimitTarget
    endpoint: Endpoint
    requests: int
    seconds: int
