from typing_extensions import Literal

from .get_oauth_authorize import OauthGetAuthorizeResources

OauthAuthorizeUrl = Literal["https://api.twitter.com/oauth/authorize"]


class OauthAuthorizeResources(OauthGetAuthorizeResources):
    pass
