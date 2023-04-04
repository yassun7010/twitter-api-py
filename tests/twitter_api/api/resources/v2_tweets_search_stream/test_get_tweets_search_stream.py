import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.data import JsonDataLoader
from twitter_api.api.resources.v2_tweets_search_stream.get_tweets_search_stream import (
    V2GetTweetsSearchStreamResponseBody,
)
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestV2GetTweetsSearchStream:
    @pytest.mark.skipif(
        True,
        reason=(
            "先にルールを作らないといけないらしい。"
            "POST /2/tweets/search/stream/rules を作成後にテストする必要があるが、"
            "まだ作っていないため後回し。"
        ),
    )
    def test_get_search_recent(self, real_app_auth_v2_client: TwitterApiRealClient):
        real_response = (
            real_app_auth_v2_client.chain()
            .request("https://api.twitter.com/2/tweets/search/stream")
            .get()
        )

        print(real_response.json())

        assert True


class TestMockV2GetTweetsSearchStream:
    @pytest.mark.parametrize(
        "json_filename",
        [
            "get_tweets_search_recent_response.json",
        ],
    )
    def test_mock_get_search_recent(
        self,
        mock_app_auth_v2_client: TwitterApiMockClient,
        json_data_loader: JsonDataLoader,
        json_filename: str,
    ):
        expected_response = V2GetTweetsSearchStreamResponseBody.parse_obj(
            json_data_loader.load(json_filename)
        )

        assert (
            mock_app_auth_v2_client.chain()
            .inject_get_response_body(
                "https://api.twitter.com/2/tweets/search/stream", expected_response
            )
            .request("https://api.twitter.com/2/tweets/search/stream")
            .get(
                {
                    "expansions": ["attachments.poll_ids"],
                    "media.fields": ["preview_image_url"],
                }
            )
        ) == expected_response
