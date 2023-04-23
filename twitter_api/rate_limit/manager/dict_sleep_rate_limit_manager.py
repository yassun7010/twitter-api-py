from twitter_api.rate_limit.manager.dict_rate_limit_manager import DictRateLimitManager
from twitter_api.rate_limit.manager.sleep_rate_limit_manager import (
    SleepRateLimitManager,
)


class DictSleepRateLimitManager(DictRateLimitManager, SleepRateLimitManager):
    pass
