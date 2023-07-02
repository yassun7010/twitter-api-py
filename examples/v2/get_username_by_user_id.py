import sys

from twitter_api import TwitterApiClient
from twitter_api.error import TwitterApiError

if len(sys.argv) == 1:
    sys.stderr.write("Please input user id: ")
    user_id = input()
elif len(sys.argv) == 2:
    user_id = sys.argv[1]
else:
    print("Usage: python get_user_name_by_user_id.py [USER_ID]", file=sys.stderr)
    sys.exit(1)

try:
    with TwitterApiClient.from_oauth2_app_env() as client:
        user = (
            client.chain()
            .request("https://api.twitter.com/2/users/:id")
            .get(user_id)
            .data
        )

        print(user.username)

except TwitterApiError as error:
    print(error.info.model_dump_json(indent=2), file=sys.stderr)
