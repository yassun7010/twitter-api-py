from typing import Callable, Literal, Optional, TypeAlias, overload

RateLimitTarget: TypeAlias = Literal["app", "user"]


@overload
def rate_limit(
    target: RateLimitTarget,
    *,
    requests: int,
    secs: int,
    mins: Literal[None] = None,
) -> Callable:
    ...


@overload
def rate_limit(
    target: RateLimitTarget,
    *,
    requests: int,
    mins: int,
    secs: Literal[None] = None,
) -> Callable:
    ...


def rate_limit(
    target: RateLimitTarget,
    *,
    requests: int,
    mins: Optional[int] = None,
    secs: Optional[int] = None,
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
