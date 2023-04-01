import base64
from typing import Literal, Optional, Type, Union

import requests
from authlib.integrations.requests_client.oauth1_session import (
    OAuth1Auth,  # pyright: reportMissingImports=false
)
from authlib.integrations.requests_client.oauth2_session import (
    OAuth2Auth,  # pyright: reportMissingImports=false
)

from twitter_api.error import (
    TwitterApiOAuthTokenV1NotFound,
    TwitterApiResponseError,
    TwitterApiResponseFailed,
    TwitterApiResponseModelBodyDecodeError,
)
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.oauth import AccessToken, ConsumerKey, ConsumerSecret
from twitter_api.utils.ratelimit import RateLimitTarget

from .request_client import (
    Headers,
    QuryParameters,
    RequestClient,
    RequestModelBody,
    ResponseModelBody,
)

TWITTER_API_DOMAIN = "https://api.twitter.com"


class RealRequestClient(RequestClient):
    def __init__(
        self,
        *,
        rate_limit: RateLimitTarget,
        auth: Union[OAuth1Auth, OAuth2Auth],
        session: Optional[requests.Session] = None,
        timeout_sec: Optional[float] = None,
    ) -> None:
        if session is None:
            session = requests.Session()

        self._rate_limit: RateLimitTarget = rate_limit
        self._auth = auth
        self._session = session
        self.timeout_sec = timeout_sec

    def get(
        self,
        *,
        endpoint: Endpoint,
        response_type: Type[ResponseModelBody],
        uri: Optional[str] = None,
        headers: Optional[Headers] = None,
        query: Optional[QuryParameters] = None,
        body: Optional[RequestModelBody] = None,
    ) -> ResponseModelBody:
        url = _make_twitter_api_url(endpoint, uri)

        response = self._session.request(
            url=url,
            auth=self._auth,
            method=endpoint.method,
            params=query,
            timeout=self.timeout_sec,
        )

        return response_type(
            **_parse_response(
                endpoint,
                response,
                url,
                headers,
                query,
                body,
            )
        )

    def post(
        self,
        *,
        endpoint: Endpoint,
        response_type: Type[ResponseModelBody],
        uri: Optional[str] = None,
        headers: Optional[Headers] = None,
        query: Optional[QuryParameters] = None,
        body: Optional[RequestModelBody] = None,
    ) -> ResponseModelBody:
        url = _make_twitter_api_url(endpoint, uri)

        response = self._session.request(
            url=url,
            auth=self._auth,
            method=endpoint.method,
            headers=headers,
            params=query,
            data=body.dict() if body is not None else None,
            timeout=self.timeout_sec,
        )

        if response_type is str:
            return response.content.decode("utf-8")  # type: ignore

        return response_type(
            **_parse_response(
                endpoint,
                response,
                url,
                headers,
                query,
                body,
            )
        )


def _make_twitter_api_url(
    endpoint: Endpoint, uri: Optional[str] = None
) -> str:
    if uri is None:
        return f"{TWITTER_API_DOMAIN}{endpoint.uri}"
    else:
        return f"{TWITTER_API_DOMAIN}{uri}"


def _parse_response(
    endpoint: Endpoint,
    response: requests.Response,
    url: str,
    headers: Optional[Headers] = None,
    query: Optional[QuryParameters] = None,
    body: Optional[RequestModelBody] = None,
) -> dict:
    try:
        data: dict = response.json()
    except ValueError:
        raise TwitterApiResponseModelBodyDecodeError(
            endpoint,
            response.content,
        )

    if not response.ok:
        raise TwitterApiResponseFailed(
            endpoint,
            url=url,
            request_headers=headers,
            request_query=query,
            request_body=body.dict() if body is not None else None,
            response_status_code=response.status_code,
            response_body=data,
        )

    # If only errors will raise
    if "errors" in data and len(data.keys()) == 1:
        raise TwitterApiResponseError(
            endpoint,
            data,
        )

    # v1 token not
    if "reason" in data:
        raise TwitterApiOAuthTokenV1NotFound(
            endpoint,
            data,
        )

    return data


class BearerTokenResponseBody(ExtraPermissiveModel):
    token_type: Literal["bearer"]
    access_token: AccessToken


def generate_bearer_token(
    consumer_key: ConsumerKey,
    consumer_secret: ConsumerSecret,
) -> BearerTokenResponseBody:
    bearer_token = base64.b64encode(
        f"{consumer_key}:{consumer_secret}".encode()
    )
    endpoint = Endpoint("POST", "/oauth2/token")
    url = f"{TWITTER_API_DOMAIN}{endpoint.uri}"
    resp = requests.post(
        url=url,
        headers={
            "Authorization": f"Basic {bearer_token.decode()}",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        },
        data={"grant_type": "client_credentials"},
    )

    return BearerTokenResponseBody(**_parse_response(endpoint, resp, url))
