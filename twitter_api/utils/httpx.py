from ssl import SSLContext
from typing import Any, Callable, Mapping, Optional, TypeAlias, Union

import httpx

Client: TypeAlias = httpx.Client
AsyncClient: TypeAlias = httpx.AsyncClient

Response: TypeAlias = httpx.Response

URLTypes: TypeAlias = httpx.URL | str
ProxiesTypes: TypeAlias = (
    URLTypes | httpx.Proxy | dict[URLTypes, Optional[URLTypes | httpx.Proxy]]
)
Limits: TypeAlias = httpx.Limits
VerifyTypes = str | bool | SSLContext
TimeoutSecond: TypeAlias = float
Timeout: TypeAlias = httpx.Timeout
TimeoutTypes: TypeAlias = Union[
    TimeoutSecond,
    tuple[
        Optional[TimeoutSecond],
        Optional[TimeoutSecond],
        Optional[TimeoutSecond],
        Optional[TimeoutSecond],
    ],
    httpx.Timeout,
]

BaseTransport: TypeAlias = httpx.BaseTransport
AsyncBaseTransport: TypeAlias = httpx.AsyncBaseTransport

EventHook = Mapping[str, list[Callable[..., Any]]]


def update_client_kwargs(
    event_hooks: Optional[EventHook],
    limits: Optional[Limits],
    mounts: Optional[Mapping[str, BaseTransport | AsyncBaseTransport]],
    proxies: Optional[ProxiesTypes],
    timeout: Optional[TimeoutTypes],
    transport: Optional[BaseTransport | AsyncBaseTransport],
    verify: Optional[VerifyTypes],
    *,
    kwargs: dict[str, Any],
) -> dict:
    if event_hooks is not None:
        kwargs["event_hooks"] = event_hooks

    if limits is not None:
        kwargs["limits"] = limits

    if mounts is not None:
        kwargs["mounts"] = mounts

    if proxies is not None:
        kwargs["proxies"] = proxies

    if timeout is not None:
        kwargs["timeout"] = timeout

    if transport is not None:
        kwargs["transport"] = transport

    if verify is not None:
        kwargs["verify"] = verify

    return kwargs
