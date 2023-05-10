from twitter_api.rate_limit.manager.checkers.no_operation_rate_limit_checker import (
    NoOperationRateLimitChecker,
)
from twitter_api.rate_limit.manager.handlers.raise_rate_limit_handler import (
    RaiseRateLimitHandler,
)
from twitter_api.rate_limit.manager.rate_limit_manager import RateLimitManager


class NoOperationRateLimitManager(
    NoOperationRateLimitChecker, RaiseRateLimitHandler, RateLimitManager
):
    """
    レートリミットに関して、クライアント側で何も制御しないマネージャ。

    Twitter API が返すレートリミットエラーをそのまま例外として投げることを想定している。
    """

    pass
