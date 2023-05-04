import sys
from datetime import datetime, timedelta

from twitter_api import TwitterApiClient
from twitter_api.error import TwitterApiError
from twitter_api.types.v2_media.media_field import ALL_MEDIA_FIELDS
from twitter_api.types.v2_place.place_field import ALL_PLACE_FIELDS
from twitter_api.types.v2_poll.poll_field import ALL_POLL_FIELDS
from twitter_api.types.v2_search_query.search_query import SearchQuery
from twitter_api.types.v2_tweet.tweet_expansion import ALL_TWEET_EXPANSIONS
from twitter_api.types.v2_tweet.tweet_field import ALL_PUBLIC_TWEET_FIELDS
from twitter_api.types.v2_user.user_field import ALL_USER_FIELDS

try:
    with TwitterApiClient.from_oauth2_app_env() as client:
        response_body = (
            client.chain()
            .request("https://api.twitter.com/2/tweets/search/recent")
            .get(
                {
                    "query": SearchQuery.build(
                        lambda q: (
                            q.keyword("day")
                            & q.group(
                                q.hashtag("#Twitter") | q.hashtag("Xcorp"),
                            )
                            & q.mention("@elonmusk")
                            & ~q.mention("SpaceX")
                            & q.is_retweet()
                        )
                    ),
                    "start_time": datetime.now() - timedelta(hours=2),
                    "end_time": datetime.now(),
                    "expansions": ALL_TWEET_EXPANSIONS,
                    "media.fields": ALL_MEDIA_FIELDS,
                    "place.fields": ALL_PLACE_FIELDS,
                    "poll.fields": ALL_POLL_FIELDS,
                    "tweet.fields": ALL_PUBLIC_TWEET_FIELDS,
                    "user.fields": ALL_USER_FIELDS,
                },
            )
        )

        if len(response_body.data) == 0:
            exit(0)

        # Find Mentioned Users
        for user in response_body.find_mentioned_users_by(response_body.data[-1]):
            print(user.json(indent=2))

except TwitterApiError as error:
    print(error.info.json(indent=2), file=sys.stderr)
