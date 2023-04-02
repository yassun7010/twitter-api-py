from datetime import datetime
from typing import Optional

from twitter_api.ratelimit.manager.ratelimit_manager import RatelimitManager
from twitter_api.ratelimit.ratelimit_data import RatelimitData


class IgnoredRatelimitManager(RatelimitManager):
    """
    レートリミットに関して、クライアント側で何も制御しないマネージャ。

    Twitter API が出すレートリミットエラーで対応することを想定している。
    """

    def check_limit_over(
        self,
        ratelimit: RatelimitData,
        now: Optional[datetime] = None,
    ) -> bool:
        return False
