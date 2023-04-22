from typing_extensions import Literal

from .get_oauth_authorize import (
    AsyncGetOauthAuthorizeResources,
    GetOauthAuthorizeResources,
)

OauthAuthorizeUrl = Literal["https://api.twitter.com/oauth/authorize"]


class OauthAuthorizeResources(GetOauthAuthorizeResources):
    pass


class AsyncOauthAuthorizeResources(AsyncGetOauthAuthorizeResources):
    pass
