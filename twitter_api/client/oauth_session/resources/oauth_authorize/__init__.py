from typing import Literal

from .generate_authorization_url_oauth_authorize import (
    GenerateAuthorizationUrlOAuthAuthorizeSessionResources,
)

OauthAuthorizeUrl = Literal["https://api.twitter.com/oauth/authorize"]


class OAuthAuthorizeSessionResources(
    GenerateAuthorizationUrlOAuthAuthorizeSessionResources,
):
    pass
