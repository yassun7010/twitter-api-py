from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import Optional

from twitter_api.ratelimit.ratelimit_data import RatelimitData


class RatelimitManager(metaclass=ABCMeta):
    @abstractmethod
    def check_limit_over(
        self,
        ratelimit: RatelimitData,
        now: Optional[datetime] = None,
    ) -> bool:
        ...
