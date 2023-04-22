from typing import Literal

from .generate_authorization_url_oauth_authenticate import (
    GenerateAuthorizationUrlOAuthAuthenticateSessionResources,
)

OauthAuthenticateUrl = Literal["https://api.twitter.com/oauth/authenticate"]


class OAuthAuthenticateSessionResources(
    GenerateAuthorizationUrlOAuthAuthenticateSessionResources,
):
    pass
