import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.data import JsonDataLoader
from twitter_api.api.resources.v2_tweets_search_all.get_v2_tweets_search_all import (
    GetV2TweetsSearchAllResponseBody,
)
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestGetV2TweetsSearchAll:
    @pytest.mark.skip(reason="プレミアムなアカウントでないとテストできない。")
    def test_get_v2_search_all(self, real_app_auth_v2_client: TwitterApiRealClient):
        real_response: GetV2TweetsSearchAllResponseBody = (
            real_app_auth_v2_client.chain()
            .request("https://api.twitter.com/2/tweets/search/all")
            .get({"query": "conversation_id:1273733248749690880", "max_results": 1})
        )

        print(real_response.json())

        assert False


class TestMockGetV2TweetsSearchAll:
    def test_mock_get_v2_search_all(
        self,
        mock_app_auth_v2_client: TwitterApiMockClient,
        json_data_loader: JsonDataLoader,
    ):
        expected_response = GetV2TweetsSearchAllResponseBody.parse_obj(
            json_data_loader.load("get_tweets_search_all_response.json")
        )

        assert (
            mock_app_auth_v2_client.chain()
            .inject_get_response_body(
                "https://api.twitter.com/2/tweets/search/all", expected_response
            )
            .request("https://api.twitter.com/2/tweets/search/all")
            .get({"query": "ツイート"})
        ) == expected_response
