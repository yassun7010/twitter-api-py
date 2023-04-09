import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.contexts.check_oauth2_user_access_token import check_oauth2_user_access_token
from tests.data import JsonDataLoader
from twitter_api.api.resources.v2_user_retweets.post_v2_user_retweets import (
    PostV2UserRetweetsResponseBody,
)
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestGetV2UserRetweets:
    def test_get_v2_user_following(
        self,
        user_id,
        real_oauth2_user_client: TwitterApiRealClient,
    ):
        with check_oauth2_user_access_token():
            (
                real_oauth2_user_client.chain()
                .request("https://api.twitter.com/2/users/:id/retweets")
                .post(user_id, {"tweet_id": "1228393702244134912"})
            )

        assert True


class TestMockGetV2UserRetweets:
    @pytest.mark.parametrize(
        "json_filename",
        [
            "get_v2_user_retweets_response.json",
        ],
    )
    def test_mock_get_v2_user_following(
        self,
        mock_oauth2_app_client: TwitterApiMockClient,
        json_data_loader: JsonDataLoader,
        json_filename: str,
    ):
        expected_response = PostV2UserRetweetsResponseBody.parse_obj(
            json_data_loader.load(json_filename)
        )

        assert (
            mock_oauth2_app_client.chain()
            .inject_post_response_body(
                "https://api.twitter.com/2/users/:id/retweets", expected_response
            )
            .request("https://api.twitter.com/2/users/:id/retweets")
            .post("2244994945", {"tweet_id": "1228393702244134912"})
        ) == expected_response
