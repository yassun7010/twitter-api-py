from twitter_api.rate_limit.manager.checkers.dict_rate_limit_checker import (
    DictRateLimitChecker,
)
from twitter_api.rate_limit.manager.mixins.raise_rate_limit_manager_mixin import (
    RaiseRateLimitManagerMixin,
)
from twitter_api.rate_limit.manager.rate_limit_manager import RateLimitManager


class DictRateLimitManager(
    DictRateLimitChecker, RaiseRateLimitManagerMixin, RateLimitManager
):
    """
    単純なハッシュマップによるレートリミットの管理を行うマネージャ。

    Redis, RDS などで管理したい場合は、
    このクラスを参考に RateLimitManager を実装すればよい。
    """

    pass
