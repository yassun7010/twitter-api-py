from abc import ABCMeta, abstractmethod
from typing import Generic

from twitter_api.types.generic_client import TwitterApiGenericClient
from twitter_api.types.oauth import AccessToken, CallbackUrl


class TwitterOAuth2Session(Generic[TwitterApiGenericClient], metaclass=ABCMeta):
    @abstractmethod
    def generate_authorization_url(
        self,
    ):
        from twitter_api.types.oauth2.oauth2_authorization import OAuth2Authorization

        _: OAuth2Authorization[TwitterApiGenericClient] = ...  # type: ignore

        return _

    @abstractmethod
    def fetch_token(
        self,
        authorization_response_url: CallbackUrl,
        state: str,
        code_verifier: str,
    ):
        from twitter_api.types.oauth2.oauth2_access_token import OAuth2AccessToken

        _: OAuth2AccessToken[TwitterApiGenericClient] = ...  # type: ignore

        return _

    @abstractmethod
    def generate_client(self, access_token: AccessToken) -> TwitterApiGenericClient:
        ...
