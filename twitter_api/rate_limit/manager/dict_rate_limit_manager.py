from typing_extensions import override

from twitter_api.rate_limit.manager.mixins.dict_rate_limit_checker_mixin import (
    DictRateLimitCheckerMixin,
    RateLimitStatus,
)
from twitter_api.rate_limit.manager.mixins.raise_rate_limit_handler_mixin import (
    RaiseRateLimitHandlerMixin,
)
from twitter_api.rate_limit.manager.rate_limit_manager import RateLimitManager
from twitter_api.rate_limit.rate_limit_info import RateLimitInfo


class DictRateLimitManager(
    DictRateLimitCheckerMixin, RaiseRateLimitHandlerMixin, RateLimitManager
):
    """
    単純なハッシュマップによるレートリミットの管理を行うマネージャ。

    Redis, RDS などで管理したい場合は、
    このクラスを参考に RateLimitManager を実装すればよい。
    """

    def __init__(self) -> None:
        self._store = {}
        super().__init__()

    @property
    @override
    def store(self) -> dict[RateLimitInfo, RateLimitStatus]:
        return self._store
