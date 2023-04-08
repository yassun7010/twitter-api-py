from dataclasses import dataclass
from typing import Optional

from authlib.integrations.requests_client.oauth2_session import OAuth2Session

from twitter_api.api.resources.oauth2_authorize import Oauth2AuthorizeUrl
from twitter_api.api.types.v2_oauth2.generate_authorization_url import (
    GenerateAuthorizationUrl,
)

from twitter_api.api.types.v2_scope import Scope
from twitter_api.rate_limit.manager.rate_limit_manager import RateLimitManager
from twitter_api.types.chainable import Chainable
from twitter_api.types.comma_separatable import CommaSeparatable
from twitter_api.types.http import Url
from twitter_api.types.oauth import ClientId, ClientSecret


@dataclass
class OAuthV2AuthorizeClient(Chainable):
    client_id: ClientId
    client_secret: ClientSecret
    callback_url: Url
    scope: CommaSeparatable[Scope]
    rate_limit_manager: Optional[RateLimitManager] = None

    def request(self, url: Oauth2AuthorizeUrl) -> GenerateAuthorizationUrl:
        session = OAuth2Session(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.callback_url,
            scope=self.scope,
            code_challenge_method="S256",
        )

        return GenerateAuthorizationUrl(url, session)
