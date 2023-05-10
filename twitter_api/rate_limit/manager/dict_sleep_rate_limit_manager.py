from random import randint

from twitter_api.rate_limit.manager.rate_limit_manager import RateLimitManager

from .checkers.dict_rate_limit_checker import DictRateLimitChecker
from .mixins.sleep_rate_limit_manager_mixin import (
    DEFAULT_MAX_RANDOM_SLEEP_SECONDS,
    DEFAULT_MIN_RANDOM_SLEEP_SECONDS,
    SleepRateLimitManagerMixin,
)


class DictSleepRateLimitManager(
    DictRateLimitChecker, SleepRateLimitManagerMixin, RateLimitManager
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
        self._min_random_sleep_seconds = min_random_sleep_seconds
        self._max_random_sleep_seconds = max_random_sleep_seconds
        super().__init__()

    def random_sleep_seconds(self) -> int:
        return randint(self._min_random_sleep_seconds, self._max_random_sleep_seconds)
