from typing_extensions import Literal

from .post_oauth2_token import PostOauth2TokenResources

Oauth2TokenUrl = Literal["https://api.twitter.com/oauth2/token"]


class Oauth2TokenResources(PostOauth2TokenResources):
    pass
