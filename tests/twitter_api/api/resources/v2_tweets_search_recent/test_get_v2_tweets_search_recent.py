import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.data import JsonDataLoader
from twitter_api.api.resources.v2_tweets_search_recent.get_v2_tweets_search_recent import (
    GetV2TweetsSearchRecentResponseBody,
)
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestGetV2TweetsSearchRecent:
    def test_get_v2_search_recent(self, real_oauth2_app_client: TwitterApiRealClient):
        real_response = (
            real_oauth2_app_client.chain()
            .request("https://api.twitter.com/2/tweets/search/recent")
            .get({"query": "ツイート", "max_results": 1})
        )

        print(real_response.json())

        assert True


class TestMockGetV2TweetsSearchRecent:
    @pytest.mark.parametrize(
        "json_filename",
        [
            "get_tweets_search_recent_response.json",
            "get_tweets_search_recent_response_empty_result.json",
        ],
    )
    def test_mock_get_v2_search_recent(
        self,
        mock_oauth2_app_client: TwitterApiMockClient,
        json_data_loader: JsonDataLoader,
        json_filename: str,
    ):
        expected_response = GetV2TweetsSearchRecentResponseBody.parse_obj(
            json_data_loader.load(json_filename)
        )

        assert (
            mock_oauth2_app_client.chain()
            .inject_get_response_body(
                "https://api.twitter.com/2/tweets/search/recent", expected_response
            )
            .request("https://api.twitter.com/2/tweets/search/recent")
            .get(
                {
                    "query": "モックされているので、この検索条件に意味はない",
                    "expansions": ["attachments.poll_ids"],
                    "media.fields": ["preview_image_url"],
                }
            )
        ) == expected_response
