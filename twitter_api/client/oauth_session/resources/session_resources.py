from typing import Generic

from twitter_api.client.oauth_session.twitter_oauth1_session import TwitterOAuth1Session
from twitter_api.client.oauth_session.twitter_oauth2_session import TwitterOAuth2Session
from twitter_api.types._generic_client import TwitterApiGenericClient


class OAuth1SessionResources(Generic[TwitterApiGenericClient]):
    def __init__(self, session: TwitterOAuth1Session[TwitterApiGenericClient]) -> None:
        self._session = session


class OAuth2SessionResources(Generic[TwitterApiGenericClient]):
    def __init__(self, session: TwitterOAuth2Session[TwitterApiGenericClient]) -> None:
        self._session = session
