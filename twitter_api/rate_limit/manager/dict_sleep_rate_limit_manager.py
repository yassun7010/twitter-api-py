from twitter_api.rate_limit.manager.rate_limit_manager import RateLimitManager

from .checkers.dict_rate_limit_checker import DictRateLimitChecker
from .handlers.sleep_rate_limit_handler import (
    DEFAULT_MAX_RANDOM_SLEEP_SECONDS,
    DEFAULT_MIN_RANDOM_SLEEP_SECONDS,
    SleepRateLimitHandler,
)


class DictSleepRateLimitManager(
    DictRateLimitChecker, SleepRateLimitHandler, RateLimitManager
):
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
        DictRateLimitChecker.__init__(self)
