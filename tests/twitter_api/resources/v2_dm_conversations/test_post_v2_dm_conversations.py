import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.contexts.spawn_real_client import spawn_real_client
from tests.data import json_test_data
from twitter_api.client.twitter_api_async_mock_client import TwitterApiAsyncMockClient
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.resources.v2_dm_conversations.post_v2_dm_conversations import (
    PostV2DmConversationsResponseBody,
)
from twitter_api.types.v2_user.user_id import UserId


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestPostV2DmConversationsMessages:
    @pytest.mark.parametrize(
        "client_fixture_name,permit",
        [
            ("oauth1_app_real_client", True),
            ("oauth1_user_real_client", True),
            ("oauth2_app_real_client", False),
            ("oauth2_user_real_client", True),
        ],
    )
    def test_post_v2_dm_conversations_messages(
        self,
        participant_ids: list[UserId],
        client_fixture_name: str,
        permit: bool,
        request: pytest.FixtureRequest,
    ):
        with spawn_real_client(client_fixture_name, request, permit) as real_client:
            response_body = (
                real_client.chain()
                .request("https://api.twitter.com/2/dm_conversations")
                .post(
                    {
                        "conversation_type": "Group",
                        "participant_ids": participant_ids,
                        "message": {
                            "text": "Hello to you two, this is a new group conversation"
                        },
                    },
                )
            )

            print(response_body.model_dump_json())

            assert response_body.model_extra == {}


class TestMockPostV2DmConversationsMessages:
    @pytest.mark.parametrize(
        "json_filename",
        [
            "post_v2_dm_conversations_response_body.json",
        ],
    )
    def test_mock_post_v2_dm_conversations_messages(
        self,
        oauth2_app_mock_client: TwitterApiMockClient,
        json_filename: str,
    ):
        response_body = PostV2DmConversationsResponseBody.model_validate(
            json_test_data(json_filename)
        )

        assert response_body.model_extra == {}

        assert (
            oauth2_app_mock_client.chain()
            .inject_post_response_body(
                "https://api.twitter.com/2/dm_conversations",
                response_body,
            )
            .request("https://api.twitter.com/2/dm_conversations")
            .post(
                {
                    "conversation_type": "Group",
                    "participant_ids": ["944480690", "906948460078698496"],
                    "message": {
                        "text": "Hello to you two, this is a new group conversation"
                    },
                },
            )
        ) == response_body


class TestAsyncMockPostV2DmConversationsMessages:
    @pytest.mark.asyncio
    async def test_async_mock_post_v2_dm_conversations_messages(
        self,
        oauth2_app_async_mock_client: TwitterApiAsyncMockClient,
    ):
        response_body = PostV2DmConversationsResponseBody.model_validate(
            json_test_data("post_v2_dm_conversations_response_body.json")
        )

        assert response_body.model_extra == {}

        assert (
            await (
                oauth2_app_async_mock_client.chain()
                .inject_post_response_body(
                    "https://api.twitter.com/2/dm_conversations",
                    response_body,
                )
                .request("https://api.twitter.com/2/dm_conversations")
                .post(
                    {
                        "conversation_type": "Group",
                        "participant_ids": ["944480690", "906948460078698496"],
                        "message": {
                            "text": "Hello to you two, this is a new group conversation"
                        },
                    },
                )
            )
            == response_body
        )
