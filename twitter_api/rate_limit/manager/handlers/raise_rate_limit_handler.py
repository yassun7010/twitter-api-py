from contextlib import asynccontextmanager, contextmanager
from typing import AsyncGenerator, Generator

from twitter_api.error import RateLimitOverError
from twitter_api.rate_limit.manager.rate_limit_manager import RateLimitManager
from twitter_api.rate_limit.rate_limit_info import RateLimitInfo


class RaiseRateLimitHandler(RateLimitManager):
    """
    レートリミットオーバーが発生した場合、例外を投げるもっとも単純な handler。
    """

    @contextmanager
    def handle_rate_limit_sync(
        self, rate_limit_info: RateLimitInfo
    ) -> Generator[None, None, None]:
        if self.check_limit_over(rate_limit_info) is not None:
            raise RateLimitOverError(rate_limit_info)

        yield

    @asynccontextmanager
    async def handle_rate_limit_async(
        self, rate_limit_info: RateLimitInfo
    ) -> AsyncGenerator[None, None]:
        if self.check_limit_over(rate_limit_info) is not None:
            raise RateLimitOverError(rate_limit_info)

        yield
