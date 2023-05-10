from twitter_api.rate_limit.manager.checkers.dict_rate_limit_checker import (
    DictRateLimitChecker,
)
from twitter_api.rate_limit.manager.mixins.raise_rate_limit_mixin import (
    RaiseRateLimitMixin,
)
from twitter_api.rate_limit.manager.rate_limit_manager import RateLimitManager


class DictRateLimitManager(DictRateLimitChecker, RaiseRateLimitMixin, RateLimitManager):
    """
    単純なハッシュマップによるレートリミットの管理を行うマネージャ。

    Redis, RDS などで管理したい場合は、
    このクラスを参考に RateLimitManager を実装すればよい。
    """

    pass
