import asyncio
import time
from logging import getLogger
from random import randint
from typing import Generator

from typing_extensions import AsyncGenerator, override

from twitter_api.error import TwitterApiErrorCode, TwitterApiResponseFailed
from twitter_api.rate_limit.manager.rate_limit_manager import (
    RateLimitManager,
    RetryRateLimitHandling,
)
from twitter_api.rate_limit.rate_limit_info import RateLimitInfo
from twitter_api.warning import RateLimitOverWarning, UnmanagedRateLimitOverWarning

logger = getLogger(__file__)

DEFAULT_MIN_RANDOM_SLEEP_SECONDS = 5 * 60
DEFAULT_MAX_RANDOM_SLEEP_SECONDS = 15 * 60


class SleepRateLimitHandlerMixin(RateLimitManager):
    """
    レートリミットに遭遇した場合、レートリミットが解除されるまでスリープする。
    """

    @property
    def min_random_sleep_seconds(self) -> int:
        return DEFAULT_MIN_RANDOM_SLEEP_SECONDS

    @property
    def max_random_sleep_seconds(self) -> int:
        return DEFAULT_MAX_RANDOM_SLEEP_SECONDS

    def generate_random_sleep_seconds(self) -> int:
        """
        予期しないレートリミットに遭遇した場合にランダムに休む時間[秒]。
        """

        return randint(self.min_random_sleep_seconds, self.max_random_sleep_seconds)

    @override
    def handle(self, rate_limit_info: RateLimitInfo) -> Generator[None, None, None]:
        # レートリミットを超えてしまっていたら、必要な待ち時間分だけ待つ。
        if wait_time_seconds := self.check_limit_over(rate_limit_info):
            logger.warning(RateLimitOverWarning(rate_limit_info))
            time.sleep(wait_time_seconds)

            raise RetryRateLimitHandling()

        try:
            yield

        except TwitterApiResponseFailed as error:
            # レートリミット以外のエラーなら上流に投げる。
            if error.status_code != TwitterApiErrorCode.TooManyRequests.value:
                raise error

            # 予期しないレートリミットに遭遇した場合、投機的な待機を行う。
            logger.warning(UnmanagedRateLimitOverWarning())
            time.sleep(self.generate_random_sleep_seconds())

            raise RetryRateLimitHandling()

    @override
    async def ahandle(
        self, rate_limit_info: RateLimitInfo
    ) -> AsyncGenerator[None, None]:
        # レートリミットを超えてしまっていたら、必要な待ち時間分だけ待つ。
        if wait_time_seconds := self.check_limit_over(rate_limit_info):
            logger.warning(RateLimitOverWarning(rate_limit_info))
            await asyncio.sleep(wait_time_seconds)

            raise RetryRateLimitHandling()

        try:
            yield

        except TwitterApiResponseFailed as error:
            # レートリミットのエラーでないなら上流に投げる。
            if error.status_code != TwitterApiErrorCode.TooManyRequests.value:
                raise error

            # 予期しないレートリミットに遭遇した場合、投機的な待機を行う。
            logger.warning(UnmanagedRateLimitOverWarning())
            await asyncio.sleep(self.generate_random_sleep_seconds())

            raise RetryRateLimitHandling()
