from typing import Callable, Literal, Optional, overload

from twitter_api.ratelimit.ratelimit_target import RatelimitTarget


@overload
def rate_limit(
    target: RatelimitTarget,
    *,
    requests: int,
    seconds: int,
    mins: Literal[None] = None,
) -> Callable:
    ...


@overload
def rate_limit(
    target: RatelimitTarget,
    *,
    requests: int,
    mins: int,
    seconds: Literal[None] = None,
) -> Callable:
    ...


def rate_limit(
    target: RatelimitTarget,
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
        def _wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return _wrapper

    return _rate_limit
