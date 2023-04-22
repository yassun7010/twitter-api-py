from abc import ABCMeta, abstractmethod
from typing import (
    Any,
    AsyncGenerator,
    Callable,
    Coroutine,
    Optional,
    Self,
    TypedDict,
    TypeVar,
)


class PageResponseBody(metaclass=ABCMeta):
    @property
    @abstractmethod
    def meta_next_token(self) -> Optional[str]:
        ...

    @abstractmethod
    def extend(self, other: Self) -> None:
        ...


AnyQueryParameters = TypeVar("AnyQueryParameters", bound=TypedDict)

AnyPageResponseBody = TypeVar(
    "AnyPageResponseBody",
    bound=PageResponseBody,
)


async def get_search_response_iter(
    get_func: Callable[
        [AnyQueryParameters],
        Coroutine[Any, Any, AnyPageResponseBody],
    ],
    query: AnyQueryParameters,
) -> AsyncGenerator[AnyPageResponseBody, None]:
    next_token = query.get("next_token")

    while True:
        query["next_token"] = next_token  # type: ignore
        response = await get_func(query)

        yield response

        next_token = response.meta_next_token

        if next_token is None:
            return


async def get_flattend_search_response(
    get_func: Callable[
        [AnyQueryParameters],
        Coroutine[Any, Any, AnyPageResponseBody],
    ],
    query: AnyQueryParameters,
) -> AnyPageResponseBody:
    paging = get_search_response_iter(get_func, query)
    first = await paging.__anext__()

    async for page in paging:
        first.extend(page)
    return first
