from collections import OrderedDict
from textwrap import dedent
from typing import Any, Never, Optional

from twitter_api.ratelimit.ratelimit_data import RatelimitData
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
        self.endpoint = endpoint
        self.expected_endpoint = expected_endpoint

    def __str__(self) -> str:
        return ErrorMessage(
            type=self.__class__.__name__,
            message=("出力したいレスポンスのエンドポイントが異なっています。"),
            **dict(
                expected_endpoint=self.expected_endpoint,
                endpoint=self.endpoint,
            ),
        ).to_message()


class TwitterApiResponseModelBodyDecodeError(TwitterApiError):
    def __init__(self, endpoint: Endpoint, content: bytes, **extra):
        self.endpoint = endpoint
        self.content = content
        self.extra = extra

    def __str__(self) -> str:
        return ErrorMessage(
            type=self.__class__.__name__,
            message="Twitter API の応答のボディを JSON でパースできませんでした。",
            **dict(endpoint=self.endpoint, content=self.content),
            **exclude_none(self.extra),
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
        self.endpoint = endpoint
        self.url = url
        self.request_headers = request_headers
        self.query = query
        self.request_body = request_body
        self.response_status_code = response_status_code
        self.response_body = response_body

    def __str__(self) -> str:
        return ErrorMessage(
            type=self.__class__.__name__,
            message="Twitter API の応答が 200 ではありません。",
            **OrderedDict(
                endpoint=self.endpoint,
                url=self.url,
                reqeust_headers=exclude_none(self.request_headers),
                query=exclude_none(self.query),
                request_body=exclude_none(self.request_body),
                response_status_code=self.response_status_code,
                response_body=(
                    exclude_none(self.response_body)
                    if not isinstance(self.response_body, bytes)
                    else self.response_body
                ),
            ),
        ).to_message()


class TwitterApiResponseError(TwitterApiError):
    def __init__(self, endpoint: Endpoint, data: Any, **extra):
        self.endpoint = endpoint
        self.data = data
        self.extra = extra

    def __str__(self) -> str:
        return ErrorMessage(
            type=self.__class__.__name__,
            message="Twitter API の応答でエラーが返りました。",
            **dict(
                endpoint=self.endpoint,
                data=exclude_none(self.data),
            ),
            **exclude_none(self.extra),
        ).to_message()


class TwitterApiOAuthTokenV1NotFound(TwitterApiError):
    def __init__(self, endpoint, data: Any, **extra):
        self.endpoint = endpoint
        self.data = data
        self.extra = extra

    def __str__(self) -> str:
        return ErrorMessage(
            type=self.__class__.__name__,
            message="OAuth V1 のトークンが見つかりませんでした。",
            **dict(
                endpoint=self.endpoint,
                data=exclude_none(self.data),
            ),
            **exclude_none(self.extra),
        ).to_message()


class TwitterApiOAuthVersionWrong(TwitterApiError):
    def __init__(self, *, version: OAuthVersion, expected_version: OAuthVersion):
        self.version = version
        self.expected_version = expected_version

    def __str__(self) -> str:
        return ErrorMessage(
            type=self.__class__.__name__,
            message=(
                f'OAuth のバージョンは "{self.version}" ではなく'
                f' "{self.expected_version}" である必要があります。'
            ),
        ).to_message()


class RatelimitOverError(TwitterApiError):
    def __init__(self, ratelimit: RatelimitData) -> None:
        self._ratelimit = ratelimit

    def __str__(self) -> str:
        return f"レートリミットを超えています。{self._ratelimit}"
