from twitter_api.rate_limit.manager.dict_rate_limit_manager import DictRateLimitManager
from twitter_api.rate_limit.manager.handlers.sleep_rate_limit_handler import (
    SleepRateLimitHandler,
)


class DictSleepRateLimitManager(DictRateLimitManager, SleepRateLimitHandler):
    """
    単純なハッシュマップによるレートリミットの管理を行うマネージャ。

    レートリミットオーバーになったとき、スリープする。
    """

    def __init__(
        self,
        min_random_sleep_seconds: int = 5 * 60,
        max_random_sleep_seconds: int = 15 * 60,
    ):
        SleepRateLimitHandler.__init__(
            self,
            min_random_sleep_seconds=min_random_sleep_seconds,
            max_random_sleep_seconds=max_random_sleep_seconds,
        )
        DictRateLimitManager.__init__(self)
