import pytest

from tests.conftest import premium_account_not_set, synthetic_monitoring_is_disable
from tests.contexts.spawn_real_client import spawn_real_client
from tests.data import json_test_data
from twitter_api.api.resources.v2_tweets_search_all.get_v2_tweets_search_all import (
    GetV2TweetsSearchAllResponseBody,
)
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
@pytest.mark.skipif(**premium_account_not_set())
class TestGetV2TweetsSearchAll:
    @pytest.mark.parametrize(
        "client_fixture_name,permit",
        [
            ("real_oauth1_user_client", True),
            ("real_oauth2_user_client", True),
            ("real_oauth2_app_client", False),
        ],
    )
    def test_get_v2_search_all(
        self,
        client_fixture_name: str,
        permit: bool,
        request: pytest.FixtureRequest,
    ):
        with spawn_real_client(client_fixture_name, request, permit) as real_client:
            real_response: GetV2TweetsSearchAllResponseBody = (
                real_client.chain()
                .request("https://api.twitter.com/2/tweets/search/all")
                .get({"query": "conversation_id:1273733248749690880", "max_results": 1})
            )

            print(real_response.json())

            assert False


class TestMockGetV2TweetsSearchAll:
    def test_mock_get_v2_search_all(
        self,
        mock_oauth2_app_client: TwitterApiMockClient,
    ):
        response = GetV2TweetsSearchAllResponseBody.parse_file(
            json_test_data("get_v2_tweets_search_all_response.json")
        )

        assert (
            mock_oauth2_app_client.chain()
            .inject_get_response_body(
                "https://api.twitter.com/2/tweets/search/all", response
            )
            .request("https://api.twitter.com/2/tweets/search/all")
            .get({"query": "ツイート"})
        ) == response
