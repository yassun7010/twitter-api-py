from typing_extensions import Literal

from .post_oauth2_token import Oauth2PostTokenResources

Oauth2TokenUrl = Literal["https://api.twitter.com/oauth2/token"]


class Oauth2TokenResources(Oauth2PostTokenResources):
    pass
