import json
from abc import abstractmethod
from collections import OrderedDict
from enum import Enum
from textwrap import dedent
from typing import Any, Never, Optional

import pydantic

from twitter_api.rate_limit.types.rate_limit_info import RateLimitInfo
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel

from .types.endpoint import Endpoint
from .types.http import Headers, QuryParameters, RequestJsonBody, ResponseJsonBody
from .types.oauth import OAuthVersion
from .utils._functional import exclude_none


class TwitterApiExceptionInfo(ExtraPermissiveModel):
    type: str
    message: str
    erros: Optional[list[str]] = None


class TwitterApiException(Exception):
    ...

    @property
    @abstractmethod
    def message(self) -> str:
        ...

    @property
    def info(self) -> TwitterApiExceptionInfo:
        return TwitterApiExceptionInfo(
            type=self.__class__.__name__,
            message=self.message,
        )

    def __str__(self) -> str:
        return self.message


class TwitterApiError(TwitterApiException):
    ...


class TwitterApiErrorCode(Enum):
    """
    Twitter API が返してくるエラーコード。

    refer: https://developer.twitter.com/en/support/twitter-api/error-troubleshooting
    """

    OK = 200
    NotModified = 304
    BadRequest = 400
    Unauthorized = 401
    Forbidden = 403
    NotFound = 404
    NotAcceptable = 406
    ConnectionException = 409
    Gone = 410
    UnprocessableEntity = 422
    TooManyRequests = 429
    InternalServerError = 500
    BadGateway = 502
    ServiceUnavailable = 503
    GatewayTimeout = 504


class NeverError(TwitterApiError):
    def __init__(self, never: Never):
        self._never = never

    @property
    def message(self) -> str:
        return f'到達できないはずの入力 "{self._never}" が与えられました。'


class MockResponseNotFound(TwitterApiError):
    @property
    def message(self) -> str:
        return dedent(
            """
            モックとして出力したいデータが入力されていません。
            `client.inject_*(response)` で定義されているメソッドを用い、
            レスポンスデータを定義した後で、API を呼んでください。
            """
        )


class MockInjectionResponseWrong(TwitterApiError):
    def __init__(self, endpoint: Endpoint, expected_endpoint: Endpoint):
        self._endpoint = endpoint
        self._expected_endpoint = expected_endpoint

    @property
    def message(self) -> str:
        return "出力したいレスポンスのエンドポイントが異なっています。"

    @property
    def info(self) -> TwitterApiExceptionInfo:
        return TwitterApiExceptionInfo(
            type=self.__class__.__name__,
            message=self.message,
            **dict(
                expected_endpoint=self._expected_endpoint,
                endpoint=self._endpoint,
            ),
        )


class TwitterApiResponseModelBodyDecodeError(TwitterApiError):
    def __init__(self, endpoint: Endpoint, content: bytes, **extra):
        self._endpoint = endpoint
        self._content = content
        self._extra = extra

    @property
    def message(self) -> str:
        return "Twitter API の応答のボディを JSON でパースできませんでした。"

    @property
    def info(self) -> TwitterApiExceptionInfo:
        return TwitterApiExceptionInfo(
            type=self.__class__.__name__,
            message=self.message,
            **dict(endpoint=self._endpoint, content=self._content),
            **exclude_none(self._extra),
        )


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
        self.status_code = response_status_code
        self._response_body = response_body

    @property
    def message(self) -> str:
        match self.status_code:
            case TwitterApiErrorCode.OK.value:
                return "API が成功しています。"
            case TwitterApiErrorCode.NotModified.value:
                return "返却する新しいデータがありません。"
            case TwitterApiErrorCode.BadRequest.value:
                return "リクエストの形式が間違っています。"
            case TwitterApiErrorCode.Unauthorized.value:
                return "このリクエストは証認されていません。"
            case TwitterApiErrorCode.Forbidden.value:
                return "このリクエストは許可されていません。"
            case TwitterApiErrorCode.NotFound.value:
                return "データが見つかりません。"
            case TwitterApiErrorCode.NotAcceptable.value:
                return "アクセスできません。"
            case TwitterApiErrorCode.ConnectionException.value:
                return "接続に失敗しました。"
            case TwitterApiErrorCode.Gone.value:
                return "このリソースは利用できなくなりました。"
            case TwitterApiErrorCode.UnprocessableEntity.value:
                return "処理できないエンティティです。"
            case TwitterApiErrorCode.TooManyRequests.value:
                return "レートリミットか Tweet Cap が制限を超えました。"
            case TwitterApiErrorCode.InternalServerError.value:
                return "Twitter API の内部でエラーが発生しました。"
            case TwitterApiErrorCode.BadGateway.value:
                return "Twitter API がダウンしているか、アップグレード中です。"
            case TwitterApiErrorCode.ServiceUnavailable.value:
                return "リクエスト数が多く処理できません。後でもう一度お試しください。"
            case TwitterApiErrorCode.GatewayTimeout.value:
                return "Twitter API が内部的にダウンしています。後でもう一度お試しください。"
            case _:
                return "Twitter API の応答が 200 ではありません。"

    @property
    def info(self) -> TwitterApiExceptionInfo:
        return TwitterApiExceptionInfo(
            type=self.__class__.__name__,
            message=self.message,
            **OrderedDict(
                endpoint=self._endpoint,
                url=self._url,
                reqeust_headers=exclude_none(self._request_headers),
                query=exclude_none(self._query),
                request_body=exclude_none(self._request_body),
                response_status_code=self.status_code,
                response_body=(
                    exclude_none(self._response_body)
                    if not isinstance(self._response_body, bytes)
                    else self._response_body
                ),
            ),
        )


class OAuth2UserAccessTokenExpired(TwitterApiError):
    @property
    def message(self) -> str:
        return "OAuth2.0 のユーザ認証の ACCESS_TOKEN が失効しました。再度発行してください。"


class TwitterApiResponseError(TwitterApiError):
    def __init__(self, endpoint: Endpoint, data: Any, **extra):
        self._endpoint = endpoint
        self._data = data
        self._extra = extra

    @property
    def message(self) -> str:
        return "Twitter API の応答でエラーが返りました。"

    @property
    def info(self) -> TwitterApiExceptionInfo:
        return TwitterApiExceptionInfo(
            type=self.__class__.__name__,
            message=self.message,
            **dict(
                endpoint=self._endpoint,
                data=exclude_none(self._data),
            ),
            **exclude_none(self._extra),
        )


class TwitterApiResponseValidationError(TwitterApiError):
    def __init__(
        self, endpoint: Endpoint, response_body: Any, error: pydantic.ValidationError
    ):
        self._endpoint = endpoint
        self._response_body = response_body
        self._error = error

    @property
    def message(self) -> str:
        return "Twitter API の応答の型が想定とは一致していません。"

    @property
    def info(self) -> TwitterApiExceptionInfo:
        response_body = exclude_none(self._response_body)

        # 文字が長すぎる場合、切り取る。
        response_body_str = json.dumps(response_body, ensure_ascii=False)
        max_length = 1000
        if len(response_body_str) > max_length:
            response_body = response_body_str[: max_length - 3] + "..."

        return TwitterApiExceptionInfo(
            type=self.__class__.__name__,
            message=self.message,
            **dict(
                endpoint=self._endpoint,
                response_body=response_body,
                error=self._error.errors(),
            ),
        )


class TwitterApiOAuthTokenV1NotFound(TwitterApiError):
    def __init__(self, endpoint, data: Any, **extra):
        self._endpoint = endpoint
        self._data = data
        self._extra = extra

    @property
    def message(self) -> str:
        return "OAuth V1 のトークンが見つかりませんでした。"

    @property
    def info(self) -> TwitterApiExceptionInfo:
        return TwitterApiExceptionInfo(
            type=self.__class__.__name__,
            message=self.message,
            **dict(
                endpoint=self._endpoint,
                data=exclude_none(self._data),
            ),
            **exclude_none(self._extra),
        )


class TwitterApiOAuthVersionWrong(TwitterApiError):
    def __init__(self, *, version: OAuthVersion, expected_version: OAuthVersion):
        self._version = version
        self._expected_version = expected_version

    @property
    def message(self) -> str:
        return f'OAuth のバージョンは "{self._version}" ではなく "{self._expected_version}" である必要があります。'


class RateLimitOverError(TwitterApiError):
    def __init__(self, rate_limit: RateLimitInfo) -> None:
        self._rate_limit = rate_limit

    @property
    def message(self) -> str:
        return f"レートリミットを超えています。{self._rate_limit}"


class UnsupportedAuthenticationError(TwitterApiError):
    @property
    def message(self) -> str:
        return "この認証方法でのアクセスは許可されていません。"
