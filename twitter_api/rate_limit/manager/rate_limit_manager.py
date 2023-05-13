from abc import ABCMeta, abstractmethod
from contextlib import asynccontextmanager, contextmanager
from datetime import datetime
from typing import AsyncGenerator, Generator, Optional

from twitter_api.rate_limit.rate_limit_info import RateLimitInfo


class RateLimitManager(metaclass=ABCMeta):
    @abstractmethod
    def check_limit_over(
        self,
        rate_limit_info: RateLimitInfo,
        now: Optional[datetime] = None,
    ) -> Optional[float]:
        """
        レートリミットオーバーかを調べ、超えている場合は必要な待ち時間[秒]を返す。
        """

        ...

    @abstractmethod
    @contextmanager
    def handle(self, rate_limit_info: RateLimitInfo) -> Generator[None, None, None]:
        """
        同期的な TwitterApiClient を用いている場合のレートリミットの対応方法。
        """

        ...

    @asynccontextmanager
    async def ahandle(
        self, rate_limit_info: RateLimitInfo
    ) -> AsyncGenerator[None, None]:
        """
        非同期的な TwitterApiAsyncClient を用いている場合のレートリミットの対応方法。
        """

        with self.handle(rate_limit_info):
            yield


class RetryRateLimitHandling(Exception):
    """
    レートリミットの制御処理を繰り返すことを指示。
    """

    pass
