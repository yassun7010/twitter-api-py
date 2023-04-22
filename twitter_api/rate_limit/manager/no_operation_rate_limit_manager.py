from datetime import datetime
from typing import Optional

from twitter_api.rate_limit.manager.rate_limit_manager import RateLimitManager
from twitter_api.rate_limit.rate_limit_info import RateLimitInfo


class NoOperationRateLimitManager(RateLimitManager):
    """
    レートリミットに関して、クライアント側で何も制御しないマネージャ。

    Twitter API がレートリミットエラーを返却ことを想定している。
    """

    def check_limit_over(
        self,
        rate_limit_info: RateLimitInfo,
        now: Optional[datetime] = None,
    ) -> Optional[float]:
        return None
