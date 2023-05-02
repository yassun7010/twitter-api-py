from datetime import datetime
from typing import Optional

from twitter_api.rate_limit.manager.handlers.raise_rate_limit_handler import (
    RaiseRateLimitHandler,
)
from twitter_api.rate_limit.rate_limit_info import RateLimitInfo


class NoOperationRateLimitManager(RaiseRateLimitHandler):
    """
    レートリミットに関して、クライアント側で何も制御しないマネージャ。

    Twitter API が返すレートリミットエラーをそのまま例外として投げることを想定している。
    """

    def check_limit_over(
        self,
        rate_limit_info: RateLimitInfo,
        now: Optional[datetime] = None,
    ) -> Optional[float]:
        return None
