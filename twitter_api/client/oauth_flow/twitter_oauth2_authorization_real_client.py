from twitter_api.client.oauth_flow.twitter_oauth2_authorization_client import (
    TwitterOAuth2AuthorizeClient,
)
from twitter_api.types._generic_client import TwitterApiGenericRealClient


class TwitterOAuth2AuthorizeRealClient(
    TwitterOAuth2AuthorizeClient[TwitterApiGenericRealClient]
):
    pass
