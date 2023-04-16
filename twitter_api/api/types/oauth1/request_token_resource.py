from twitter_api.api.types.oauth1.oauth1_request_token import OAuth1RequestToken
from twitter_api.api.types.oauth1.twitter_oauth1_authorization_client import (
    TwitterOAuth1AuthorizeClient,
)
from twitter_api.client.oauth_session.twitter_oauth1_session import TwitterOAuth1Session


class PostOAuthRequestTokenResources:
    def __init__(self, session: TwitterOAuth1Session) -> None:
        self._session = session

    def post(self) -> TwitterOAuth1AuthorizeClient:
        return self._session.request_token()
