from twitter_api.client.oauth_flow.twitter_oauth1_authorization_client import (
    TwitterOAuth1AuthorizeClient,
)
from twitter_api.types._generic_client import TwitterApiGenericMockClient


class TwitterOAuth1AuthorizeMockClient(
    TwitterOAuth1AuthorizeClient[TwitterApiGenericMockClient]
):
    pass
