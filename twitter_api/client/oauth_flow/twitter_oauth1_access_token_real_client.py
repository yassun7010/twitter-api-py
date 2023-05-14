from twitter_api.client.oauth_flow.twitter_oauth1_access_token_client import (
    TwitterOAuth1AccessTokenClient,
)
from twitter_api.types._generic_client import TwitterApiGenericRealClient


class TwitterOAuth1AccessTokenRealClient(
    TwitterOAuth1AccessTokenClient[TwitterApiGenericRealClient]
):
    pass
