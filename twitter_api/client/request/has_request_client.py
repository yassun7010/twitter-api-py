from abc import ABCMeta, abstractmethod

from twitter_api.client.request.request_client import RequestClient


class HasReqeustClient(metaclass=ABCMeta):
    @property
    @abstractmethod
    def request_client(self) -> RequestClient:
        ...
