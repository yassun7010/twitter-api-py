import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.data import JsonDataLoader
from twitter_api.api.resources.v2_dm_conversations.post_dm_conversations import (
    V2PostDmConversationsResponseBody,
)
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestV2GetUserFollowing:
    @pytest.mark.skip("You do not have permission to DM one or more participants.")
    def test_get_user_following(
        self,
        real_user_auth_v1_client: TwitterApiRealClient,
    ):
        response = (
            real_user_auth_v1_client.chain()
            .request("https://api.twitter.com/2/dm_conversations")
            .post(
                "2244994945",
                {
                    "conversation_type": "Group",
                    "participant_ids": ["944480690", "906948460078698496"],
                    "message": {
                        "text": "Hello to you two, this is a new group conversation"
                    },
                },
            )
        )

        print(response.json())

        assert True


class TestMockV2GetUserFollowing:
    @pytest.mark.parametrize(
        "json_filename",
        [
            "post_dm_conversations.json",
        ],
    )
    def test_mock_get_user_following(
        self,
        mock_app_auth_v2_client: TwitterApiMockClient,
        json_data_loader: JsonDataLoader,
        json_filename: str,
    ):
        expected_response = V2PostDmConversationsResponseBody(
            **json_data_loader.load(json_filename)
        )

        assert (
            mock_app_auth_v2_client.chain()
            .inject_post_response_body(
                "https://api.twitter.com/2/dm_conversations",
                expected_response,
            )
            .request("https://api.twitter.com/2/dm_conversations")
            .post(
                "2244994945",
                {
                    "conversation_type": "Group",
                    "participant_ids": ["944480690", "906948460078698496"],
                    "message": {
                        "text": "Hello to you two, this is a new group conversation"
                    },
                },
            )
            == expected_response
        )
