from twitter_api.client.oauth_flow.twitter_oauth1_request_token_client import (
    TwitterOAuth1RequestTokenClient,
)
from twitter_api.types._generic_client import TwitterApiGenericMockClient


class TwitterOAuth1RequestTokenMockClient(
    TwitterOAuth1RequestTokenClient[TwitterApiGenericMockClient]
):
    pass
