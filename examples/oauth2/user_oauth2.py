import sys

from twitter_api.client import TwitterApiClient
from twitter_api.error import TwitterApiError

YOUR_CALLBACK_URL = "https://127.0.0.1:3000/"

try:
    access_token = (
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
        .access_token
    )

    client = TwitterApiClient.from_oauth2_bearer_token(access_token)

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
