from typing_extensions import Literal

from .post_oauth2_invalidate_token import PostOauth2InvalidateTokenResources

Oauth2InvalidateTokenUrl = Literal["https://api.twitter.com/oauth2/invalidate_token"]


class Oauth2InvalidateTokenResources(PostOauth2InvalidateTokenResources):
    pass
