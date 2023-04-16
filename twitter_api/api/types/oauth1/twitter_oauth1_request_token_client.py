from twitter_api.api.resources.oauth_request_token import OauthRequestTokenUrl
from twitter_api.api.types.oauth1.oauth1_request_token_session_resource import (
    PostOAuth1RequestTokenSessionResources,
)
from twitter_api.client.oauth_session.twitter_oauth1_session import TwitterOAuth1Session
from twitter_api.types.chainable import Chainable


class TwitterOAuth1RequestTokenClient(Chainable):
    def __init__(self, session: TwitterOAuth1Session) -> None:
        self._session = session

    def request(
        self, url: OauthRequestTokenUrl
    ) -> PostOAuth1RequestTokenSessionResources:
        return PostOAuth1RequestTokenSessionResources(
            self._session,
        )
