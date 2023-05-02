import pytest

from twitter_api.rate_limit.manager.handlers.sleep_rate_limit_handler import (
    SleepRateLimitHandler,
)
from twitter_api.rate_limit.manager.no_operation_rate_limit_manager import (
    NoOperationRateLimitManager,
)
from twitter_api.rate_limit.rate_limit_info import RateLimitInfo
from twitter_api.types.endpoint import Endpoint


class NoOperationSleepRateLimitHandler(
    NoOperationRateLimitManager, SleepRateLimitHandler
):
    def random_sleep_seconds(self) -> float:
        """
        テストのため、常に待機しないようにする
        """
        return 0


@pytest.fixture
def rate_limit_info() -> RateLimitInfo:
    return RateLimitInfo(
        target="app",
        endpoint=Endpoint("GET", "https://api.twitter.com/2/tweets"),
        requests=10,
        total_seconds=1000,
    )


class TestSleepRateLimitHandler:
    def test_check_limit_over(
        self,
        rate_limit_info: RateLimitInfo,
    ):
        assert (
            NoOperationSleepRateLimitHandler().check_limit_over(
                rate_limit_info=rate_limit_info,
            )
            is None
        )
