import sys

from twitter_api.client import TwitterApiClient
from twitter_api.error import TwitterApiError

client = TwitterApiClient.from_app_auth_env()

try:
    tweets = client.request("/2/tweets").get(
        {"ids": ["1460323737035677698"]},
    )
    print(tweets)

except TwitterApiError as error:
    print(error, file=sys.stderr)
