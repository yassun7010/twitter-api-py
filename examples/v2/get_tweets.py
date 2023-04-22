import sys

from twitter_api.client import TwitterApiClient
from twitter_api.error import TwitterApiError

try:
    client = TwitterApiClient.from_oauth2_app_env()

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
