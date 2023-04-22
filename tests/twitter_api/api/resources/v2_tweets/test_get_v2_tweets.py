import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.contexts.spawn_real_client import spawn_real_client
from tests.data import json_test_data
from twitter_api.api.resources.v2_tweets.get_v2_tweets import (
    GetV2TweetsQueryParameters,
    GetV2TweetsResponseBody,
)
from twitter_api.api.types.v2_expansion import Expansion
from twitter_api.api.types.v2_media.media_field import MediaField
from twitter_api.api.types.v2_place.place_field import PlaceField
from twitter_api.api.types.v2_poll.poll_field import PollField
from twitter_api.api.types.v2_tweet.tweet import Tweet
from twitter_api.api.types.v2_tweet.tweet_field import TweetField
from twitter_api.api.types.v2_user.user_field import UserField
from twitter_api.client.twitter_api_async_mock_client import TwitterApiAsyncMockClient
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient
from twitter_api.types.extra_permissive_model import get_extra_fields


@pytest.fixture
def tweets(intro_tweet: Tweet) -> list[Tweet]:
    return [intro_tweet]


@pytest.fixture
def all_fields(
    tweets: list[Tweet],
    all_expansions: list[Expansion],
    all_media_fields: list[MediaField],
    all_place_fields: list[PlaceField],
    all_poll_fields: list[PollField],
    all_tweet_fields: list[TweetField],
    all_user_fields: list[UserField],
) -> GetV2TweetsQueryParameters:
    return {
        "ids": list(map(lambda tweet: tweet.id, tweets)),
        "expansions": all_expansions,
        "media.fields": all_media_fields,
        "place.fields": all_place_fields,
        "poll.fields": all_poll_fields,
        "tweet.fields": all_tweet_fields,
        "user.fields": all_user_fields,
    }


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestGetV2Tweets:
    @pytest.mark.parametrize(
        "client_fixture_name,permit",
        [
            ("real_oauth1_app_client", True),
            ("real_oauth1_user_client", True),
            ("real_oauth2_app_client", True),
            ("real_oauth2_user_client", True),
        ],
    )
    def test_get_v2_tweets(
        self,
        tweets: list[Tweet],
        client_fixture_name: str,
        permit: bool,
        request: pytest.FixtureRequest,
    ):
        with spawn_real_client(client_fixture_name, request, permit) as real_client:
            expected_response = GetV2TweetsResponseBody(data=tweets)

            response = (
                real_client.chain()
                .resource("https://api.twitter.com/2/tweets")
                .get({"ids": list(map(lambda tweet: tweet.id, tweets))})
            )

            print(response.json())
            print(expected_response.json())

            assert get_extra_fields(response) == {}
            assert response == expected_response

    def test_get_v2_tweet_all_fields(
        self,
        real_oauth2_app_client: TwitterApiRealClient,
        all_fields: GetV2TweetsQueryParameters,
    ):
        response = (
            real_oauth2_app_client.chain()
            .resource("https://api.twitter.com/2/tweets")
            .get(all_fields)
        )

        print(response.json())

        assert get_extra_fields(response) == {}


class TestMockGetV2Tweets:
    @pytest.mark.parametrize(
        "json_filename",
        [
            "get_v2_tweets_response_all_fields.json",
        ],
    )
    def test_mock_get_v2_tweets(
        self,
        mock_oauth2_app_client: TwitterApiMockClient,
        all_fields: GetV2TweetsQueryParameters,
        json_filename: str,
    ):
        response = GetV2TweetsResponseBody.parse_file(
            json_test_data(json_filename),
        )

        assert (
            mock_oauth2_app_client.chain()
            .inject_get_response_body("https://api.twitter.com/2/tweets", response)
            .resource("https://api.twitter.com/2/tweets")
            .get(all_fields)
        ) == response

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "json_filename",
        [
            "get_v2_tweets_response_all_fields.json",
        ],
    )
    async def test_async_mock_get_v2_tweets(
        self,
        mock_oauth2_app_async_client: TwitterApiAsyncMockClient,
        all_fields: GetV2TweetsQueryParameters,
        json_filename: str,
    ):
        response = GetV2TweetsResponseBody.parse_file(
            json_test_data(json_filename),
        )

        assert (
            await (
                mock_oauth2_app_async_client.chain()
                .inject_get_response_body("https://api.twitter.com/2/tweets", response)
                .resource("https://api.twitter.com/2/tweets")
                .get(all_fields)
            )
            == response
        )
