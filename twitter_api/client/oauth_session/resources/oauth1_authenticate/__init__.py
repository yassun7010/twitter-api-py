from typing import Literal

from .generate_authorization_url_oauth1_authenticate import (
    GenerateAuthorizationUrlOAuth1AuthenticateSessionResources,
)

OauthAuth1enticateUrl = Literal["https://api.twitter.com/oauth/authenticate"]


class OAuth1AuthenticateSessionResources(
    GenerateAuthorizationUrlOAuth1AuthenticateSessionResources,
):
    pass
