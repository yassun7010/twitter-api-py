from typing import Literal

from .generate_authorization_url_oauth1_authorize import (
    GenerateAuthorizationUrlOAuth1AuthorizeSessionResources,
)

Oauth1AuthorizeUrl = Literal["https://api.twitter.com/oauth/authorize"]


class OAuth1AuthorizeSessionResources(
    GenerateAuthorizationUrlOAuth1AuthorizeSessionResources,
):
    pass
