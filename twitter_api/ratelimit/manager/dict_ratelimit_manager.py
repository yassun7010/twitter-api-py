from bisect import bisect_left
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

from twitter_api.ratelimit.manager.ratelimit_manager import RatelimitManager
from twitter_api.ratelimit.ratelimit import Ratelimit


@dataclass
class RatelimitStatus:
    start_at: datetime
    requests: list[datetime]


class DictRatelimitManager(RatelimitManager):
    def __init__(self) -> None:
        self._store: dict[Ratelimit, RatelimitStatus] = {}

    def check_limit_over(
        self,
        ratelimit: Ratelimit,
        now: Optional[datetime] = None,
    ) -> bool:
        if now is None:
            now = datetime.now()

        if ratelimit not in self._store:
            self._store[ratelimit] = RatelimitStatus(start_at=now, requests=[now])

        # レートリミットの窓に今回のデータを入れる。
        status = self._store[ratelimit]
        status.requests.append(now)

        # 窓に入っている過去のデータのうち、考慮する必要のないデータを消す。
        min_datetime = now - timedelta(seconds=ratelimit.seconds)
        index = bisect_left(status.requests, min_datetime)
        del status.requests[:index]

        return len(status.requests) > ratelimit.requests
