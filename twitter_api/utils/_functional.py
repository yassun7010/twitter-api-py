from typing import Any, Callable, Optional, TypeVar, overload

T = TypeVar("T")
S = TypeVar("S")


def map_optional(method: Callable[[T], S], data: Optional[T]) -> Optional[S]:
    if data is None:
        return None
    else:
        return method(data)


@overload
def exclude_none(data: dict) -> dict:
    ...


@overload
def exclude_none(data: Optional[dict]) -> Optional[dict]:
    ...


def exclude_none(data: Optional[dict]) -> Optional[dict]:
    if data is None:
        return None

    return {k: _exclude_none_recursive(v) for k, v in data.items() if v is not None}


def _exclude_none_recursive(data: Any):
    if isinstance(data, dict):
        return exclude_none(data)
    else:
        return data
