from typing_extensions import Literal

from .get_oauth_authorize import GetOauthAuthorizeResources

OauthAuthorizeUrl = Literal["https://api.twitter.com/oauth/authorize"]


class OauthAuthorizeResources(GetOauthAuthorizeResources):
    pass
