from typing_extensions import Literal

from .post_oauth1_request_token import PostOAuth1RequestTokenSessionResources

Oauth1RequestTokenUrl = Literal["https://api.twitter.com/oauth/request_token"]


class OAuth1RequestTokenSessionResources(PostOAuth1RequestTokenSessionResources):
    pass
