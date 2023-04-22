from typing_extensions import Literal

from .post_oauth_request_token import (
    AsyncPostOauthRequestTokenResources,
    PostOauthRequestTokenResources,
)

OauthRequestTokenUrl = Literal["https://api.twitter.com/oauth/request_token"]


class OauthRequestTokenResources(PostOauthRequestTokenResources):
    pass


class AsyncOauthRequestTokenResources(AsyncPostOauthRequestTokenResources):
    pass
