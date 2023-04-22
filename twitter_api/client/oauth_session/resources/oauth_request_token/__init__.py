from typing_extensions import Literal

from .post_oauth_request_token import PostOAuth1RequestTokenSessionResources

OauthRequestTokenUrl = Literal["https://api.twitter.com/oauth/request_token"]


class OAuth1RequestTokenSessionResources(PostOAuth1RequestTokenSessionResources):
    pass
