import asyncio
import time
from abc import abstractmethod
from logging import getLogger
from random import randint
from typing import AsyncGenerator, Generator

from twitter_api.error import TwitterApiErrorCode, TwitterApiResponseFailed
from twitter_api.rate_limit.manager.rate_limit_manager import (
    LoopRateLimitHandling,
    RateLimitManager,
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
    @abstractmethod
    def max_random_sleep_seconds(self) -> int:
        ...

    @property
    @abstractmethod
    def min_random_sleep_seconds(self) -> int:
        ...

    def generate_random_sleep_seconds(self) -> int:
        """
        予期しないレートリミットに遭遇した場合にランダムに休む時間[秒]。
        """

        return randint(self.min_random_sleep_seconds, self.max_random_sleep_seconds)

    def handle_rate_limit_sync(
        self, rate_limit_info: RateLimitInfo
    ) -> Generator[None, None, None]:
        # レートリミットを超えてしまっていたら、必要な待ち時間分だけ待つ。
        if wait_time_seconds := self.check_limit_over(rate_limit_info):
            logger.warning(RateLimitOverWarning(rate_limit_info))
            time.sleep(wait_time_seconds)

            raise LoopRateLimitHandling()

        try:
            yield

        except TwitterApiResponseFailed as error:
            # レートリミット以外のエラーなら上流に投げる。
            if error.status_code != TwitterApiErrorCode.TooManyRequests.value:
                raise error

            # 予期しないレートリミットに遭遇した場合、投機的な待機を行う。
            logger.warning(UnmanagedRateLimitOverWarning())
            time.sleep(self.generate_random_sleep_seconds())

            raise LoopRateLimitHandling()

    async def handle_rate_limit_async(
        self, rate_limit_info: RateLimitInfo
    ) -> AsyncGenerator[None, None]:
        # レートリミットを超えてしまっていたら、必要な待ち時間分だけ待つ。
        if wait_time_seconds := self.check_limit_over(rate_limit_info):
            logger.warning(RateLimitOverWarning(rate_limit_info))
            await asyncio.sleep(wait_time_seconds)

            raise LoopRateLimitHandling()

        try:
            yield

        except TwitterApiResponseFailed as error:
            # レートリミットのエラーでないなら上流に投げる。
            if error.status_code != TwitterApiErrorCode.TooManyRequests.value:
                raise error

            # 予期しないレートリミットに遭遇した場合、投機的な待機を行う。
            logger.warning(UnmanagedRateLimitOverWarning())
            await asyncio.sleep(self.generate_random_sleep_seconds())

            raise LoopRateLimitHandling()
