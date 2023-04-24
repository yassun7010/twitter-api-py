from typing import Callable, Optional, TypeVar

T = TypeVar("T")
S = TypeVar("S")


def map_optional(method: Callable[[T], S], data: Optional[T]) -> Optional[S]:
    if data is None:
        return None
    else:
        return method(data)
