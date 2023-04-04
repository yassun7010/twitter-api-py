from typing_extensions import Literal

from .get_authorize import OauthGetAuthorize

OauthAuthorizeUrl = Literal["https://api.twitter.com/oauth/authorize"]


class OauthRequestTokenResources(OauthGetAuthorize):
    pass
