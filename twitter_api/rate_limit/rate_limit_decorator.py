from typing import Callable, Literal, Optional, overload

from twitter_api.client.request.has_request_client import HasReqeustClient
from twitter_api.error import RateLimitOverError
from twitter_api.rate_limit.rate_limit_info import RateLimitInfo
from twitter_api.rate_limit.rate_limit_target import RateLimitTarget
from twitter_api.types.endpoint import Endpoint


@overload
def rate_limit(
    endpoint: Endpoint,
    target: RateLimitTarget,
    *,
    requests: int,
    seconds: int,
    mins: Literal[None] = None,
) -> Callable:
    ...


@overload
def rate_limit(
    endpoint: Endpoint,
    target: RateLimitTarget,
    *,
    requests: int,
    mins: int,
    seconds: Literal[None] = None,
) -> Callable:
    ...


def rate_limit(
    endpoint: Endpoint,
    target: RateLimitTarget,
    *,
    requests: int,
    mins: Optional[int] = None,
    seconds: Optional[int] = None,
) -> Callable:
    """
    レートリミットに関する情報を付与します。

    将来的には、レートリミットを回避するように非同期で api を実行する機能を提供します。

    また、公式には明らかになっていないレートリミットを追加する機能、
    特定のアカウント用にレートリミットを上書きする機能も提供します。
    """

    def _rate_limit(func):
        def _wrapper(self: HasReqeustClient, *args, **kwargs):
            total_seconds = 0
            if seconds is not None:
                total_seconds += seconds
            if mins is not None:
                total_seconds += 60 * mins

            data = RateLimitInfo(
                target=target,
                endpoint=endpoint,
                requests=requests,
                total_seconds=total_seconds,
            )

            if self.request_client.rate_limit_manager.check_limit_over(data):
                raise RateLimitOverError(data)

            return func(self, *args, **kwargs)

        return _wrapper

    return _rate_limit
