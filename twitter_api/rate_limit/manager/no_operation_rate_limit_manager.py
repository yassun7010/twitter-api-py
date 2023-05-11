from contextlib import asynccontextmanager, contextmanager
from datetime import datetime
from typing import AsyncGenerator, Generator, Optional

from twitter_api.rate_limit.manager.rate_limit_manager import RateLimitManager
from twitter_api.rate_limit.rate_limit_info import RateLimitInfo


class NoOperationRateLimitManager(RateLimitManager):
    """
    レートリミットに関して、クライアント側で何も制御しないマネージャ。

    Twitter API が返すレートリミットエラーをそのまま例外として投げることを想定している。
    """

    def check_limit_over(
        self,
        rate_limit_info: RateLimitInfo,
        now: Optional[datetime] = None,
    ) -> Optional[float]:
        return None

    @contextmanager
    def handle_rate_limit_sync(
        self, rate_limit_info: RateLimitInfo
    ) -> Generator[None, None, None]:
        yield

    @asynccontextmanager
    async def handle_rate_limit_async(
        self, rate_limit_info: RateLimitInfo
    ) -> AsyncGenerator[None, None]:
        yield
