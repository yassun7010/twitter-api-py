from abc import ABCMeta, abstractmethod

from twitter_api.ratelimit.manager.ratelimit_manager import RatelimitManager


class RatelimitInterface(metaclass=ABCMeta):
    @property
    @abstractmethod
    def ratelimit(self) -> RatelimitManager:
        ...
