from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import Optional

from twitter_api.rate_limit.rate_limit_data import RateLimitData


class RateLimitManager(metaclass=ABCMeta):
    @abstractmethod
    def check_limit_over(
        self,
        rate_limit_data: RateLimitData,
        now: Optional[datetime] = None,
    ) -> bool:
        ...
