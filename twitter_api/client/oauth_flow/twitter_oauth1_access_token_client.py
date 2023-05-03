from typing import Generic

from twitter_api.client.oauth_session.resources.oauth1_access_token import (
    Oauth1AccessTokenResources,
    Oauth1AccessTokenUrl,
)
from twitter_api.client.oauth_session.twitter_oauth1_session import TwitterOAuth1Session
from twitter_api.types._chainable import Chainable
from twitter_api.types._generic_client import TwitterApiGenericClient
from twitter_api.types.oauth import CallbackUrl


class TwitterOAuth1AccessTokenClient(Chainable, Generic[TwitterApiGenericClient]):
    def __init__(
        self,
        authorization_response_url: CallbackUrl,
        session: TwitterOAuth1Session[TwitterApiGenericClient],
    ):
        self.authorization_response_url = authorization_response_url
        self._session = session

    def request(
        self, url: Oauth1AccessTokenUrl
    ) -> Oauth1AccessTokenResources[TwitterApiGenericClient]:
        return Oauth1AccessTokenResources(
            session=self._session,
            authorization_response_url=self.authorization_response_url,
        )
