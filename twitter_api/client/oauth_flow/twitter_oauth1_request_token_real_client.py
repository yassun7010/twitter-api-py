from twitter_api.client.oauth_flow.twitter_oauth1_request_token_client import (
    TwitterOAuth1RequestTokenClient,
)
from twitter_api.types._generic_client import TwitterApiGenericRealClient


class TwitterOAuth1RequestTokenRealClient(
    TwitterOAuth1RequestTokenClient[TwitterApiGenericRealClient]
):
    pass
