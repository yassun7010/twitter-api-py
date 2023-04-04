from typing_extensions import Literal

from .get_oauth_authenticate import OauthGetAuthenticate

OauthAuthenticateUrl = Literal["https://api.twitter.com/oauth/authenticate"]


class OauthRequestTokenResources(OauthGetAuthenticate):
    pass
