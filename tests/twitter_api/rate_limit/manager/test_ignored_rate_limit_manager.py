import pytest

from twitter_api.rate_limit.manager.ignored_rate_limit_manager import (
    IgnoredRateLimitManager,
)
from twitter_api.rate_limit.rate_limit_data import RateLimitData
from twitter_api.types.endpoint import Endpoint


@pytest.fixture
def rate_limit_data() -> RateLimitData:
    return RateLimitData(
        target="app",
        endpoint=Endpoint("GET", "https://api.twitter.com/2/tweets"),
        requests=10,
        total_seconds=1000,
    )


class TestIgnoredRateLimitManager:
    def test_check_limit_over(
        self,
        rate_limit_data: RateLimitData,
    ):
        assert (
            IgnoredRateLimitManager().check_limit_over(
                rate_limit_data=rate_limit_data,
            )
            is False
        )
