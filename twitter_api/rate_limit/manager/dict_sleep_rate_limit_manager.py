from twitter_api.rate_limit.manager.dict_rate_limit_manager import DictRateLimitManager
from twitter_api.rate_limit.manager.handlers.sleep_rate_limit_handler import (
    SleepRateLimitHandler,
)


class DictSleepRateLimitManager(DictRateLimitManager, SleepRateLimitHandler):
    """
    単純なハッシュマップによるレートリミットの管理を行うマネージャ。

    DictSleepRateLimitManager と異なり、レートリミットオーバーになったとき、スリープする。
    """

    pass
