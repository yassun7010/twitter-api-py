from typing import Generic

from typing_extensions import Literal

from twitter_api.client.oauth_session.twitter_oauth2_session import TwitterOAuth2Session
from twitter_api.types.chainable import Chainable
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.generic_client import TwitterApiGenericClient
from twitter_api.types.oauth import AccessToken
from twitter_api.types.v2_scope import Scope


class OAuth2AccessToken(
    Chainable, ExtraPermissiveModel, Generic[TwitterApiGenericClient]
):
    token_type: Literal["bearer"]
    expires_in: int
    expires_at: int
    access_token: AccessToken
    scope: list[Scope]
    _session: TwitterOAuth2Session[TwitterApiGenericClient]

    def generate_client(self) -> TwitterApiGenericClient:
        return self._session.generate_client(self.access_token)
