import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.data import JsonDataLoader
from twitter_api.api.resources.v2_dm_conversations_with_messages.post_v2_dm_conversations_with_messages import (
    PostV2DmConversationsWithParticipantMessagesResponseBody,
)
from twitter_api.api.types.v2_user.user_id import UserId
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient
from twitter_api.types.extra_permissive_model import get_extra_fields


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestGetV2UserFollowing:
    def test_get_v2_user_following(
        self,
        participant_id: UserId,
        real_oauth1_user_client: TwitterApiRealClient,
    ):
        response = (
            real_oauth1_user_client.chain()
            .request(
                "https://api.twitter.com/2/dm_conversations/with/:participant_id/messages"
            )
            .post(participant_id, {"text": "DM のテスト。"})
        )

        print(response.json())

        assert get_extra_fields(response) == {}


class TestMockGetV2UserFollowing:
    @pytest.mark.parametrize(
        "json_filename",
        [
            "post_v2_dm_conversations_with_participant_messages.json",
        ],
    )
    def test_mock_get_v2_user_following(
        self,
        mock_oauth2_app_client: TwitterApiMockClient,
        json_data_loader: JsonDataLoader,
        json_filename: str,
    ):
        response = PostV2DmConversationsWithParticipantMessagesResponseBody.parse_obj(
            json_data_loader.load(json_filename)
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
