from typing_extensions import Literal

from .get_authenticate import OauthGetAuthenticate

OauthAuthenticateUrl = Literal["https://api.twitter.com/oauth/authenticate"]


class OauthRequestTokenResources(OauthGetAuthenticate):
    pass
