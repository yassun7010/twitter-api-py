import pytest

from tests.conftest import premium_account_not_set, synthetic_monitoring_is_disable
from tests.contexts.spawn_real_client import spawn_real_client
from tests.data import json_test_data
from twitter_api.client.twitter_api_async_mock_client import TwitterApiAsyncMockClient
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.resources.v2_tweets_search_all.get_v2_tweets_search_all import (
    GetV2TweetsSearchAllResponseBody,
)


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
@pytest.mark.skipif(**premium_account_not_set())
class TestGetV2TweetsSearchAll:
    @pytest.mark.parametrize(
        "client_fixture_name,permit",
        [
            ("oauth1_app_real_client", True),
            ("oauth1_user_real_client", True),
            ("oauth2_app_real_client", False),
            ("oauth2_user_real_client", True),
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

            print(real_response.model_dump_json())

            assert False


class TestMockGetV2TweetsSearchAll:
    def test_mock_get_v2_search_all(
        self,
        oauth2_app_mock_client: TwitterApiMockClient,
    ):
        response_body = GetV2TweetsSearchAllResponseBody.model_validate(
            json_test_data("get_v2_tweets_search_all_response_body.json")
        )

        assert (
            oauth2_app_mock_client.chain()
            .inject_get_response_body(
                "https://api.twitter.com/2/tweets/search/all", response_body
            )
            .request("https://api.twitter.com/2/tweets/search/all")
            .get({"query": "ツイート"})
        ) == response_body


class TestAsyncMockGetV2TweetsSearchAll:
    @pytest.mark.asyncio
    async def test_async_mock_get_v2_search_all(
        self,
        oauth2_app_async_mock_client: TwitterApiAsyncMockClient,
    ):
        response_body = GetV2TweetsSearchAllResponseBody.model_validate(
            json_test_data("get_v2_tweets_search_all_response_body.json")
        )

        assert (
            await (
                oauth2_app_async_mock_client.chain()
                .inject_get_response_body(
                    "https://api.twitter.com/2/tweets/search/all", response_body
                )
                .request("https://api.twitter.com/2/tweets/search/all")
                .get({"query": "ツイート"})
            )
            == response_body
        )
