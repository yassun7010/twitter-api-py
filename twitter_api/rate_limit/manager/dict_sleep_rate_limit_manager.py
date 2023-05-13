from typing_extensions import override

from twitter_api.rate_limit.manager.mixins.dict_rate_limit_checker_mixin import (
    DictRateLimitCheckerMixin,
)
from twitter_api.rate_limit.manager.rate_limit_manager import RateLimitManager

from .mixins.sleep_rate_limit_handler_mixin import (
    DEFAULT_MAX_RANDOM_SLEEP_SECONDS,
    DEFAULT_MIN_RANDOM_SLEEP_SECONDS,
    SleepRateLimitHandlerMixin,
)


class DictSleepRateLimitManager(
    DictRateLimitCheckerMixin, SleepRateLimitHandlerMixin, RateLimitManager
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

    @property
    @override
    def min_random_sleep_seconds(self) -> int:
        return self._min_random_sleep_seconds

    @property
    @override
    def max_random_sleep_seconds(self) -> int:
        return self._max_random_sleep_seconds
