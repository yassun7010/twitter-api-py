from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import Optional

from twitter_api.ratelimit.ratelimit import Ratelimit


class RatelimitManager(metaclass=ABCMeta):
    @abstractmethod
    def check_limit_over(
        self,
        ratelimit: Ratelimit,
        now: Optional[datetime] = None,
    ) -> bool:
        ...
