from twitter_api.client.oauth_flow.twitter_oauth2_access_token_client import (
    TwitterOAuth2AccessTokenClient,
)
from twitter_api.types._generic_client import TwitterApiGenericRealClient


class TwitterOAuth2AccessTokenRealClient(
    TwitterOAuth2AccessTokenClient[TwitterApiGenericRealClient]
):
    pass
