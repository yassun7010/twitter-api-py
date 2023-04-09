from datetime import datetime

import pytest

from tests.conftest import synthetic_monitoring_is_disable
from twitter_api.api.resources.v2_tweet.delete_v2_tweet import (
    DeleteV2TweetResponseBody,
    DeleteV2TweetResponseBodyData,
)
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestDeleteV2Tweet:
    def test_delete_v2_tweet(self, real_auth1_user_client: TwitterApiRealClient):
        tweet_text = f"テストツイート。{datetime.now().isoformat()}"

        tweet = (
            real_auth1_user_client.chain()
            .request("https://api.twitter.com/2/tweets")
            .post({"text": tweet_text})
            .data
        )

        real_response = (
            real_auth1_user_client.chain()
            .request("https://api.twitter.com/2/tweets/:id")
            .delete(tweet.id)
        )

        print(real_response.json())

        assert real_response.data.deleted is True


class TestMockDeleteV2Tweet:
    def test_mock_delete_v2_tweet(self, mock_oauth2_app_client: TwitterApiMockClient):
        expected_response = DeleteV2TweetResponseBody(
            data=DeleteV2TweetResponseBodyData(deleted=True)
        )

        assert (
            mock_oauth2_app_client.chain()
            .inject_delete_response_body(
                "https://api.twitter.com/2/tweets/:id", expected_response
            )
            .request("https://api.twitter.com/2/tweets/:id")
            .delete("1234567890123456789")
        ) == expected_response
