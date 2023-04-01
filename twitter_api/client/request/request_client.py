from abc import abstractmethod
from typing import Generic, Optional, Type, TypeAlias

from authlib.integrations.requests_client.oauth1_session import (
    OAuth1Auth,  # pyright: reportMissingImports=false
)
from authlib.integrations.requests_client.oauth2_session import (
    OAuth2Auth,  # pyright: reportMissingImports=false
)

from twitter_api.types.endpoint import Endpoint
from twitter_api.types.http import (
    Headers,
    QuryParameters,
    RequestJsonBody,
    ResponseModelBody,
)

OAuth: TypeAlias = OAuth1Auth | OAuth2Auth


class RequestClient(Generic[QuryParameters, ResponseModelBody]):
    @abstractmethod
    def get(
        self,
        *,
        endpoint: Endpoint,
        response_type: Type[ResponseModelBody],
        uri: Optional[str] = None,
        auth: bool = True,
        query: Optional[QuryParameters] = None,
    ) -> ResponseModelBody:
        ...

    @abstractmethod
    def post(
        self,
        *,
        endpoint: Endpoint,
        response_type: Type[ResponseModelBody],
        uri: Optional[str] = None,
        auth: bool = True,
        headers: Optional[Headers] = None,
        query: Optional[QuryParameters] = None,
        body: Optional[RequestJsonBody] = None,
    ) -> ResponseModelBody:
        ...
