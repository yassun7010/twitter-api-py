import re

import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.contexts.spawn_real_client import spawn_real_client
from tests.data import json_test_data
from tests.types.convinient_tweet import ConvinientTweetDetail
from twitter_api.api.resources.v2_tweet.get_v2_tweet import (
    GetV2TweetQueryParameters,
    GetV2TweetResponseBody,
)
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
def all_fields_tweet() -> ConvinientTweetDetail:
    return ConvinientTweetDetail.parse_obj(
        GetV2TweetResponseBody.parse_file(
            json_test_data("get_v2_tweet_response_all_fields.json"),
        ).data
    )


@pytest.fixture
def all_fields(
    all_expansions: list[Expansion],
    all_media_fields: list[MediaField],
    all_place_fields: list[PlaceField],
    all_poll_fields: list[PollField],
    all_tweet_fields: list[TweetField],
    all_user_fields: list[UserField],
) -> GetV2TweetQueryParameters:
    return {
        "expansions": all_expansions,
        "media.fields": all_media_fields,
        "place.fields": all_place_fields,
        "poll.fields": all_poll_fields,
        "tweet.fields": all_tweet_fields,
        "user.fields": all_user_fields,
    }


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestGetV2Tweet:
    @pytest.mark.parametrize(
        "client_fixture_name,permit",
        [
            ("real_oauth1_app_client", True),
            ("real_oauth2_user_client", True),
            ("real_oauth2_app_client", True),
        ],
    )
    def test_get_v2_tweet(
        self,
        intro_tweet: TweetDetail,
        client_fixture_name: str,
        permit: bool,
        request: pytest.FixtureRequest,
    ):
        with spawn_real_client(client_fixture_name, request, permit) as real_client:
            expected_response = GetV2TweetResponseBody(data=intro_tweet)

            response = real_client.request("https://api.twitter.com/2/tweets/:id").get(
                intro_tweet.id
            )

            print(response.json())
            print(expected_response.json())

            assert get_extra_fields(response) == {}
            assert response == expected_response

    def test_get_v2_tweet_all_fields(
        self,
        real_oauth2_app_client: TwitterApiRealClient,
        intro_tweet: TweetDetail,
        all_fields: GetV2TweetQueryParameters,
    ):
        response = real_oauth2_app_client.request(
            "https://api.twitter.com/2/tweets/:id"
        ).get(
            intro_tweet.id,
            all_fields,
        )

        print(response.json())

        assert get_extra_fields(response) == {}

    def test_get_v2_tweet_retweeted(
        self,
        real_oauth2_app_client: TwitterApiRealClient,
        all_fields: GetV2TweetQueryParameters,
    ):
        response = real_oauth2_app_client.request(
            "https://api.twitter.com/2/tweets/:id"
        ).get(
            "1275781448855891968",
            all_fields,
        )

        print(response.json())

        assert get_extra_fields(response) == {}


class TestMockGetV2Tweet:
    @pytest.mark.parametrize(
        "json_filename",
        [
            "get_v2_tweet_response_all_fields.json",
        ],
    )
    def test_mock_get_v2_tweet(
        self,
        mock_oauth2_app_client: TwitterApiMockClient,
        intro_tweet: TweetDetail,
        all_fields: GetV2TweetQueryParameters,
        json_filename: str,
    ):
        response = GetV2TweetResponseBody.parse_file(
            json_test_data(json_filename),
        )

        assert get_extra_fields(response) == {}
        assert (
            mock_oauth2_app_client.chain()
            .inject_get_response_body("https://api.twitter.com/2/tweets/:id", response)
            .request("https://api.twitter.com/2/tweets/:id")
            .get(
                intro_tweet.id,
                all_fields,
            )
        ) == response

    def test_has_tweet_text(self, all_fields_tweet: ConvinientTweetDetail):
        assert len(all_fields_tweet.text) > 0

    def test_has_url(self, all_fields_tweet: ConvinientTweetDetail):
        url_regex = re.compile(r"^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+")

        assert len(all_fields_tweet.entities_urls) != 0

        for url in all_fields_tweet.entities_urls:
            assert url_regex.match(str(url.expanded_url))

    def test_has_like_count(self, all_fields_tweet: ConvinientTweetDetail):
        assert all_fields_tweet.like_count is not None
