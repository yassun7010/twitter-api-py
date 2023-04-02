from abc import ABCMeta, abstractmethod

from twitter_api.ratelimit.ratelimit import Ratelimit


class RatelimitManager(metaclass=ABCMeta):
    @abstractmethod
    def check_ratelimit(self, ratelimit: Ratelimit) -> bool:
        ...
