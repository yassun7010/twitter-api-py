from typing_extensions import Literal

from .post_invalidate_token import Oauth2PostInvalidateTokenResources

Oauth2InvalidateTokenUrl = Literal["https://api.twitter.com/oauth2/invalidate_token"]


class Oauth2InvalidateTokenResources(Oauth2PostInvalidateTokenResources):
    pass
