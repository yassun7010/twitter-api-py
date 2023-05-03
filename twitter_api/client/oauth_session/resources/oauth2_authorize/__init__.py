from typing_extensions import Literal

from twitter_api.client.oauth_session.resources.oauth2_authorize.generate_authorization_url_oauth2_authorize import (
    GenerateAuthorizationUrlOAuth2AuthorizeSessionResources,
)
from twitter_api.types._generic_client import TwitterApiGenericClient

Oauth2AuthorizeUrl = Literal["https://twitter.com/i/oauth2/authorize"]


class OAuth2AuthorizeSessionResources(
    GenerateAuthorizationUrlOAuth2AuthorizeSessionResources[TwitterApiGenericClient],
):
    pass
