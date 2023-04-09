import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.data import JsonDataLoader
from twitter_api.api.resources.v2_tweets_search_stream_rules.post_v2_tweets_search_stream_rules import (
    PostV2TweetsSearchStreamRulesResponseBody,
)
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient
from twitter_api.types.extra_permissive_model import get_extra_fields


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestPostV2TweetsSearchStreamRules:
    def test_post_v2_search_stream_rules_when_add_case(
        self, real_oauth2_app_client: TwitterApiRealClient
    ):
        response = (
            real_oauth2_app_client.chain()
            .request("https://api.twitter.com/2/tweets/search/stream/rules")
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
        self, real_oauth2_app_client: TwitterApiRealClient
    ):
        value = "dog has:media"
        (
            real_oauth2_app_client.chain()
            .request("https://api.twitter.com/2/tweets/search/stream/rules")
            .post(
                {
                    "add": [
                        {"value": value},
                    ]
                },
            )
        )

        response = (
            real_oauth2_app_client.chain()
            .request("https://api.twitter.com/2/tweets/search/stream/rules")
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
        mock_oauth2_app_client: TwitterApiMockClient,
        json_data_loader: JsonDataLoader,
        json_filename: str,
    ):
        response = PostV2TweetsSearchStreamRulesResponseBody.parse_obj(
            json_data_loader.load(json_filename)
        )

        assert get_extra_fields(response) == {}

        assert (
            mock_oauth2_app_client.chain()
            .inject_post_response_body(
                "https://api.twitter.com/2/tweets/search/stream/rules",
                response,
            )
            .request("https://api.twitter.com/2/tweets/search/stream/rules")
            .post(
                {
                    "add": [
                        {"value": "cat has:media"},
                    ]
                }
            )
        ) == response
