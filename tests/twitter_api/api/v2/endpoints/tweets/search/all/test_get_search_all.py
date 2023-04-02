import pytest

from tests.conftest import synthetic_monitoring_is_disable
from twitter_api.api.v2.endpoints.tweets.search.all.get_search_all import (
    V2GetTweetsSearchAllResponseBody,
    V2GetTweetsSearchAllResponseBodyMeta,
)
from twitter_api.api.v2.types.tweet.tweet import Tweet
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

    @pytest.mark.skipif(True, reason="OAuth2.0 で入らないといけないらしい。")
    def test_get_search_all(self, real_app_auth_v2_client: TwitterApiRealClient):
        real_response = (
            real_app_auth_v2_client.chain()
            .request("https://api.twitter.com/2/tweets/search/all")
            .get({"query": "conversation_id:1273733248749690880", "max_results": 1})
        )

        print(real_response.dict())

        assert False


class TestMockV2GetTweetsSearchAll:
    def test_mock_get_search_all(self, mock_app_auth_v2_client: TwitterApiMockClient):
        expected_response = V2GetTweetsSearchAllResponseBody(
            data=[
                Tweet(
                    id="12345676890123456789",
                    text="ツイートしました。",
                    edit_history_tweet_ids=[],
                )
            ],
            meta=V2GetTweetsSearchAllResponseBodyMeta(result_count=1),
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
