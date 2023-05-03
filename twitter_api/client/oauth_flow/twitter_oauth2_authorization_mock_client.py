from twitter_api.client.oauth_flow.twitter_oauth2_authorization_client import (
    TwitterOAuth2AuthorizeClient,
)
from twitter_api.types._generic_client import TwitterApiGenericMockClient


class TwitterOAuth2AuthorizeMockClient(
    TwitterOAuth2AuthorizeClient[TwitterApiGenericMockClient]
):
    pass
