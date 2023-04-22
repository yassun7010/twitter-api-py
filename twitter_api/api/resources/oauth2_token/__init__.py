from typing_extensions import Literal

from .post_oauth2_token import AsyncPostOauth2TokenResources, PostOauth2TokenResources

Oauth2TokenUrl = Literal["https://api.twitter.com/oauth2/token"]


class Oauth2TokenResources(PostOauth2TokenResources):
    pass


class AsyncOauth2TokenResources(AsyncPostOauth2TokenResources):
    pass
