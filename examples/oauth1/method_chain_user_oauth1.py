import os
import sys

from twitter_api.client import TwitterApiClient
from twitter_api.error import TwitterApiError

YOUR_CALLBACK_URL = os.environ["CALLBACK_URL"]


try:
    client = (
        TwitterApiClient.from_oauth1_user_flow_env()
        .resource("https://api.twitter.com/oauth/request_token")
        .post()
        .resource("https://api.twitter.com/oauth/authorize")
        .generate_authorization_url()
        .open_request_url()
        .input_response_url()
        .resource("https://api.twitter.com/oauth/access_token")
        .post()
        .generate_client()
    )

    tweets = (
        client.chain()
        .resource("https://api.twitter.com/2/tweets")
        .get(
            {"ids": ["1460323737035677698"]},
        )
        .data
    )

    print(tweets)


except TwitterApiError as error:
    print(error, file=sys.stderr)