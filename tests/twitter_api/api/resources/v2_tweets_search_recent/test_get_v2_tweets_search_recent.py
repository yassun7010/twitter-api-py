import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.data import json_test_data
from twitter_api.api.resources.v2_tweets_search_recent.get_v2_tweets_search_recent import (
    GetV2TweetsSearchRecentResponseBody,
)
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient
from twitter_api.types.extra_permissive_model import get_extra_fields


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestGetV2TweetsSearchRecent:
    def test_get_v2_search_recent(self, real_oauth2_app_client: TwitterApiRealClient):
        response = (
            real_oauth2_app_client.chain()
            .request("https://api.twitter.com/2/tweets/search/recent")
            .get({"query": "ツイート", "max_results": 1})
        )

        print(response.json())

        assert get_extra_fields(response) == {}


class TestMockGetV2TweetsSearchRecent:
    @pytest.mark.parametrize(
        "json_filename",
        [
            "get_v2_tweets_search_recent_response.json",
            "get_v2_tweets_search_recent_response_empty_result.json",
        ],
    )
    def test_mock_get_v2_search_recent(
        self,
        mock_oauth2_app_client: TwitterApiMockClient,
        json_filename: str,
    ):
        response = GetV2TweetsSearchRecentResponseBody.parse_file(
            json_test_data(json_filename)
        )

        assert get_extra_fields(response) == {}

        assert (
            mock_oauth2_app_client.chain()
            .inject_get_response_body(
                "https://api.twitter.com/2/tweets/search/recent", response
            )
            .request("https://api.twitter.com/2/tweets/search/recent")
            .get(
                {
                    "query": "モックされているので、この検索条件に意味はない",
                    "expansions": ["attachments.poll_ids"],
                    "media.fields": ["preview_image_url"],
                }
            )
        ) == response
