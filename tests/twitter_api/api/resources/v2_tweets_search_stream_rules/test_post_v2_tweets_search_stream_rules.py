import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.contexts.spawn_real_client import spawn_real_client
from tests.data import json_test_data
from twitter_api.api.resources.v2_tweets_search_stream_rules.post_v2_tweets_search_stream_rules import (
    PostV2TweetsSearchStreamRulesResponseBody,
)
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient
from twitter_api.types.extra_permissive_model import get_extra_fields


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestPostV2TweetsSearchStreamRules:
    @pytest.mark.parametrize(
        "client_fixture_name,permit",
        [
            ("oauth1_app_real_client", False),
            ("oauth1_user_real_client", False),
            ("oauth2_app_real_client", True),
            ("oauth2_user_real_client", False),
        ],
    )
    def test_post_v2_search_stream_rules_when_add_case(
        self,
        client_fixture_name: str,
        permit: bool,
        request: pytest.FixtureRequest,
    ):
        with spawn_real_client(client_fixture_name, request, permit) as real_client:
            response = (
                real_client.chain()
                .resource("https://api.twitter.com/2/tweets/search/stream/rules")
                .post(
                    {
                        "add": [
                            {"value": "cat has:media"},
                        ]
                    },
                    {"dry_run": True},
                )
            )

            print(response.json())

            assert get_extra_fields(response) == {}

    def test_post_v2_search_stream_rules_when_delete_case(
        self, oauth2_app_real_client: TwitterApiRealClient
    ):
        value = "dog has:media"
        (
            oauth2_app_real_client.chain()
            .resource("https://api.twitter.com/2/tweets/search/stream/rules")
            .post(
                {
                    "add": [
                        {"value": value},
                    ]
                },
            )
        )

        # 終わったら削除もしておく。
        response = (
            oauth2_app_real_client.chain()
            .resource("https://api.twitter.com/2/tweets/search/stream/rules")
            .post(
                {"delete": {"values": [value]}},
            )
        )

        print(response.json())

        assert get_extra_fields(response) == {}


class TestMockPostV2TweetsSearchStreamRules:
    @pytest.mark.parametrize(
        "json_filename",
        [
            "post_v2_search_stream_rules_response_create_rules.json",
            "post_v2_search_stream_rules_response_success.json",
        ],
    )
    def test_mock_post_v2_search_stream_rules(
        self,
        oauth2_app_mock_client: TwitterApiMockClient,
        json_filename: str,
    ):
        response = PostV2TweetsSearchStreamRulesResponseBody.parse_file(
            json_test_data(json_filename)
        )

        assert get_extra_fields(response) == {}

        assert (
            oauth2_app_mock_client.chain()
            .inject_post_response_body(
                "https://api.twitter.com/2/tweets/search/stream/rules",
                response,
            )
            .resource("https://api.twitter.com/2/tweets/search/stream/rules")
            .post(
                {
                    "add": [
                        {"value": "cat has:media"},
                    ]
                }
            )
        ) == response
