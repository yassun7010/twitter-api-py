import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.contexts.spawn_real_client import spawn_real_client
from tests.data import json_test_data
from twitter_api.api.resources.v2_tweets.get_v2_tweets import (
    GetV2TweetsQueryParameters,
    GetV2TweetsResponseBody,
)
from twitter_api.api.types.v2_media.media_field import ALL_MEDIA_FIELDS
from twitter_api.api.types.v2_place.place_field import ALL_PLACE_FIELDS
from twitter_api.api.types.v2_poll.poll_field import ALL_POLL_FIELDS
from twitter_api.api.types.v2_tweet.tweet import Tweet
from twitter_api.api.types.v2_tweet.tweet_expansion import ALL_TWEET_EXPANSIONS
from twitter_api.api.types.v2_tweet.tweet_field import ALL_PUBLIC_TWEET_FIELDS
from twitter_api.api.types.v2_user.user_field import ALL_USER_FIELDS
from twitter_api.client.twitter_api_async_mock_client import TwitterApiAsyncMockClient
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient
from twitter_api.types.extra_permissive_model import get_extra_fields


@pytest.fixture
def tweets(intro_tweet: Tweet) -> list[Tweet]:
    return [intro_tweet]


@pytest.fixture
def all_fields(tweets: list[Tweet]) -> GetV2TweetsQueryParameters:
    return {
        "ids": list(map(lambda tweet: tweet.id, tweets)),
        "expansions": ALL_TWEET_EXPANSIONS,
        "media.fields": ALL_MEDIA_FIELDS,
        "place.fields": ALL_PLACE_FIELDS,
        "poll.fields": ALL_POLL_FIELDS,
        "tweet.fields": ALL_PUBLIC_TWEET_FIELDS,
        "user.fields": ALL_USER_FIELDS,
    }


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestGetV2Tweets:
    @pytest.mark.parametrize(
        "client_fixture_name,permit",
        [
            ("oauth1_app_real_client", True),
            ("oauth1_user_real_client", True),
            ("oauth2_app_real_client", True),
            ("oauth2_user_real_client", True),
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
            expected_response_body = GetV2TweetsResponseBody(data=tweets)

            response_body = (
                real_client.chain()
                .request("https://api.twitter.com/2/tweets")
                .get({"ids": list(map(lambda tweet: tweet.id, tweets))})
            )

            print(response_body.json())
            print(expected_response_body.json())

            assert get_extra_fields(response_body) == {}
            assert response_body == expected_response_body

    def test_get_v2_tweet_all_fields(
        self,
        oauth2_app_real_client: TwitterApiRealClient,
        all_fields: GetV2TweetsQueryParameters,
    ):
        response_body = (
            oauth2_app_real_client.chain()
            .request("https://api.twitter.com/2/tweets")
            .get(all_fields)
        )

        print(response_body.json())

        assert get_extra_fields(response_body) == {}


class TestMockGetV2Tweets:
    @pytest.mark.parametrize(
        "json_filename",
        [
            "get_v2_tweets_response_body_all_fields.json",
        ],
    )
    def test_mock_get_v2_tweets(
        self,
        oauth2_app_mock_client: TwitterApiMockClient,
        all_fields: GetV2TweetsQueryParameters,
        json_filename: str,
    ):
        response_body = GetV2TweetsResponseBody.parse_file(
            json_test_data(json_filename),
        )

        assert (
            oauth2_app_mock_client.chain()
            .inject_get_response_body("https://api.twitter.com/2/tweets", response_body)
            .request("https://api.twitter.com/2/tweets")
            .get(all_fields)
        ) == response_body


class TestAsyncMockGetV2Tweets:
    @pytest.mark.asyncio
    async def test_async_mock_get_v2_tweets(
        self,
        oauth2_app_async_mock_client: TwitterApiAsyncMockClient,
        all_fields: GetV2TweetsQueryParameters,
    ):
        response_body: GetV2TweetsResponseBody = GetV2TweetsResponseBody.parse_file(
            json_test_data("get_v2_tweets_response_body_all_fields.json"),
        )

        assert (
            await (
                oauth2_app_async_mock_client.chain()
                .inject_get_response_body(
                    "https://api.twitter.com/2/tweets", response_body
                )
                .request("https://api.twitter.com/2/tweets")
                .get(all_fields)
            )
            == response_body
        )
