from bisect import bisect_left
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

from twitter_api.rate_limit.manager.rate_limit_manager import RateLimitManager
from twitter_api.rate_limit.rate_limit_data import RateLimitData


@dataclass
class RateLimitStatus:
    start_datetime: datetime
    request_datetimes: list[datetime]


class DictRateLimitManager(RateLimitManager):
    def __init__(self) -> None:
        self._store: dict[RateLimitData, RateLimitStatus] = {}

    def check_limit_over(
        self,
        rate_limit_data: RateLimitData,
        now: Optional[datetime] = None,
    ) -> bool:
        if now is None:
            now = datetime.now()

        if rate_limit_data not in self._store:
            self._store[rate_limit_data] = RateLimitStatus(
                start_datetime=now, request_datetimes=[now]
            )

        # レートリミットの窓に今回のデータを入れる。
        status = self._store[rate_limit_data]
        status.request_datetimes.append(now)

        # 窓に入っている過去のデータのうち、考慮する必要のないデータを消す。
        min_datetime = now - timedelta(seconds=rate_limit_data.total_seconds)
        index = bisect_left(status.request_datetimes, min_datetime)
        del status.request_datetimes[:index]

        # 窓に入っているデータの数が、制限を超えていたらリミットオーバ
        return len(status.request_datetimes) > rate_limit_data.requests
