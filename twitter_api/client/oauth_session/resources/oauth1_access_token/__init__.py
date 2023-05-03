from typing_extensions import Literal

from twitter_api.types._generic_client import TwitterApiGenericClient

from .post_oauth1_access_token import PostOauth1AccessTokenResources

Oauth1AccessTokenUrl = Literal["https://api.twitter.com/oauth/access_token"]


class Oauth1AccessTokenResources(
    PostOauth1AccessTokenResources[TwitterApiGenericClient]
):
    pass
