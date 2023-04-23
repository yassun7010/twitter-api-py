import asyncio
import random
import time
from abc import ABCMeta
from contextlib import asynccontextmanager, contextmanager
from logging import getLogger

from twitter_api.error import TwitterApiErrorCode, TwitterApiResponseFailed
from twitter_api.rate_limit.manager.rate_limit_manager import RateLimitManager
from twitter_api.rate_limit.rate_limit_info import RateLimitInfo
from twitter_api.warning import RateLimitOverWarning, UnmanagedRateLimitOverWarning

logger = getLogger(__file__)


class SleepRateLimitHandler(RateLimitManager, metaclass=ABCMeta):
    """
    レートリミットに遭遇した場合、スリープするマネージャ。

    これ自体は抽象クラスなので、他の RateLimitManager と組み合わせる必要がある。
    """

    def random_sleep_seconds(self) -> float:
        """
        予期しないレートリミットに遭遇した場合にランダムに休む時間[秒]。
        """

        # デフォルトは 5 ~ 15 分。
        return random.randint(5 * 60, 15 * 60)

    @asynccontextmanager
    async def handle_rate_limit_async(self, rate_limit_info: RateLimitInfo):
        while True:
            # レートリミットを超えてしまっていたら、必要な待ち時間分だけ待つ。
            wait_time_seconds = self.check_limit_over(rate_limit_info)
            if wait_time_seconds is not None:
                logger.warning(RateLimitOverWarning(rate_limit_info))
                await asyncio.sleep(wait_time_seconds)
                continue

            try:
                yield
            except TwitterApiResponseFailed as error:
                # レートリミットのエラーでないなら上流に投げる。
                if error.status_code != TwitterApiErrorCode.TooManyRequests.value:
                    raise error

                # 予期しないレートリミットに遭遇した場合、投機的な待機を行う
                logger.warning(UnmanagedRateLimitOverWarning())
                await asyncio.sleep(self.random_sleep_seconds())
            else:
                return

    @contextmanager
    def handle_rate_limit_sync(self, rate_limit_info: RateLimitInfo):
        while True:
            # レートリミットを超えてしまっていたら、必要な待ち時間分だけ待つ。
            wait_time_seconds = self.check_limit_over(rate_limit_info)
            if wait_time_seconds is not None:
                logger.warning(RateLimitOverWarning(rate_limit_info))
                time.sleep(wait_time_seconds)
                continue

            try:
                yield
            except TwitterApiResponseFailed as error:
                # レートリミット以外のエラーなら上流に投げる。
                if error.status_code != TwitterApiErrorCode.TooManyRequests.value:
                    raise error

                # 予期しないレートリミットに遭遇した場合、投機的な待機を行う
                logger.warning(UnmanagedRateLimitOverWarning())
                time.sleep(self.random_sleep_seconds())
            else:
                return
