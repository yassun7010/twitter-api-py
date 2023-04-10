from textwrap import dedent

import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.data import JsonDataLoader
from twitter_api.api.resources.v2_tweet.get_v2_tweet import GetV2TweetResponseBody
from twitter_api.api.types.v2_tweet.tweet_detail import TweetDetail
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient
from twitter_api.types.extra_permissive_model import get_extra_fields


@pytest.fixture
def tweet() -> TweetDetail:
    return TweetDetail(
        id="1460323737035677698",
        text=dedent(
            # flake8: noqa E501
            """
            Introducing a new era for the Twitter Developer Platform! \n
            📣The Twitter API v2 is now the primary API and full of new features
            ⏱Immediate access for most use cases, or apply to get more access for free
            📖Removed certain restrictions in the Policy
            https://t.co/Hrm15bkBWJ https://t.co/YFfCDErHsg
            """
        ).strip(),
        edit_history_tweet_ids=["1460323737035677698"],
    )


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestGetV2Tweet:
    def test_get_v2_tweet(
        self, real_oauth2_app_client: TwitterApiRealClient, tweet: TweetDetail
    ):
        response = real_oauth2_app_client.request(
            "https://api.twitter.com/2/tweets/:id"
        ).get(tweet.id)

        print(response.json())

        assert get_extra_fields(response) == {}

    def test_get_v2_tweet_all_query(
        self, real_oauth2_app_client: TwitterApiRealClient, tweet: TweetDetail
    ):
        response = real_oauth2_app_client.request(
            "https://api.twitter.com/2/tweets/:id"
        ).get(
            tweet.id,
            {
                "expansions": [
                    # "attachments.media_keys",
                    "attachments.poll_ids",
                    "author_id",
                    "edit_history_tweet_ids",
                    "entities.mentions.username",
                    "geo.place_id",
                    "in_reply_to_user_id",
                    "referenced_tweets.id",
                    "referenced_tweets.id.author_id",
                ],
                "media.fields": [
                    "alt_text",
                    "duration_ms",
                    "height",
                    "media_key",
                    "non_public_metrics",
                    "organic_metrics",
                    "preview_image_url",
                    "promoted_metrics",
                    "type",
                    "url",
                    "variants",
                    "width",
                ],
                "place.fields": [
                    "contained_within",
                    "country",
                    "country_code",
                    "full_name",
                    "geo",
                    "id",
                    "name",
                    "place_type",
                ],
                "poll.fields": [
                    "duration_minutes",
                    "end_datetime",
                    "id",
                    "options",
                    "voting_status",
                ],
                "tweet.fields": [
                    "attachments",
                    "author_id",
                    "context_annotations",
                    "conversation_id",
                    "created_at",
                    "edit_controls",
                    "entities",
                    "geo",
                    "id",
                    "in_reply_to_user_id",
                    "lang",
                    # "non_public_metrics",
                    # "organic_metrics",
                    "possibly_sensitive",
                    # "promoted_metrics",
                    "public_metrics",
                    "referenced_tweets",
                    "reply_settings",
                    "source",
                    "text",
                    "withheld",
                ],
                "user.fields": [
                    "created_at",
                    "description",
                    "entities",
                    "id",
                    "location",
                    "name",
                    "pinned_tweet_id",
                    "profile_image_url",
                    "protected",
                    "public_metrics",
                    "url",
                    "username",
                    "verified",
                    "verified_type",
                    "withheld",
                ],
            },
        )

        print(response.json())

        assert get_extra_fields(response) == {}


class TestMockGetV2Tweet:
    @pytest.mark.parametrize(
        "json_filename",
        [
            "get_v2_tweet_all_fields.json",
        ],
    )
    def test_mock_get_v2_tweet(
        self,
        mock_oauth2_app_client: TwitterApiMockClient,
        json_data_loader: JsonDataLoader,
        json_filename: str,
    ):
        response = GetV2TweetResponseBody.parse_obj(
            json_data_loader.load(json_filename)
        )

        assert get_extra_fields(response) == {}
        assert (
            mock_oauth2_app_client.chain()
            .inject_get_response_body("https://api.twitter.com/2/tweets/:id", response)
            .request("https://api.twitter.com/2/tweets/:id")
            .get("1460323737035677698")
        ) == response
