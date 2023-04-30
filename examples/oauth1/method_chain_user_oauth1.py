import os
import sys

from twitter_api import TwitterApiClient
from twitter_api.error import TwitterApiError

YOUR_CALLBACK_URL = os.environ["CALLBACK_URL"]


try:
    with (
        TwitterApiClient.from_oauth1_user_flow_env()
        .request("https://api.twitter.com/oauth/request_token")
        .post()
        .request("https://api.twitter.com/oauth/authorize")
        .generate_authorization_url()
        .print_request_url()
        .input_response_url()
        .request("https://api.twitter.com/oauth/access_token")
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
