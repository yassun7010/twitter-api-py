from abc import ABCMeta, abstractmethod
from typing import Generic, cast

from twitter_api.types._generic_client import TwitterApiGenericClient
from twitter_api.types.oauth import CallbackUrl


class TwitterOAuth2Session(Generic[TwitterApiGenericClient], metaclass=ABCMeta):
    @abstractmethod
    def generate_authorization_url(
        self,
    ):
        from twitter_api.types.oauth2.oauth2_authorization import OAuth2Authorization

        return cast(OAuth2Authorization[TwitterApiGenericClient], ...)

    @abstractmethod
    def fetch_token(
        self,
        authorization_response_url: CallbackUrl,
        state: str,
        code_verifier: str,
    ):
        from twitter_api.types.oauth2.oauth2_access_token import OAuth2AccessToken

        return cast(OAuth2AccessToken[TwitterApiGenericClient], ...)
