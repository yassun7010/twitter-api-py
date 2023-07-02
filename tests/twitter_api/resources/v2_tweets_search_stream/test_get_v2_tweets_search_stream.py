import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.contexts.spawn_real_client import spawn_real_client
from tests.data import json_test_data
from twitter_api.client.twitter_api_async_mock_client import TwitterApiAsyncMockClient
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.resources.v2_tweets_search_stream.get_v2_tweets_search_stream import (
    GetV2TweetsSearchStreamResponseBody,
)


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestGetV2TweetsSearchStream:
    @pytest.mark.skip(reason="応答が戻ってこない。stream で実装する必要があるが、後回し。")
    @pytest.mark.parametrize(
        "client_fixture_name,permit",
        [
            ("oauth1_app_real_client", True),
            ("oauth1_user_real_client", True),
            ("oauth2_app_real_client", False),
            ("oauth2_user_real_client", True),
        ],
    )
    def test_get_v2_search_stream(
        self,
        client_fixture_name: str,
        permit: bool,
        request: pytest.FixtureRequest,
    ):
        with spawn_real_client(client_fixture_name, request, permit) as real_client:
            response_body = (
                real_client.chain()
                .request("https://api.twitter.com/2/tweets/search/stream")
                .get()
            )

            print(response_body.model_dump_json())

            assert response_body.model_extra == {}


class TestMockGetV2TweetsSearchStream:
    @pytest.mark.parametrize(
        "json_filename",
        [
            "get_v2_tweets_search_stream_response_body.json",
        ],
    )
    def test_mock_get_v2_search_stream(
        self,
        oauth2_app_mock_client: TwitterApiMockClient,
        json_filename: str,
    ):
        response_body = GetV2TweetsSearchStreamResponseBody.model_validate(
            json_test_data(json_filename)
        )

        assert response_body.model_extra == {}

        assert (
            oauth2_app_mock_client.chain()
            .inject_get_response_body(
                "https://api.twitter.com/2/tweets/search/stream", response_body
            )
            .request("https://api.twitter.com/2/tweets/search/stream")
            .get(
                {
                    "expansions": ["attachments.poll_ids"],
                    "media.fields": ["preview_image_url"],
                }
            )
        ) == response_body


class TestAsyncMockGetV2TweetsSearchStream:
    @pytest.mark.asyncio
    async def test_async_mock_get_v2_search_stream(
        self,
        oauth2_app_async_mock_client: TwitterApiAsyncMockClient,
    ):
        response_body = GetV2TweetsSearchStreamResponseBody.model_validate(
            json_test_data("get_v2_tweets_search_stream_response_body.json")
        )

        assert response_body.model_extra == {}

        assert (
            await (
                oauth2_app_async_mock_client.chain()
                .inject_get_response_body(
                    "https://api.twitter.com/2/tweets/search/stream", response_body
                )
                .request("https://api.twitter.com/2/tweets/search/stream")
                .get(
                    {
                        "expansions": ["attachments.poll_ids"],
                        "media.fields": ["preview_image_url"],
                    }
                )
            )
            == response_body
        )
