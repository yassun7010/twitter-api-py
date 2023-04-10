import pytest

from tests.conftest import synthetic_monitoring_is_disable
from twitter_api.api.resources.v2_tweets.get_v2_tweets import GetV2TweetsResponseBody
from twitter_api.api.types.v2_expansion import Expansion
from twitter_api.api.types.v2_media.media_field import MediaField
from twitter_api.api.types.v2_place.place_field import PlaceField
from twitter_api.api.types.v2_poll.poll_field import PollField
from twitter_api.api.types.v2_tweet.tweet_detail import TweetDetail
from twitter_api.api.types.v2_tweet.tweet_field import TweetField
from twitter_api.api.types.v2_user.user_field import UserField
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient
from twitter_api.types.extra_permissive_model import get_extra_fields


@pytest.fixture
def tweets(intro_tweet: TweetDetail) -> list[TweetDetail]:
    return [intro_tweet]


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestGetV2Tweets:
    def test_get_v2_tweets(
        self,
        real_oauth2_app_client: TwitterApiRealClient,
        tweets: list[TweetDetail],
    ):
        expected_response = GetV2TweetsResponseBody(data=tweets)
        response = (
            real_oauth2_app_client.chain()
            .request("https://api.twitter.com/2/tweets")
            .get({"ids": list(map(lambda tweet: tweet.id, tweets))})
        )

        print(response.json())
        print(expected_response.json())

        assert get_extra_fields(response) == {}
        assert response == expected_response

    def test_get_v2_tweet_all_query(
        self,
        real_oauth2_app_client: TwitterApiRealClient,
        tweets: list[TweetDetail],
        all_expansions: list[Expansion],
        all_media_fields: list[MediaField],
        all_place_fields: list[PlaceField],
        all_poll_fields: list[PollField],
        all_tweet_fields: list[TweetField],
        all_user_fields: list[UserField],
    ):
        response = (
            real_oauth2_app_client.chain()
            .request("https://api.twitter.com/2/tweets")
            .get(
                {
                    "ids": list(map(lambda tweet: tweet.id, tweets)),
                    "expansions": all_expansions,
                    "media.fields": all_media_fields,
                    "place.fields": all_place_fields,
                    "poll.fields": all_poll_fields,
                    "tweet.fields": all_tweet_fields,
                    "user.fields": all_user_fields,
                }
            )
        )

        print(response.json())

        assert get_extra_fields(response) == {}


class TestMockGetV2Tweets:
    def test_mock_get_v2_tweets(self, mock_oauth2_app_client: TwitterApiMockClient):
        tweet = TweetDetail(
            id="12345",
            text="tweet",
            edit_history_tweet_ids=["56789"],
        )

        response = GetV2TweetsResponseBody(data=[tweet for _ in range(10)])

        assert (
            mock_oauth2_app_client.chain()
            .inject_get_response_body("https://api.twitter.com/2/tweets", response)
            .request("https://api.twitter.com/2/tweets")
            .get(
                {
                    "ids": "1460323737035677698",
                    "expansions": ["attachments.media_keys"],
                }
            )
        ) == response
