from typing import TypeAlias

from typing_extensions import Literal

from twitter_api.types._generic_client import TwitterApiGenericClient

from .post_v2_oauth2_token import PostV2OAuth2TokenRerources

V2Oauth2TokenUrl: TypeAlias = Literal["https://api.twitter.com/2/oauth2/token"]


class V2OAuth2TokenRerources(PostV2OAuth2TokenRerources[TwitterApiGenericClient]):
    pass
