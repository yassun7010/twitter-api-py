import pytest

from twitter_api.rate_limit.manager.no_operation_rate_limit_manager import (
    NoOperationRateLimitManager,
)
from twitter_api.rate_limit.rate_limit_info import RateLimitInfo
from twitter_api.types.endpoint import Endpoint


@pytest.fixture
def rate_limit_info() -> RateLimitInfo:
    return RateLimitInfo(
        target="app",
        endpoint=Endpoint("GET", "https://api.twitter.com/2/tweets"),
        requests=10,
        total_seconds=1000,
    )


class TestNoOperationRateLimitManager:
    def test_check_limit_over(
        self,
        rate_limit_info: RateLimitInfo,
    ):
        assert (
            NoOperationRateLimitManager().check_limit_over(
                rate_limit_info=rate_limit_info,
            )
            is False
        )
