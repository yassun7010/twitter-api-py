import sys

from twitter_api.client.twitter_api_client import TwitterApiClient
from twitter_api.error import TwitterApiError

if len(sys.argv) == 1:
    sys.stderr.write("Please input username: ")
    username = input()
elif len(sys.argv) == 2:
    username = sys.argv[1]
else:
    print("Usage: python get_user_id_by_username.py [USER_ID]", file=sys.stderr)
    sys.exit(1)

try:
    with TwitterApiClient.from_oauth2_app_env() as client:
        user = (
            client.chain()
            .request("https://api.twitter.com/2/users/by/username/:username")
            .get(username)
            .data
        )

        print(user.id)

except TwitterApiError as error:
    print(error.info.json(indent=2), file=sys.stderr)
