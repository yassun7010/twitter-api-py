import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.data import JsonDataLoader
from twitter_api.api.resources.v2_dm_conversation_messages.post_v2_dm_conversations_messages import (
    PostV2DmConversationMessagesResponseBody,
)
from twitter_api.api.types.v2_user.user_id import UserId
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestGetV2UserFollowing:
    def test_get_v2_user_following(
        self,
        participant_id: UserId,
        participant_ids: list[UserId],
        real_oauth2_user_client: TwitterApiRealClient,
    ):
        dm_conversation_id = (
            real_oauth2_user_client.chain()
            .request("https://api.twitter.com/2/dm_conversations")
            .post(
                participant_id,
                {
                    "conversation_type": "Group",
                    "participant_ids": participant_ids,
                    "message": {
                        "text": "Hello to you two, this is a new group conversation"
                    },
                },
            )
            .data.dm_conversation_id
        )

        response = (
            real_oauth2_user_client.chain()
            .request(
                "https://api.twitter.com/2/dm_conversations/:dm_conversation_id/messages"
            )
            .post(dm_conversation_id, {"text": "DM のテスト。"})
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
                "https://api.twitter.com/2/dm_conversations/:dm_conversation_id/messages",
                expected_response,
            )
            .request(
                "https://api.twitter.com/2/dm_conversations/:dm_conversation_id/messages"
            )
            .post("2244994945", {"text": "DM のテスト。"})
        ) == expected_response
