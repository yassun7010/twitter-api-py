from contextlib import asynccontextmanager, contextmanager
from typing import AsyncGenerator, Generator

from twitter_api.error import RateLimitOverError
from twitter_api.rate_limit.manager.rate_limit_manager import RateLimitManager
from twitter_api.rate_limit.rate_limit_info import RateLimitInfo


class RaiseRateLimitHandler(RateLimitManager):
    """
    レートリミットオーバーが発生した場合、例外を投げるもっとも単純な handler。
    """

    @asynccontextmanager
    async def handle_rate_limit_async(
        self, rate_limit_info: RateLimitInfo
    ) -> AsyncGenerator[None, None]:
        """
        非同期的な TwitterApiAsyncClient を用いている場合のレートリミットの処理方法。
        """

        if self.check_limit_over(rate_limit_info) is not None:
            raise RateLimitOverError(rate_limit_info)

        yield

    @contextmanager
    def handle_rate_limit_sync(
        self, rate_limit_info: RateLimitInfo
    ) -> Generator[None, None, None]:
        """
        同期的な TwitterApiClient を用いている場合のレートリミットの処理方法。
        """

        if self.check_limit_over(rate_limit_info) is not None:
            raise RateLimitOverError(rate_limit_info)

        yield
