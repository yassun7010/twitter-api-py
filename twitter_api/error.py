from collections import OrderedDict
from textwrap import dedent
from typing import Any, Never, Optional

import pydantic

from twitter_api.rate_limit.rate_limit_data import RateLimitData
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel

from .types.endpoint import Endpoint
from .types.http import Headers, QuryParameters, RequestJsonBody, ResponseJsonBody
from .types.oauth import OAuthVersion
from .utils.json import exclude_none


class ErrorMessage(ExtraPermissiveModel):
    type: str
    message: str
    erros: Optional[list[str]] = None

    def to_message(self) -> str:
        return self.json()


class TwitterApiException(Exception):
    ...


class TwitterApiError(TwitterApiException):
    ...


class NeverError(TwitterApiError):
    def __init__(self, never: Never):
        self._never = never

    def __str__(self) -> str:
        return ErrorMessage(
            type=self.__class__.__name__,
            message=f'到達できない入力 "{self._never}" が与えられました。',
        ).to_message()


class MockResponseNotFound(TwitterApiError):
    def __str__(self) -> str:
        return ErrorMessage(
            type=self.__class__.__name__,
            message=dedent(
                """
                モックとして出力したいデータが入力されていません。
                `client.inject_*(response)` で定義されているメソッドを用い、
                レスポンスデータを定義した後で、API を呼んでください。
                """
            ),
        ).to_message()


class MockInjectionResponseWrong(TwitterApiError):
    def __init__(self, endpoint: Endpoint, expected_endpoint: Endpoint):
        self._endpoint = endpoint
        self._expected_endpoint = expected_endpoint

    def __str__(self) -> str:
        return ErrorMessage(
            type=self.__class__.__name__,
            message=("出力したいレスポンスのエンドポイントが異なっています。"),
            **dict(
                expected_endpoint=self._expected_endpoint,
                endpoint=self._endpoint,
            ),
        ).to_message()


class TwitterApiResponseModelBodyDecodeError(TwitterApiError):
    def __init__(self, endpoint: Endpoint, content: bytes, **extra):
        self._endpoint = endpoint
        self._content = content
        self._extra = extra

    def __str__(self) -> str:
        return ErrorMessage(
            type=self.__class__.__name__,
            message="Twitter API の応答のボディを JSON でパースできませんでした。",
            **dict(endpoint=self._endpoint, content=self._content),
            **exclude_none(self._extra),
        ).to_message()


class TwitterApiResponseFailed(TwitterApiError):
    def __init__(
        self,
        endpoint: Endpoint,
        url: str,
        request_headers: Optional[Headers],
        query: Optional[QuryParameters],
        request_body: Optional[RequestJsonBody],
        response_status_code: int,
        response_body: Optional[ResponseJsonBody | bytes],
    ):
        self._endpoint = endpoint
        self._url = url
        self._request_headers = request_headers
        self._query = query
        self._request_body = request_body
        self._response_status_code = response_status_code
        self._response_body = response_body

    def __str__(self) -> str:
        return ErrorMessage(
            type=self.__class__.__name__,
            message="Twitter API の応答が 200 ではありません。",
            **OrderedDict(
                endpoint=self._endpoint,
                url=self._url,
                reqeust_headers=exclude_none(self._request_headers),
                query=exclude_none(self._query),
                request_body=exclude_none(self._request_body),
                response_status_code=self._response_status_code,
                response_body=(
                    exclude_none(self._response_body)
                    if not isinstance(self._response_body, bytes)
                    else self._response_body
                ),
            ),
        ).to_message()


class TwitterApiResponseError(TwitterApiError):
    def __init__(self, endpoint: Endpoint, data: Any, **extra):
        self._endpoint = endpoint
        self._data = data
        self._extra = extra

    def __str__(self) -> str:
        return ErrorMessage(
            type=self.__class__.__name__,
            message="Twitter API の応答でエラーが返りました。",
            **dict(
                endpoint=self._endpoint,
                data=exclude_none(self._data),
            ),
            **exclude_none(self._extra),
        ).to_message()


class TwitterApiResponseValidationError(TwitterApiError):
    def __init__(
        self, endpoint: Endpoint, response_body: Any, error: pydantic.ValidationError
    ):
        self._endpoint = endpoint
        self._response_body = response_body
        self._error = error

    def __str__(self) -> str:
        return ErrorMessage(
            type=self.__class__.__name__,
            message="Twitter API の応答の型が想定とは一致していません。",
            **dict(
                endpoint=self._endpoint,
                response_body=exclude_none(self._response_body),
                error=self._error.errors(),
            ),
        ).to_message()


class TwitterApiOAuthTokenV1NotFound(TwitterApiError):
    def __init__(self, endpoint, data: Any, **extra):
        self._endpoint = endpoint
        self._data = data
        self._extra = extra

    def __str__(self) -> str:
        return ErrorMessage(
            type=self.__class__.__name__,
            message="OAuth V1 のトークンが見つかりませんでした。",
            **dict(
                endpoint=self._endpoint,
                data=exclude_none(self._data),
            ),
            **exclude_none(self._extra),
        ).to_message()


class TwitterApiOAuthVersionWrong(TwitterApiError):
    def __init__(self, *, version: OAuthVersion, expected_version: OAuthVersion):
        self._version = version
        self._expected_version = expected_version

    def __str__(self) -> str:
        return ErrorMessage(
            type=self.__class__.__name__,
            message=(
                f'OAuth のバージョンは "{self._version}" ではなく'
                f' "{self._expected_version}" である必要があります。'
            ),
        ).to_message()


class RateLimitOverError(TwitterApiError):
    def __init__(self, rate_limit: RateLimitData) -> None:
        self._rate_limit = rate_limit

    def __str__(self) -> str:
        return f"レートリミットを超えています。{self._rate_limit}"
