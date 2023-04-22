from typing_extensions import Literal

from .get_oauth_authenticate import AsyncGetOauthAuthenticate, GetOauthAuthenticate

OauthAuthenticateUrl = Literal["https://api.twitter.com/oauth/authenticate"]


class OauthRequestTokenResources(GetOauthAuthenticate):
    pass


class AsyncOauthRequestTokenResources(AsyncGetOauthAuthenticate):
    pass
