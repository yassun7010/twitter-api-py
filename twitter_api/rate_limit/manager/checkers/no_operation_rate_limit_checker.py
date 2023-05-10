from datetime import datetime
from typing import Optional

from twitter_api.rate_limit.manager.checkers.rate_limit_checker import RateLimitChecker
from twitter_api.rate_limit.rate_limit_info import RateLimitInfo


class NoOperationRateLimitChecker(RateLimitChecker):
    """
    レートリミットに関して、クライアント側で何も確認しない。

    Twitter API が返すレートリミットエラーをそのまま例外として投げることを想定している。
    """

    def check_limit_over(
        self,
        rate_limit_info: RateLimitInfo,
        now: Optional[datetime] = None,
    ) -> Optional[float]:
        return None
