from attr import dataclass

from twitter_api.rate_limit.rate_limit_target import RateLimitTarget
from twitter_api.types.endpoint import Endpoint


@dataclass(frozen=True)
class RateLimitData:
    target: RateLimitTarget
    endpoint: Endpoint
    requests: int
    total_seconds: int
