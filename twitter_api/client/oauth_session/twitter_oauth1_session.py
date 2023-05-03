from abc import ABCMeta, abstractmethod
from typing import Generic, cast

from twitter_api.types._generic_client import TwitterApiGenericClient
from twitter_api.types.http import Url
from twitter_api.types.oauth import CallbackUrl


class TwitterOAuth1Session(Generic[TwitterApiGenericClient], metaclass=ABCMeta):
    @abstractmethod
    def request_token(self):
        from twitter_api.client.oauth_flow.twitter_oauth1_authorization_client import (
            TwitterOAuth1AuthorizeClient,
        )

        return cast(TwitterOAuth1AuthorizeClient[TwitterApiGenericClient], ...)

    @abstractmethod
    def generate_authorization_url(
        self,
        url: Url,
    ):
        from twitter_api.types.oauth1.oauth1_authorization import OAuth1Authorization

        return cast(OAuth1Authorization[TwitterApiGenericClient], ...)

    @abstractmethod
    def fetch_token(
        self,
        authorization_response_url: CallbackUrl,
    ):
        from twitter_api.types.oauth1.oauth1_access_token import OAuth1AccessToken

        return cast(OAuth1AccessToken[TwitterApiGenericClient], ...)
