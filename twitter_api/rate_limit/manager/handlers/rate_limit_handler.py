from abc import ABCMeta, abstractmethod
from contextlib import asynccontextmanager, contextmanager
from typing import AsyncGenerator, Generator

from twitter_api.rate_limit.rate_limit_info import RateLimitInfo


class RateLimitHandler(metaclass=ABCMeta):
    @abstractmethod
    @contextmanager
    def handle_rate_limit_sync(
        self, rate_limit_info: RateLimitInfo
    ) -> Generator[None, None, None]:
        """
        同期的な TwitterApiClient を用いている場合のレートリミットの対応方法。
        """

        ...

    @abstractmethod
    @asynccontextmanager
    async def handle_rate_limit_async(
        self, rate_limit_info: RateLimitInfo
    ) -> AsyncGenerator[None, None]:
        """
        非同期的な TwitterApiAsyncClient を用いている場合のレートリミットの対応方法。
        """

        ...
