import sys

from twitter_api.client import TwitterApiClient
from twitter_api.error import TwitterApiError

client = TwitterApiClient.from_app_auth_env()

try:
    token = client.request("/oauth/request_token").post(
        {"oauth_callback": "https://120.0.0.1:8080"}
    )

except TwitterApiError as error:
    print(error, file=sys.stderr)
