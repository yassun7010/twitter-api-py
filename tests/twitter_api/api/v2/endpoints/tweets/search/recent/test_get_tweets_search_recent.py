import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.data import JsonDataLoader
from twitter_api.api.v2.endpoints.tweets.search.recent.get_tweets_search_recent import (
    V2GetTweetsSearchRecentResponseBody,
)
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestV2GetTweetsSearchRecent:
    def test_get_search_recent(self, real_app_auth_v2_client: TwitterApiRealClient):
        real_response = (
            real_app_auth_v2_client.chain()
            .request("https://api.twitter.com/2/tweets/search/recent")
            .get({"query": "ツイート", "max_results": 1})
        )

        print(real_response.json())

        assert True


class TestMockV2GetTweetsSearchRecent:
    @pytest.mark.parametrize(
        "json_filename",
        [
            "get_tweets_search_recent_response.json",
            "get_tweets_search_recent_response_empty_result.json",
        ],
    )
    def test_mock_get_search_recent(
        self,
        mock_app_auth_v2_client: TwitterApiMockClient,
        json_data_loader: JsonDataLoader,
        json_filename: str,
    ):
        expected_response = V2GetTweetsSearchRecentResponseBody(
            **json_data_loader.load(json_filename)
        )

        assert (
            mock_app_auth_v2_client.chain()
            .inject_get_response_body(
                "https://api.twitter.com/2/tweets/search/recent", expected_response
            )
            .request("https://api.twitter.com/2/tweets/search/recent")
            .get({"query": "モックされているので、この検索条件に意味はない"})
            == expected_response
        )
