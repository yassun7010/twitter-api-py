from typing import Generator

from typing_extensions import override

from twitter_api.error import RateLimitOverError
from twitter_api.rate_limit.manager.rate_limit_manager import RateLimitManager
from twitter_api.rate_limit.rate_limit_info import RateLimitInfo


class RaiseRateLimitHandlerMixin(RateLimitManager):
    """
    レートリミットオーバーが発生した場合、例外を投げる単純な操作を行う。
    """

    @override
    def handle(self, rate_limit_info: RateLimitInfo) -> Generator[None, None, None]:
        if self.check_limit_over(rate_limit_info) is not None:
            raise RateLimitOverError(rate_limit_info)

        yield
