from typing import TypeAlias

import httpx

Client: TypeAlias = httpx.Client
AsyncClient: TypeAlias = httpx.AsyncClient

Response: TypeAlias = httpx.Response

URL: TypeAlias = httpx.URL
URLTypes: TypeAlias = httpx._types.URLTypes
Proxy: TypeAlias = httpx.Proxy
ProxiesTypes: TypeAlias = httpx._types.ProxiesTypes
Limits: TypeAlias = httpx.Limits
VerifyTypes = httpx._types.VerifyTypes
Timeout: TypeAlias = httpx.Timeout
TimeoutTypes: TypeAlias = httpx._types.TimeoutTypes

BaseTransport: TypeAlias = httpx.BaseTransport
AsyncBaseTransport: TypeAlias = httpx.AsyncBaseTransport

EventHook: TypeAlias = httpx._client.EventHook

DEFAULT_LIMITS = httpx._config.DEFAULT_LIMITS
DEFAULT_TIMEOUT_CONFIG = httpx._config.DEFAULT_TIMEOUT_CONFIG
