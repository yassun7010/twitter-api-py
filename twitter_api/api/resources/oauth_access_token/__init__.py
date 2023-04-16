from typing_extensions import Literal

from .post_oauth_access_token import PostOauthAccessTokenResources

OauthAccessTokenUrl = Literal["https://api.twitter.com/oauth/access_token"]


class OauthAccessTokenResources(PostOauthAccessTokenResources):
    pass
