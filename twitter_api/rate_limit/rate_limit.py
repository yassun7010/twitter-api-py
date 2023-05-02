from typing import Callable, Literal, Optional, overload

from twitter_api.client.request.request_async_client import RequestAsyncClient
from twitter_api.rate_limit.rate_limit_info import RateLimitInfo
from twitter_api.rate_limit.rate_limit_target import RateLimitTarget
from twitter_api.resources.api_resources import ApiResources
from twitter_api.types.endpoint import Endpoint


@overload
def rate_limit(
    endpoint: Endpoint,
    target: RateLimitTarget,
    *,
    requests: int,
    hours: int,
    mins: Literal[None] = None,
    seconds: Literal[None] = None,
) -> Callable:
    ...


@overload
def rate_limit(
    endpoint: Endpoint,
    target: RateLimitTarget,
    *,
    requests: int,
    seconds: int,
    hours: Literal[None] = None,
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
    hours: Literal[None] = None,
    seconds: Literal[None] = None,
) -> Callable:
    ...


def rate_limit(
    endpoint: Endpoint,
    target: RateLimitTarget,
    *,
    requests: int,
    hours: Optional[int] = None,
    mins: Optional[int] = None,
    seconds: Optional[int] = None,
) -> Callable:
    """
    レートリミットに関する情報を付与します。

    将来的には、公式には明らかになっていないレートリミットを追加する機能、
    特定のアカウント用にレートリミットを上書きする機能を提供するかもしれません。
    """

    def _rate_limit(func):
        async def handle_async(
            rate_limit_info: RateLimitInfo, self: ApiResources, *args, **kwargs
        ):
            rate_limit_manager = self.request_client.rate_limit_manager

            async with rate_limit_manager.handle_rate_limit_async(
                rate_limit_info,
            ):
                return await func(self, *args, **kwargs)

        def handle_sync(
            rate_limit_info: RateLimitInfo, self: ApiResources, *args, **kwargs
        ):
            rate_limit_manager = self.request_client.rate_limit_manager

            with rate_limit_manager.handle_rate_limit_sync(
                rate_limit_info,
            ):
                return func(self, *args, **kwargs)

        def _wrapper(self: ApiResources, *args, **kwargs):
            if self.request_client.rate_limit_target != target:
                return func(self, *args, **kwargs)

            # RateLimitTarget が一致する場合、 LimitOver を確認する。
            total_seconds = 0
            if hours is not None:
                total_seconds += 3600 * hours
            if mins is not None:
                total_seconds += 60 * mins
            if seconds is not None:
                total_seconds += seconds

            rate_limit_info = RateLimitInfo(
                target=target,
                endpoint=endpoint,
                requests=requests,
                total_seconds=total_seconds,
            )

            if isinstance(self.request_client, RequestAsyncClient):
                return handle_async(rate_limit_info, self, *args, **kwargs)
            else:
                return handle_sync(rate_limit_info, self, *args, **kwargs)

        return _wrapper

    return _rate_limit
