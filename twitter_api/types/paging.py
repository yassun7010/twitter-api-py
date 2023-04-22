from abc import ABCMeta, abstractmethod
from typing import (
    Any,
    AsyncGenerator,
    Callable,
    Coroutine,
    Generator,
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


def get_paging_response_iter_sync(
    get_func: Callable[
        [AnyQueryParameters],
        AnyPageResponseBody,
    ],
    query: Optional[AnyQueryParameters],
) -> Generator[AnyPageResponseBody, None, None]:
    """
    ページングされたレスポンスを返す API に対して、ページングをイテレータで返す。
    """
    if query is None:
        _query: AnyQueryParameters = {"next_token": None}  # type: ignore
    else:
        _query = query

    next_token = _query.get("next_token")

    while True:
        _query["next_token"] = next_token  # type: ignore
        response = get_func(_query)

        yield response

        next_token = response.meta_next_token

        if next_token is None:
            return


def get_collected_paging_response_sync(
    get_func: Callable[
        [AnyQueryParameters],
        AnyPageResponseBody,
    ],
    query: Optional[AnyQueryParameters],
) -> AnyPageResponseBody:
    """
    ページングされたレスポンスを返す API に対して、最後までデータを読み取り、結合した状態で返す。
    """
    paging = get_paging_response_iter_sync(get_func, query)
    first = next(paging)

    for page in paging:
        first.extend(page)
    return first


async def get_paging_response_iter_async(
    get_func: Callable[
        [AnyQueryParameters],
        Coroutine[Any, Any, AnyPageResponseBody],
    ],
    query: Optional[AnyQueryParameters],
) -> AsyncGenerator[AnyPageResponseBody, None]:
    """
    ページングされたレスポンスを返す API に対して、ページングをイテレータで返す。
    """
    if query is None:
        _query: AnyQueryParameters = {"next_token": None}  # type: ignore
    else:
        _query = query
    next_token = _query.get("next_token")

    while True:
        _query["next_token"] = next_token  # type: ignore
        response = await get_func(_query)

        yield response

        next_token = response.meta_next_token

        if next_token is None:
            return


async def get_collected_paging_response_async(
    get_func: Callable[
        [AnyQueryParameters],
        Coroutine[Any, Any, AnyPageResponseBody],
    ],
    query: Optional[AnyQueryParameters],
) -> AnyPageResponseBody:
    """
    ページングされたレスポンスを返す API に対して、最後までデータを読み取り、結合した状態で返す。
    """
    paging = get_paging_response_iter_async(get_func, query)
    first = await paging.__anext__()

    async for page in paging:
        first.extend(page)
    return first
