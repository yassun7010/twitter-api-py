from datetime import datetime

import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.contexts.spawn_real_client import spawn_real_client
from twitter_api.client.twitter_api_async_mock_client import TwitterApiAsyncMockClient
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.resources.v2_tweet.delete_v2_tweet import (
    DeleteV2TweetResponseBody,
    DeleteV2TweetResponseBodyData,
)


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestDeleteV2Tweet:
    @pytest.mark.parametrize(
        "client_fixture_name,permit",
        [
            ("oauth1_app_real_client", True),
            ("oauth1_user_real_client", True),
            ("oauth2_app_real_client", False),
            ("oauth2_user_real_client", True),
        ],
    )
    def test_delete_v2_tweet(
        self,
        client_fixture_name: str,
        permit: bool,
        request: pytest.FixtureRequest,
    ):
        with spawn_real_client(client_fixture_name, request, permit) as real_client:
            tweet_text = f"削除テスト。{datetime.now().isoformat()}"

            tweet = (
                real_client.chain()
                .request("https://api.twitter.com/2/tweets")
                .post({"text": tweet_text})
                .data
            )

            real_response = (
                real_client.chain()
                .request("https://api.twitter.com/2/tweets/:id")
                .delete(tweet.id)
            )

            print(real_response.model_dump_json())

            assert real_response.data.deleted is True


class TestMockDeleteV2Tweet:
    def test_mock_delete_v2_tweet(self, oauth2_app_mock_client: TwitterApiMockClient):
        response_body = DeleteV2TweetResponseBody(
            data=DeleteV2TweetResponseBodyData(deleted=True)
        )

        assert response_body.model_extra == {}

        assert (
            oauth2_app_mock_client.chain()
            .inject_delete_response_body(
                "https://api.twitter.com/2/tweets/:id", response_body
            )
            .request("https://api.twitter.com/2/tweets/:id")
            .delete("1234567890123456789")
        ) == response_body


class TestAsyncMockDeleteV2Tweet:
    @pytest.mark.asyncio
    async def test_async_mock_delete_v2_tweet(
        self,
        oauth2_app_async_mock_client: TwitterApiAsyncMockClient,
    ):
        response_body = DeleteV2TweetResponseBody(
            data=DeleteV2TweetResponseBodyData(deleted=True)
        )

        assert response_body.model_extra == {}

        assert (
            await (
                oauth2_app_async_mock_client.chain()
                .inject_delete_response_body(
                    "https://api.twitter.com/2/tweets/:id", response_body
                )
                .request("https://api.twitter.com/2/tweets/:id")
                .delete("1234567890123456789")
            )
            == response_body
        )
