import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.data import JsonDataLoader
from twitter_api.api.resources.v2_dm_conversation_messages.post_v2_dm_conversations_messages import (
    PostV2DmConversationMessagesResponseBody,
)
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestGetV2UserFollowing:
    @pytest.mark.skip("You do not have permission to DM one or more participants.")
    def test_get_v2_user_following(
        self,
        real_auth1_user_client: TwitterApiRealClient,
    ):
        response = (
            real_auth1_user_client.chain()
            .request(
                "https://api.twitter.com/2/dm_conversations/:dm_conversation_id"
                "/messages"
            )
            .post("2244994945", {"text": "DM のテスト。"})
        )

        print(response.json())

        assert True


class TestMockGetV2UserFollowing:
    @pytest.mark.parametrize(
        "json_filename",
        [
            "post_dm_conversations_messages.json",
        ],
    )
    def test_mock_get_v2_user_following(
        self,
        mock_oauth2_app_client: TwitterApiMockClient,
        json_data_loader: JsonDataLoader,
        json_filename: str,
    ):
        expected_response = PostV2DmConversationMessagesResponseBody.parse_obj(
            json_data_loader.load(json_filename)
        )

        assert (
            mock_oauth2_app_client.chain()
            .inject_post_response_body(
                "https://api.twitter.com/2/dm_conversations/:dm_conversation_id"
                "/messages",
                expected_response,
            )
            .request(
                "https://api.twitter.com/2/dm_conversations/:dm_conversation_id"
                "/messages"
            )
            .post("2244994945", {"text": "DM のテスト。"})
        ) == expected_response
