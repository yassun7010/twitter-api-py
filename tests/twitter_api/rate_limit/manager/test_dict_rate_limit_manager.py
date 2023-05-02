from datetime import datetime, timedelta

import pytest

from twitter_api.rate_limit.manager.dict_rate_limit_manager import (
    DictRateLimitManager,
    RateLimitStatus,
)
from twitter_api.rate_limit.rate_limit_info import RateLimitInfo
from twitter_api.types.endpoint import Endpoint

TOTAL_REQUESTS = 10


@pytest.fixture
def rate_limit_info() -> RateLimitInfo:
    return RateLimitInfo(
        target="app",
        endpoint=Endpoint("GET", "https://api.twitter.com/2/tweets"),
        requests=TOTAL_REQUESTS,
        total_seconds=1000,
    )


class TestDictRateLimitManager:
    @pytest.mark.parametrize(
        "requests,result",
        [(i, False) for i in range(1, TOTAL_REQUESTS)] + [(TOTAL_REQUESTS, True)],
    )
    def test_check_limit_over(
        self,
        rate_limit_info: RateLimitInfo,
        requests,
        result,
    ):
        # テスト用のデータを作成する。
        # ストアに入れる値は、窓の中に納まる範囲にしておく。
        start_datetime = datetime(2020, 1, 1, 0, 0, 0)
        request_datetimes = [
            start_datetime + timedelta(seconds=i) for i in range(requests)
        ]

        manager = DictRateLimitManager()
        manager._store[rate_limit_info] = RateLimitStatus(
            start_datetime=start_datetime,
            request_datetimes=request_datetimes,
        )

        # 窓の中身が消えるようなデータを入れていないので、
        # 単純に窓の上限を超えるデータを入れるとレートリミットになる。
        assert (
            manager.check_limit_over(
                rate_limit_info=rate_limit_info,
                now=start_datetime + timedelta(seconds=len(request_datetimes)),
            )
            is not None
        ) is result
