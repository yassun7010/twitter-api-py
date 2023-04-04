from typing_extensions import Literal

from .post_request_token import OauthPostRequestToken

OauthRequestTokenUrl = Literal["https://api.twitter.com/oauth/request_token"]


class OauthRequestTokenResources(OauthPostRequestToken):
    pass
