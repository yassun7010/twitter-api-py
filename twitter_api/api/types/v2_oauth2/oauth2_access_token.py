from dataclasses import dataclass

from typing_extensions import Literal

from twitter_api.api.types.v2_scope import Scope
from twitter_api.types.chainable import Chainable
from twitter_api.types.comma_separatable import CommaSeparatable
from twitter_api.types.oauth import AccessToken


@dataclass
class OAuth2AcccessToken(Chainable):
    token_type: Literal["bearer"]
    expires_in: int
    expires_at: int
    access_token: AccessToken
    scope: CommaSeparatable[Scope]

    def generate_client(self):
        from twitter_api.client.twitter_api_real_client import TwitterApiRealClient

        return TwitterApiRealClient.from_app_oauth2_bearer_token(self.access_token)
