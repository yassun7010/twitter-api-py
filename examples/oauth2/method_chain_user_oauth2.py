import os
import sys

from twitter_api.client.twitter_api_client import TwitterApiClient
from twitter_api.error import TwitterApiError

YOUR_CALLBACK_URL = os.environ["CALLBACK_URL"]

try:
    with (
        TwitterApiClient.from_oauth2_user_flow_env(
            callback_url=YOUR_CALLBACK_URL,
            scope=[
                "tweet.read",
                "users.read",
            ],
        )
        .request("https://twitter.com/i/oauth2/authorize")
        .generate_authorization_url()
        .print_request_url()
        .input_response_url()
        .request("https://api.twitter.com/2/oauth2/token")
        .post()
        .generate_client()
    ) as client:
        tweets = (
            client.chain()
            .request("https://api.twitter.com/2/tweets")
            .get(
                {"ids": ["1460323737035677698"]},
            )
            .data
        )

        print(tweets)


except TwitterApiError as error:
    print(error.info.json(indent=2), file=sys.stderr)
