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


async def get_paging_response_iter(
    get_func: Callable[
        [AnyQueryParameters],
        Coroutine[Any, Any, AnyPageResponseBody],
    ],
    query: AnyQueryParameters,
) -> AsyncGenerator[AnyPageResponseBody, None]:
    """
    ページングされたレスポンスを返す API に対して、ページングをイテレータで返す。

    この関数は非同期の場合にしか用意されていない。
    理由は、同期の場合レートリミットの制限に引っかかると即時でエラーを返す仕様のため。

    非同期の場合、レートリミットエラーになった際に処理を別のタスクに返す RateLimitManager が用意されている。
    """
    next_token = query.get("next_token")

    while True:
        query["next_token"] = next_token  # type: ignore
        response = await get_func(query)

        yield response

        next_token = response.meta_next_token

        if next_token is None:
            return


async def get_collected_paging_response(
    get_func: Callable[
        [AnyQueryParameters],
        Coroutine[Any, Any, AnyPageResponseBody],
    ],
    query: AnyQueryParameters,
) -> AnyPageResponseBody:
    """
    ページングされたレスポンスを返す API に対して、最後までデータを読み取り、結合した状態で返す。
    """
    paging = get_paging_response_iter(get_func, query)
    first = await paging.__anext__()

    async for page in paging:
        first.extend(page)
    return first
