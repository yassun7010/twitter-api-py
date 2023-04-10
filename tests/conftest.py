import os
from textwrap import dedent

import pytest

from twitter_api.api.resources.v2_tweet.get_v2_tweet import GetV2TweetQueryParameters
from twitter_api.api.types.v2_expansion import Expansion
from twitter_api.api.types.v2_media.media_field import MediaField
from twitter_api.api.types.v2_place.place_field import PlaceField
from twitter_api.api.types.v2_poll.poll_field import PollField
from twitter_api.api.types.v2_tweet.tweet_detail import TweetDetail
from twitter_api.api.types.v2_tweet.tweet_field import TweetField
from twitter_api.api.types.v2_user.user_field import UserField
from twitter_api.api.types.v2_user.user_id import UserId
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient


def synthetic_monitoring_is_disable() -> dict:
    """
    外形監視が無効であるかどうかを確認する。

    下記の環境変数を設定すると、実際に API を叩いてテストが行われる。

    ```env
    SYNTHETIC_MONITORING_TEST=true
    ```
    """

    return dict(
        condition=(
            "SYNTHETIC_MONITORING_TEST" not in os.environ
            or os.environ["SYNTHETIC_MONITORING_TEST"].lower() != "true"
        ),
        reason="外形監視が有効時（環境変数 SYNTHETIC_MONITORING_TEST が true ）に実行されます。",
    )


def premium_account_not_set() -> dict:
    """
    プレミアムアカウントの Access Token が未設定かを確認する。

    下記の環境変数を設定すると、テストが行われる。

    ```env
    OAUTH2_PREMIUM_ACCESS_TOKEN=XXXXXXXXXXXXXXXXXXXXXXX
    ```
    """

    return dict(
        condition=(
            "OAUTH2_PREMIUM_ACCESS_TOKEN" not in os.environ
            or os.environ["OAUTH2_PREMIUM_ACCESS_TOKEN"] == ""
        ),
        reason="プレミアムアカウントを持っている場合に実行されます。",
    )


@pytest.fixture
def user_id() -> UserId:
    return os.environ["USER_ID"]


@pytest.fixture
def participant_id(user_id) -> UserId:
    """
    DM への参加者の ID。

    会話を作れるのはアプリ側なのでアプリ側のユーザ ID を用いる。
    """

    return user_id


@pytest.fixture
def participant_ids(participant_id: UserId) -> list[UserId]:
    """
    DM の会話への参加者たちの ID。

    """

    return [participant_id] + os.environ["PARTICIPANT_IDS"].split(",")


@pytest.fixture
def real_oauth2_bearer_client() -> TwitterApiRealClient:
    return TwitterApiRealClient.from_oauth2_bearer_token_env()


@pytest.fixture
def real_oauth2_app_client() -> TwitterApiRealClient:
    return TwitterApiRealClient.from_oauth2_app_env()


@pytest.fixture
def real_oauth2_user_client() -> TwitterApiRealClient:
    return TwitterApiRealClient.from_oauth2_bearer_token_env("OAUTH2_USER_ACCESS_TOKEN")


@pytest.fixture
def real_oauth1_user_client() -> TwitterApiRealClient:
    return TwitterApiRealClient.from_oauth1_user_env()


@pytest.fixture
def mock_oauth2_app_client() -> TwitterApiMockClient:
    return TwitterApiMockClient(
        oauth_version="2.0",
        rate_limit_target="app",
    )


@pytest.fixture
def mock_oauth2_user_client() -> TwitterApiMockClient:
    return TwitterApiMockClient(
        oauth_version="2.0",
        rate_limit_target="user",
    )


@pytest.fixture
def mock_oauth1_app_client() -> TwitterApiMockClient:
    return TwitterApiMockClient(
        oauth_version="1.0a",
        rate_limit_target="app",
    )


@pytest.fixture
def mock_oauth1_user_client() -> TwitterApiMockClient:
    return TwitterApiMockClient(
        oauth_version="1.0a",
        rate_limit_target="user",
    )


@pytest.fixture
def all_expansions() -> list[Expansion]:
    return [
        # "attachments.media_keys",
        "attachments.poll_ids",
        "author_id",
        "edit_history_tweet_ids",
        "entities.mentions.username",
        "geo.place_id",
        "in_reply_to_user_id",
        "referenced_tweets.id",
        "referenced_tweets.id.author_id",
    ]


@pytest.fixture
def all_media_fields() -> list[MediaField]:
    return [
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
    ]


@pytest.fixture
def all_place_fields() -> list[PlaceField]:
    return [
        "contained_within",
        "country",
        "country_code",
        "full_name",
        "geo",
        "id",
        "name",
        "place_type",
    ]


@pytest.fixture
def all_poll_fields() -> list[PollField]:
    return [
        "duration_minutes",
        "end_datetime",
        "id",
        "options",
        "voting_status",
    ]


@pytest.fixture
def all_tweet_fields() -> list[TweetField]:
    return [
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
    ]


@pytest.fixture
def all_user_fields() -> list[UserField]:
    return [
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
    ]


@pytest.fixture
def intro_tweet() -> TweetDetail:
    """
    Twitter API の公式リファレンスのサンプルに記載されていたツイート。
    """

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
