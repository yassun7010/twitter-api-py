import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.contexts.check_oauth2_user_access_token import check_oauth2_user_access_token
from tests.data import json_test_data
from twitter_api.api.resources.v2_dm_conversations_with_messages.post_v2_dm_conversations_with_messages import (
    PostV2DmConversationsWithParticipantMessagesResponseBody,
)
from twitter_api.api.types.v2_user.user_id import UserId
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient
from twitter_api.types.extra_permissive_model import get_extra_fields


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestPostV2DmConversationsWithMessages:
    @pytest.mark.parametrize(
        "real_client_name",
        [
            "real_oauth1_user_client",
            "real_oauth2_user_client",
        ],
    )
    def test_post_v2_dm_conversations_with_messages_by_client(
        self,
        participant_id: UserId,
        real_client_name: str,
        request: pytest.FixtureRequest,
    ):
        real_client: TwitterApiRealClient = request.getfixturevalue(real_client_name)

        with check_oauth2_user_access_token():
            response = (
                real_client.chain()
                .request(
                    "https://api.twitter.com/2/dm_conversations/with/:participant_id/messages"
                )
                .post(participant_id, {"text": "DM のテスト。"})
            )

            print(response.json())

            assert get_extra_fields(response) == {}


class TestMockPostV2DmConversationsWithMessages:
    @pytest.mark.parametrize(
        "json_filename",
        [
            "post_v2_dm_conversations_with_participant_messages.json",
        ],
    )
    def test_mock_post_v2_dm_conversations_with_messages(
        self,
        mock_oauth2_app_client: TwitterApiMockClient,
        json_filename: str,
    ):
        response = PostV2DmConversationsWithParticipantMessagesResponseBody.parse_file(
            json_test_data(json_filename)
        )

        assert get_extra_fields(response) == {}

        assert (
            mock_oauth2_app_client.chain()
            .inject_post_response_body(
                "https://api.twitter.com/2/dm_conversations/with/:participant_id/messages",
                response,
            )
            .request(
                "https://api.twitter.com/2/dm_conversations/with/:participant_id/messages"
            )
            .post("2244994945", {"text": "DM のテスト。"})
        ) == response
