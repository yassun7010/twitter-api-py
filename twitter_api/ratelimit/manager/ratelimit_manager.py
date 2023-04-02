from abc import ABCMeta, abstractmethod

from twitter_api.ratelimit.ratelimit import Ratelimit


class RatelimitManager(metaclass=ABCMeta):
    @abstractmethod
    def check_limit_over(self, ratelimit: Ratelimit) -> bool:
        ...
