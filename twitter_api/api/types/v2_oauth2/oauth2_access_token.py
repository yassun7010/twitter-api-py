from typing_extensions import Literal

from twitter_api.api.types.v2_scope import Scope
from twitter_api.types.chainable import Chainable
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.oauth import AccessToken


class OAuth2AcccessToken(Chainable, ExtraPermissiveModel):
    token_type: Literal["bearer"]
    expires_in: int
    expires_at: int
    access_token: AccessToken
    scope: list[Scope]

    def generate_client(self):
        from twitter_api.client.twitter_api_real_client import TwitterApiRealClient

        return TwitterApiRealClient.from_app_oauth2_bearer_token(self.access_token)
