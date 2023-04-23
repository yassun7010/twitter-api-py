import itertools
from functools import reduce

import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.contexts.spawn_real_client import spawn_real_client
from tests.data import json_test_data
from twitter_api.api.resources.v2_tweets_search_recent.get_v2_tweets_search_recent import (
    GetV2TweetsSearchRecentResponseBody,
)
from twitter_api.api.types.v2_expansion import Expansion
from twitter_api.api.types.v2_media.media_field import MediaField
from twitter_api.api.types.v2_place.place_field import PlaceField
from twitter_api.api.types.v2_poll.poll_field import PollField
from twitter_api.api.types.v2_tweet.tweet_field import TweetField
from twitter_api.api.types.v2_user.user_field import UserField
from twitter_api.client.twitter_api_async_mock_client import TwitterApiAsyncMockClient
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient
from twitter_api.types.extra_permissive_model import get_extra_fields


@pytest.fixture
def json_files() -> list[str]:
    return [
        "get_v2_tweets_search_recent_response/response_01.json",
        "get_v2_tweets_search_recent_response/response_02.json",
    ]


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestGetV2TweetsSearchRecent:
    @pytest.mark.parametrize(
        "client_fixture_name,permit",
        [
            ("oauth1_app_real_client", True),
            ("oauth1_user_real_client", True),
            ("oauth2_app_real_client", True),
            ("oauth2_user_real_client", True),
        ],
    )
    def test_get_v2_search_recent_when_oauth1(
        self,
        client_fixture_name: str,
        permit: bool,
        request: pytest.FixtureRequest,
    ):
        with spawn_real_client(client_fixture_name, request, permit) as real_client:
            response = (
                real_client.chain()
                .resource("https://api.twitter.com/2/tweets/search/recent")
                .get({"query": "ツイート", "max_results": 10})
            )

            print(response.json())

            assert get_extra_fields(response) == {}

    def test_get_v2_search_recent_all_fields(
        self,
        oauth2_app_real_client: TwitterApiRealClient,
        all_expansions: list[Expansion],
        all_media_fields: list[MediaField],
        all_place_fields: list[PlaceField],
        all_poll_fields: list[PollField],
        all_tweet_fields: list[TweetField],
        all_user_fields: list[UserField],
    ):
        next_token = None
        for _ in range(3):
            response = (
                oauth2_app_real_client.chain()
                .resource("https://api.twitter.com/2/tweets/search/recent")
                .get(
                    {
                        "query": "#japan test",
                        "max_results": 100,
                        "expansions": all_expansions,
                        "media.fields": all_media_fields,
                        "place.fields": all_place_fields,
                        "poll.fields": all_poll_fields,
                        "tweet.fields": all_tweet_fields,
                        "user.fields": all_user_fields,
                        "next_token": next_token,
                    }
                )
            )

            assert get_extra_fields(response) == {}

            if response.meta.next_token is None:
                break

            next_token = response.meta.next_token


class TestMockGetV2TweetsSearchRecent:
    @pytest.mark.parametrize(
        "json_filename",
        [
            "get_v2_tweets_search_recent_response.json",
            "get_v2_tweets_search_recent_response_all_fields.json",
            "get_v2_tweets_search_recent_response_empty_result.json",
        ],
    )
    def test_mock_get_v2_search_recent(
        self,
        oauth2_app_mock_client: TwitterApiMockClient,
        json_filename: str,
    ):
        response = GetV2TweetsSearchRecentResponseBody.parse_file(
            json_test_data(json_filename)
        )

        assert get_extra_fields(response) == {}

        assert (
            oauth2_app_mock_client.chain()
            .inject_get_response_body(
                "https://api.twitter.com/2/tweets/search/recent", response
            )
            .resource("https://api.twitter.com/2/tweets/search/recent")
            .get(
                {
                    "query": "モックされているので、この検索条件に意味はない",
                    "expansions": ["attachments.poll_ids"],
                    "media.fields": ["preview_image_url"],
                }
            )
        ) == response

    def test_mock_get_v2_search_recent_recent(
        self,
        oauth2_app_mock_client: TwitterApiMockClient,
        all_expansions: list[Expansion],
        all_media_fields: list[MediaField],
        all_place_fields: list[PlaceField],
        all_poll_fields: list[PollField],
        all_tweet_fields: list[TweetField],
        all_user_fields: list[UserField],
        json_files: list[str],
    ):
        for json_file in json_files:
            oauth2_app_mock_client.inject_get_response_body(
                "https://api.twitter.com/2/tweets/search/recent",
                GetV2TweetsSearchRecentResponseBody.parse_file(
                    json_test_data(json_file)
                ),
            )

        next_token: str | None = None

        for _ in itertools.count():
            response = (
                oauth2_app_mock_client.chain()
                .resource("https://api.twitter.com/2/tweets/search/recent")
                .get(
                    {
                        "query": "#japan test",
                        "max_results": 100,
                        "expansions": all_expansions,
                        "media.fields": all_media_fields,
                        "place.fields": all_place_fields,
                        "poll.fields": all_poll_fields,
                        "tweet.fields": all_tweet_fields,
                        "user.fields": all_user_fields,
                        "next_token": next_token,
                    }
                )
            )

            assert get_extra_fields(response) == {}

            next_token = response.meta.next_token

            if next_token is None:
                break

    def test_mock_get_paging_response_iter_v2_search_recent(
        self,
        oauth2_app_mock_client: TwitterApiMockClient,
        json_files: list[str],
    ):
        responses = [
            GetV2TweetsSearchRecentResponseBody.parse_file(json_test_data(json_file))
            for json_file in json_files
        ]

        for response in responses:
            assert get_extra_fields(response) == {}

            oauth2_app_mock_client.inject_get_response_body(
                "https://api.twitter.com/2/tweets/search/recent",
                response,
            )

        assert [
            res
            for res in (
                oauth2_app_mock_client.chain()
                .resource("https://api.twitter.com/2/tweets/search/recent")
                .get_paging_response_iter(
                    {
                        "query": "モックされているので、この検索条件に意味はない",
                        "expansions": ["attachments.poll_ids"],
                        "media.fields": ["preview_image_url"],
                    }
                )
            )
        ] == responses

    def test_mock_get_collected_response_v2_search(
        self,
        oauth2_app_mock_client: TwitterApiMockClient,
        json_files: list[str],
    ):
        response = GetV2TweetsSearchRecentResponseBody.parse_file(
            json_test_data(
                "get_v2_tweets_search_recent_response/collected_response.json"
            )
        )

        assert get_extra_fields(response) == {}

        for json_file in json_files:
            oauth2_app_mock_client.inject_get_response_body(
                "https://api.twitter.com/2/tweets/search/recent",
                GetV2TweetsSearchRecentResponseBody.parse_file(
                    json_test_data(json_file)
                ),
            )

        assert (
            oauth2_app_mock_client.chain()
            .resource("https://api.twitter.com/2/tweets/search/recent")
            .get_collected_response(
                {
                    "query": "モックされているので、この検索条件に意味はない",
                    "expansions": ["attachments.poll_ids"],
                    "media.fields": ["preview_image_url"],
                }
            )
        ) == response


class TestAsyncMockGetV2TweetsSearchRecent:
    @pytest.mark.asyncio
    async def test_async_mock_get_v2_search_recent(
        self,
        oauth2_app_async_mock_client: TwitterApiAsyncMockClient,
    ):
        response = GetV2TweetsSearchRecentResponseBody.parse_file(
            json_test_data("get_v2_tweets_search_recent_response.json")
        )

        assert (
            await (
                oauth2_app_async_mock_client.chain()
                .inject_get_response_body(
                    "https://api.twitter.com/2/tweets/search/recent", response
                )
                .resource("https://api.twitter.com/2/tweets/search/recent")
                .get(
                    {
                        "query": "モックされているので、この検索条件に意味はない",
                        "expansions": ["attachments.poll_ids"],
                        "media.fields": ["preview_image_url"],
                    }
                )
            )
            == response
        )

    @pytest.mark.asyncio
    async def test_async_mock_get_paging_response_iter_v2_search_recent(
        self,
        oauth2_app_async_mock_client: TwitterApiAsyncMockClient,
        json_files: list[str],
    ):
        responses = [
            GetV2TweetsSearchRecentResponseBody.parse_file(json_test_data(json_file))
            for json_file in json_files
        ]

        for response in responses:
            oauth2_app_async_mock_client.inject_get_response_body(
                "https://api.twitter.com/2/tweets/search/recent",
                response,
            )

        assert [
            res
            async for res in await (
                oauth2_app_async_mock_client.chain()
                .resource("https://api.twitter.com/2/tweets/search/recent")
                .get_paging_response_iter(
                    {
                        "query": "モックされているので、この検索条件に意味はない",
                        "expansions": ["attachments.poll_ids"],
                        "media.fields": ["preview_image_url"],
                    }
                )
            )
        ] == responses

    @pytest.mark.asyncio
    async def test_async_mock_get_collected_response_v2_search(
        self,
        oauth2_app_async_mock_client: TwitterApiAsyncMockClient,
        json_files: list[str],
    ):
        response = GetV2TweetsSearchRecentResponseBody.parse_file(
            json_test_data(
                "get_v2_tweets_search_recent_response/collected_response.json"
            )
        )

        for json_file in json_files:
            oauth2_app_async_mock_client.inject_get_response_body(
                "https://api.twitter.com/2/tweets/search/recent",
                GetV2TweetsSearchRecentResponseBody.parse_file(
                    json_test_data(json_file)
                ),
            )

        assert (
            await (
                oauth2_app_async_mock_client.chain()
                .resource("https://api.twitter.com/2/tweets/search/recent")
                .get_collected_response(
                    {
                        "query": "モックされているので、この検索条件に意味はない",
                        "expansions": ["attachments.poll_ids"],
                        "media.fields": ["preview_image_url"],
                    }
                )
            )
            == response
        )
