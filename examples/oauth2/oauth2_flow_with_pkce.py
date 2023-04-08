import sys

from twitter_api.client import TwitterApiClient
from twitter_api.error import TwitterApiError

YOUR_CALLBACK_URL = "https://127.0.0.1:3000/"

try:
    client = (
        TwitterApiClient.from_user_oauth2_flow_env(
            callback_url=YOUR_CALLBACK_URL,
            scope=[
                "tweet.read",
                "users.read",
            ],
        )
        .chain()
        .request("https://twitter.com/i/oauth2/authorize")
        .open_request_url()
        .input_response_url()
        .request("https://api.twitter.com/2/oauth2/token")
        .post()
        .generate_client()
    )

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
    print(error, file=sys.stderr)
