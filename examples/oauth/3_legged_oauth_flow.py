import os
import sys

from twitter_api.client import TwitterApiClient
from twitter_api.error import TwitterApiError

YOUR_CALLBACK_URL = os.environ["CALLBACK_URL"]


try:
    token = (
        TwitterApiClient.from_oauth1_user_flow_env()
        .request("https://api.twitter.com/oauth/request_token")
        .post()
        .request("https://api.twitter.com/oauth/authorize")
        .generate_authorization_url()
        .print_request_url()
        .input_response_url()
        .request("https://api.twitter.com/oauth/access_token")
        .post()
    )

    client = TwitterApiClient.from_oauth1_app(
        api_key=os.environ["API_KEY"],
        api_secret=os.environ["API_SECRET"],
        access_token=token.oauth_token,
        access_secret=token.oauth_token_secret,
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
