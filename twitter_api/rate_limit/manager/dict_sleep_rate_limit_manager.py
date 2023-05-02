from twitter_api.rate_limit.manager.dict_rate_limit_manager import DictRateLimitManager
from twitter_api.rate_limit.manager.handlers.sleep_rate_limit_handler import (
    DEFAULT_MAX_RANDOM_SLEEP_SECONDS,
    DEFAULT_MIN_RANDOM_SLEEP_SECONDS,
    SleepRateLimitHandler,
)


class DictSleepRateLimitManager(DictRateLimitManager, SleepRateLimitHandler):
    """
    単純なハッシュマップによるレートリミットの管理を行うマネージャ。

    レートリミットオーバーになったとき、スリープする。
    """

    def __init__(
        self,
        min_random_sleep_seconds: int = DEFAULT_MIN_RANDOM_SLEEP_SECONDS,
        max_random_sleep_seconds: int = DEFAULT_MAX_RANDOM_SLEEP_SECONDS,
    ):
        SleepRateLimitHandler.__init__(
            self,
            min_random_sleep_seconds=min_random_sleep_seconds,
            max_random_sleep_seconds=max_random_sleep_seconds,
        )
        DictRateLimitManager.__init__(self)
