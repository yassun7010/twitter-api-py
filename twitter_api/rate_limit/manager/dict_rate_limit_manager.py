from twitter_api.rate_limit.manager.mixins.dict_rate_limit_checker_mixin import (
    DictRateLimitCheckerMixin,
)
from twitter_api.rate_limit.manager.mixins.raise_rate_limit_handler_mixin import (
    RaiseRateLimitHandlerMixin,
)
from twitter_api.rate_limit.manager.rate_limit_manager import RateLimitManager


class DictRateLimitManager(
    DictRateLimitCheckerMixin, RaiseRateLimitHandlerMixin, RateLimitManager
):
    """
    単純なハッシュマップによるレートリミットの管理を行うマネージャ。

    Redis, RDS などで管理したい場合は、
    このクラスを参考に RateLimitManager を実装すればよい。
    """

    pass
