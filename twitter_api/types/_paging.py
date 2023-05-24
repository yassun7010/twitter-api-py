from abc import ABCMeta, abstractmethod
from typing import Callable, Generator, Optional, cast

from typing_extensions import Any, AsyncGenerator, Coroutine, Self, TypedDict, TypeVar

from twitter_api.types.pagination_token import PaginationToken


class PageResponseBody(metaclass=ABCMeta):
    @property
    @abstractmethod
    def meta_next_token(self) -> Optional[PaginationToken]:
        ...

    @abstractmethod
    def extend(self, other: Self) -> None:
        ...


AnyQueryParameters = TypeVar("AnyQueryParameters", bound=TypedDict)

AnyPageResponseBody = TypeVar(
    "AnyPageResponseBody",
    bound=PageResponseBody,
)


def get_paging_iter(
    get_func: Callable[
        [AnyQueryParameters],
        AnyPageResponseBody,
    ],
    query: Optional[AnyQueryParameters],
    pagination_token_key: str,
) -> Generator[AnyPageResponseBody, None, None]:
    """
    ページングされたレスポンスを返す API に対して、ページングをイテレータで返す。
    """
    _query = cast(dict, query if query is not None else {pagination_token_key: None})

    next_token = _query.get(pagination_token_key)

    while True:
        _query[pagination_token_key] = next_token
        response_body = get_func(cast(AnyQueryParameters, _query))

        yield response_body

        next_token = response_body.meta_next_token

        if next_token is None:
            return


def get_paging_all(
    get_func: Callable[
        [AnyQueryParameters],
        AnyPageResponseBody,
    ],
    query: Optional[AnyQueryParameters],
    pagination_token_key: str,
) -> AnyPageResponseBody:
    """
    ページングされたレスポンスを返す API に対して、最後までデータを読み取り、結合した状態で返す。
    """
    paging = get_paging_iter(get_func, query, pagination_token_key)
    first = next(paging)

    for page in paging:
        first.extend(page)

    return first


async def aget_paging_iter(
    get_func: Callable[
        [AnyQueryParameters],
        Coroutine[Any, Any, AnyPageResponseBody],
    ],
    query: Optional[AnyQueryParameters],
    pagination_token_key: str,
) -> AsyncGenerator[AnyPageResponseBody, None]:
    """
    ページングされたレスポンスを返す API に対して、ページングをイテレータで返す。
    """
    _query = cast(dict, query if query is not None else {pagination_token_key: None})

    next_token = _query.get(pagination_token_key)

    while True:
        _query[pagination_token_key] = next_token
        response_body = await get_func(cast(AnyQueryParameters, _query))

        yield response_body

        next_token = response_body.meta_next_token

        if next_token is None:
            return


async def aget_paging_all(
    get_func: Callable[
        [AnyQueryParameters],
        Coroutine[Any, Any, AnyPageResponseBody],
    ],
    query: Optional[AnyQueryParameters],
    pagination_token_key: str,
) -> AnyPageResponseBody:
    """
    ページングされたレスポンスを返す API に対して、最後までデータを読み取り、結合した状態で返す。
    """
    paging = aget_paging_iter(get_func, query, pagination_token_key)
    first = await paging.__anext__()

    async for page in paging:
        first.extend(page)

    return first
