from twitter_api.client.oauth_session.resources.oauth1_request_token import (
    OAuth1RequestTokenSessionResources,
    Oauth1RequestTokenUrl,
)
from twitter_api.client.oauth_session.twitter_oauth1_session import TwitterOAuth1Session
from twitter_api.types.chainable import Chainable


class TwitterOAuth1RequestTokenClient(Chainable):
    def __init__(self, session: TwitterOAuth1Session) -> None:
        self._session = session

    def resource(
        self, url: Oauth1RequestTokenUrl
    ) -> OAuth1RequestTokenSessionResources:
        return OAuth1RequestTokenSessionResources(
            self._session,
        )
