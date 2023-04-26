import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.contexts.spawn_real_client import spawn_real_client
from tests.data import json_test_data
from twitter_api.api.resources.v2_tweet.get_v2_tweet import (
    GetV2TweetQueryParameters,
    GetV2TweetResponseBody,
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
def all_fields() -> GetV2TweetQueryParameters:
    return {
        "expansions": ALL_TWEET_EXPANSIONS,
        "media.fields": ALL_MEDIA_FIELDS,
        "place.fields": ALL_PLACE_FIELDS,
        "poll.fields": ALL_POLL_FIELDS,
        "tweet.fields": ALL_PUBLIC_TWEET_FIELDS,
        "user.fields": ALL_USER_FIELDS,
    }


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestGetV2Tweet:
    @pytest.mark.parametrize(
        "client_fixture_name,permit",
        [
            ("oauth1_app_real_client", True),
            ("oauth1_user_real_client", True),
            ("oauth2_app_real_client", True),
            ("oauth2_user_real_client", True),
        ],
    )
    def test_get_v2_tweet(
        self,
        intro_tweet: Tweet,
        client_fixture_name: str,
        permit: bool,
        request: pytest.FixtureRequest,
    ):
        with spawn_real_client(client_fixture_name, request, permit) as real_client:
            expected_response_body = GetV2TweetResponseBody(data=intro_tweet)

            response_body = real_client.request(
                "https://api.twitter.com/2/tweets/:id"
            ).get(intro_tweet.id)

            print(response_body.json())
            print(expected_response_body.json())

            assert get_extra_fields(response_body) == {}
            assert response_body == expected_response_body

    def test_get_v2_tweet_all_fields(
        self,
        oauth2_app_real_client: TwitterApiRealClient,
        intro_tweet: Tweet,
        all_fields: GetV2TweetQueryParameters,
    ):
        response_body = oauth2_app_real_client.request(
            "https://api.twitter.com/2/tweets/:id"
        ).get(
            intro_tweet.id,
            all_fields,
        )

        print(response_body.json())

        assert get_extra_fields(response_body) == {}


class TestMockGetV2Tweet:
    @pytest.mark.parametrize(
        "json_filename",
        [
            "get_v2_tweet_response_body_all_fields.json",
        ],
    )
    def test_mock_get_v2_tweet(
        self,
        oauth2_app_mock_client: TwitterApiMockClient,
        intro_tweet: Tweet,
        all_fields: GetV2TweetQueryParameters,
        json_filename: str,
    ):
        response_body = GetV2TweetResponseBody.parse_file(
            json_test_data(json_filename),
        )

        assert get_extra_fields(response_body) == {}
        assert (
            oauth2_app_mock_client.chain()
            .inject_get_response_body(
                "https://api.twitter.com/2/tweets/:id", response_body
            )
            .request("https://api.twitter.com/2/tweets/:id")
            .get(
                intro_tweet.id,
                all_fields,
            )
        ) == response_body


class TestAsyncMockGetV2Tweet:
    @pytest.mark.asyncio
    async def test_async_mock_get_v2_tweet(
        self,
        oauth2_app_async_mock_client: TwitterApiAsyncMockClient,
        intro_tweet: Tweet,
        all_fields: GetV2TweetQueryParameters,
    ):
        response_body = GetV2TweetResponseBody.parse_file(
            json_test_data("get_v2_tweet_response_body_all_fields.json"),
        )

        assert get_extra_fields(response_body) == {}
        assert (
            await (
                oauth2_app_async_mock_client.chain()
                .inject_get_response_body(
                    "https://api.twitter.com/2/tweets/:id", response_body
                )
                .request("https://api.twitter.com/2/tweets/:id")
                .get(
                    intro_tweet.id,
                    all_fields,
                )
            )
            == response_body
        )
