from datetime import datetime
from typing import Optional

from twitter_api.rate_limit.manager.rate_limit_manager import RateLimitManager
from twitter_api.rate_limit.rate_limit_data import RateLimitData


class IgnoredRateLimitManager(RateLimitManager):
    """
    レートリミットに関して、クライアント側で何も制御しないマネージャ。

    Twitter API が出すレートリミットエラーで対応することを想定している。
    """

    def check_limit_over(
        self,
        rate_limit_data: RateLimitData,
        now: Optional[datetime] = None,
    ) -> bool:
        return False
