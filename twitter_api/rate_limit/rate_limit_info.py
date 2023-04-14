from dataclasses import dataclass

from twitter_api.rate_limit.rate_limit_target import RateLimitTarget
from twitter_api.types.endpoint import Endpoint


@dataclass(frozen=True)
class RateLimitInfo:
    target: RateLimitTarget
    endpoint: Endpoint
    requests: int
    total_seconds: int
