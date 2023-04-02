import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.data import JsonDataLoader
from twitter_api.api.v2.endpoints.tweets.search.all.get_tweets_search_all import (
    V2GetTweetsSearchAllResponseBody,
)
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient
from twitter_api.error import TwitterApiResponseFailed


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestV2GetTweetsSearchAll:
    def test_get_search_all_v1(self, real_app_auth_v2_client: TwitterApiRealClient):
        with pytest.raises(TwitterApiResponseFailed):
            (
                real_app_auth_v2_client.chain()
                .request("https://api.twitter.com/2/tweets/search/all")
                .get({"query": "conversation_id:1273733248749690880", "max_results": 1})
            )

    @pytest.mark.skipif(True, reason="プレミアムなアカウントでないとテストできない。")
    def test_get_search_all(self, real_app_auth_v2_client: TwitterApiRealClient):
        real_response = (
            real_app_auth_v2_client.chain()
            .request("https://api.twitter.com/2/tweets/search/all")
            .get({"query": "conversation_id:1273733248749690880", "max_results": 1})
        )

        print(real_response.dict())

        assert False


class TestMockV2GetTweetsSearchAll:
    def test_mock_get_search_all(
        self,
        mock_app_auth_v2_client: TwitterApiMockClient,
        json_data_loader: JsonDataLoader,
    ):
        expected_response = V2GetTweetsSearchAllResponseBody(
            **json_data_loader.load("get_tweets_search_all_response.json")
        )

        assert (
            mock_app_auth_v2_client.chain()
            .inject_get_response_body(
                "https://api.twitter.com/2/tweets/search/all", expected_response
            )
            .request("https://api.twitter.com/2/tweets/search/all")
            .get({"query": "ツイート"})
            == expected_response
        )
