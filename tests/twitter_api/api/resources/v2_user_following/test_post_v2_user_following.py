import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.contexts.check_oauth2_user_access_token import check_oauth2_user_access_token
from tests.data import json_test_data
from twitter_api.api.resources.v2_user_following.post_v2_user_following import (
    PostV2UserFollowingResponseBody,
)
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient
from twitter_api.types.extra_permissive_model import get_extra_fields


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestGetV2UserFollowing:
    def test_get_v2_user_following(
        self,
        user_id,
        real_oauth2_user_client: TwitterApiRealClient,
    ):
        with check_oauth2_user_access_token():
            response = (
                real_oauth2_user_client.chain()
                .request("https://api.twitter.com/2/users/:id/following")
                .post(user_id, {"target_user_id": "2244994945"})
            )

            assert get_extra_fields(response) == {}


class TestMockGetV2UserFollowing:
    @pytest.mark.parametrize(
        "json_filename",
        [
            "get_v2_user_following_response.json",
        ],
    )
    def test_mock_get_v2_user_following(
        self,
        mock_oauth2_app_client: TwitterApiMockClient,
        json_filename: str,
    ):
        response = PostV2UserFollowingResponseBody.parse_file(
            json_test_data(json_filename)
        )

        assert get_extra_fields(response) == {}

        assert (
            mock_oauth2_app_client.chain()
            .inject_post_response_body(
                "https://api.twitter.com/2/users/:id/following", response
            )
            .request("https://api.twitter.com/2/users/:id/following")
            .post("2244994945", {"target_user_id": "2244994945"})
        ) == response
