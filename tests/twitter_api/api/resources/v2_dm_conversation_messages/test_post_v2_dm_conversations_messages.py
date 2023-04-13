import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.contexts.spawn_real_client import spawn_real_client
from tests.data import json_test_data
from twitter_api.api.resources.v2_dm_conversation_messages.post_v2_dm_conversations_messages import (
    PostV2DmConversationMessagesResponseBody,
)
from twitter_api.api.types.v2_user.user_id import UserId
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.types.extra_permissive_model import get_extra_fields


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestGetV2DmConversationsMessages:
    @pytest.mark.parametrize(
        "client_fixture_name,permit",
        [
            ("real_oauth1_app_client", True),
            ("real_oauth2_user_client", True),
            ("real_oauth2_app_client", False),
        ],
    )
    def test_get_v2_dm_conversations_messages(
        self,
        participant_id: UserId,
        participant_ids: list[UserId],
        client_fixture_name: str,
        permit: bool,
        request: pytest.FixtureRequest,
    ):
        with spawn_real_client(client_fixture_name, request, permit) as real_client:
            dm_conversation_id = (
                real_client.chain()
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
                real_client.chain()
                .request(
                    "https://api.twitter.com/2/dm_conversations/:dm_conversation_id/messages"
                )
                .post(dm_conversation_id, {"text": "DM のテスト。"})
            )

            print(response.json())

            assert get_extra_fields(response) == {}


class TestMockGetV2DmConversationsMessages:
    @pytest.mark.parametrize(
        "json_filename",
        [
            "post_v2_dm_conversations_messages.json",
        ],
    )
    def test_mock_get_v2_dm_conversations_messages(
        self,
        mock_oauth2_app_client: TwitterApiMockClient,
        json_filename: str,
    ):
        response = PostV2DmConversationMessagesResponseBody.parse_file(
            json_test_data(json_filename)
        )

        assert get_extra_fields(response) == {}

        assert (
            mock_oauth2_app_client.chain()
            .inject_post_response_body(
                "https://api.twitter.com/2/dm_conversations/:dm_conversation_id/messages",
                response,
            )
            .request(
                "https://api.twitter.com/2/dm_conversations/:dm_conversation_id/messages"
            )
            .post("2244994945", {"text": "DM のテスト。"})
        ) == response
