from twitter_api.rate_limit.manager.checkers.dict_rate_limit_checker import (
    DictRateLimitChecker,
)
from twitter_api.rate_limit.manager.handlers.raise_rate_limit_handler import (
    RaiseRateLimitHandler,
)


class DictRateLimitManager(DictRateLimitChecker, RaiseRateLimitHandler):
    """
    単純なハッシュマップによるレートリミットの管理を行うマネージャ。

    Redis, RDS などで管理したい場合は、
    このクラスを参考に RateLimitManager を実装すればよい。
    """

    pass
