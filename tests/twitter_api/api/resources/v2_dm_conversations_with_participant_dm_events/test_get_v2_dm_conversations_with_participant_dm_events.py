import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.contexts.spawn_real_client import spawn_real_client
from tests.data import json_test_data
from twitter_api.api.resources.v2_dm_conversations_with_participant_dm_events.get_v2_dm_conversations_with_participant_dm_events import (
    GetV2DmConversationsWithParticipantDmEventsResponseBody,
)
from twitter_api.api.types.v2_dm_event.dm_event_expansion import ALL_DM_EVENT_EXPANSIONS
from twitter_api.api.types.v2_dm_event.dm_event_field import ALL_DM_EVENT_FIELDS
from twitter_api.api.types.v2_dm_event.dm_event_type import ALL_DM_EVENT_TYPES
from twitter_api.api.types.v2_tweet.tweet_field import ALL_PUBLIC_TWEET_FIELDS
from twitter_api.api.types.v2_user.user import User
from twitter_api.api.types.v2_user.user_field import ALL_USER_FIELDS
from twitter_api.api.types.v2_user.user_id import UserId
from twitter_api.client.twitter_api_async_mock_client import TwitterApiAsyncMockClient
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient
from twitter_api.types.extra_permissive_model import get_extra_fields


@pytest.fixture
def json_files() -> list[str]:
    return [
        "get_v2_dm_conversations_with_participant_dm_events/response_body_01.json",
        "get_v2_dm_conversations_with_participant_dm_events/response_body_02.json",
        "get_v2_dm_conversations_with_participant_dm_events/response_body_03.json",
        "get_v2_dm_conversations_with_participant_dm_events/response_body_04.json",
        "get_v2_dm_conversations_with_participant_dm_events/response_body_05.json",
    ]


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestGetV2DmConversationsWithParticipantDmEvents:
    @pytest.mark.parametrize(
        "client_fixture_name,permit",
        [
            ("oauth1_app_real_client", True),
            ("oauth1_user_real_client", True),
            ("oauth2_app_real_client", False),
            ("oauth2_user_real_client", True),
        ],
    )
    def test_get_v2_dm_conversations_with_participant_dm_events(
        self,
        participant_id: UserId,
        client_fixture_name: str,
        permit: bool,
        request: pytest.FixtureRequest,
    ):
        with spawn_real_client(client_fixture_name, request, permit) as real_client:
            response_body = (
                real_client.chain()
                .request(
                    "https://api.twitter.com/2/dm_conversations/with/:participant_id/dm_events"
                )
                .get(participant_id)
            )

            print(response_body.json())

            assert get_extra_fields(response_body) == {}

    def test_get_v2_dm_conversations_with_participant_dm_events_all_fields(
        self,
        participant_id: UserId,
        oauth1_app_real_client: TwitterApiRealClient,
    ):
        for response_body, _ in zip(
            oauth1_app_real_client.chain()
            .request(
                "https://api.twitter.com/2/dm_conversations/with/:participant_id/dm_events"
            )
            .get_paging_response_body_iter(
                participant_id,
                {
                    "dm_event.fields": ALL_DM_EVENT_FIELDS,
                    "event_types": ALL_DM_EVENT_TYPES,
                    "expansions": ALL_DM_EVENT_EXPANSIONS,
                    "max_results": 100,
                    "pagination_token": None,
                    "tweet.fields": ALL_PUBLIC_TWEET_FIELDS,
                    "user.fields": ALL_USER_FIELDS,
                },
            ),
            range(3),
        ):
            assert get_extra_fields(response_body) == {}


class TestMockGetV2DmConversationsWithParticipantDmEvents:
    @pytest.mark.parametrize(
        "json_filename",
        [
            "get_v2_dm_conversations_with_participant_dm_events_response_body.json",
        ],
    )
    def test_mock_get_v2_dm_conversations_with_participant_dm_events(
        self,
        oauth2_app_mock_client: TwitterApiMockClient,
        json_filename: str,
        twitter_dev_user: User,
    ):
        response_body = (
            GetV2DmConversationsWithParticipantDmEventsResponseBody.parse_file(
                json_test_data(json_filename)
            )
        )

        assert get_extra_fields(response_body) == {}

        assert (
            oauth2_app_mock_client.chain()
            .inject_get_response_body(
                "https://api.twitter.com/2/dm_conversations/with/:participant_id/dm_events",
                response_body,
            )
            .request(
                "https://api.twitter.com/2/dm_conversations/with/:participant_id/dm_events"
            )
            .get(twitter_dev_user.id)
        ) == response_body


class TestAsyncMockGetV2DmConversationsWithParticipantDmEvents:
    @pytest.mark.asyncio
    async def test_async_mock_get_v2_dm_conversations_with_participant_dm_events(
        self,
        oauth2_app_async_mock_client: TwitterApiAsyncMockClient,
        twitter_dev_user: User,
    ):
        response_body = GetV2DmConversationsWithParticipantDmEventsResponseBody.parse_file(
            json_test_data(
                "get_v2_dm_conversations_with_participant_dm_events_response_body.json"
            )
        )

        assert get_extra_fields(response_body) == {}

        assert (
            await (
                oauth2_app_async_mock_client.chain()
                .inject_get_response_body(
                    "https://api.twitter.com/2/dm_conversations/with/:participant_id/dm_events",
                    response_body,
                )
                .request(
                    "https://api.twitter.com/2/dm_conversations/with/:participant_id/dm_events"
                )
                .get(twitter_dev_user.id)
            )
            == response_body
        )

    @pytest.mark.asyncio
    async def test_async_mock_get_paging_response_body_iter_v2_dm_conversations_with_participant_dm_events(
        self,
        oauth2_app_async_mock_client: TwitterApiAsyncMockClient,
        json_files: list[str],
        twitter_dev_user: User,
    ):
        response_bodies = [
            GetV2DmConversationsWithParticipantDmEventsResponseBody.parse_file(
                json_test_data(json_file)
            )
            for json_file in json_files
        ]

        for response_body in response_bodies:
            oauth2_app_async_mock_client.inject_get_response_body(
                "https://api.twitter.com/2/dm_conversations/with/:participant_id/dm_events",
                response_body,
            )

        assert [
            res
            async for res in await (
                oauth2_app_async_mock_client.chain()
                .request(
                    "https://api.twitter.com/2/dm_conversations/with/:participant_id/dm_events"
                )
                .get_paging_response_body_iter(twitter_dev_user.id)
            )
        ] == response_bodies

    @pytest.mark.asyncio
    async def test_async_mock_get_collected_paging_response_body_v2_search(
        self,
        oauth2_app_async_mock_client: TwitterApiAsyncMockClient,
        json_files: list[str],
        twitter_dev_user: User,
    ):
        response_body = GetV2DmConversationsWithParticipantDmEventsResponseBody.parse_file(
            json_test_data(
                "get_v2_dm_conversations_with_participant_dm_events/collected_response_body.json"
            )
        )

        for json_file in json_files:
            oauth2_app_async_mock_client.inject_get_response_body(
                "https://api.twitter.com/2/dm_conversations/with/:participant_id/dm_events",
                GetV2DmConversationsWithParticipantDmEventsResponseBody.parse_file(
                    json_test_data(json_file)
                ),
            )

        assert (
            await (
                oauth2_app_async_mock_client.chain()
                .request(
                    "https://api.twitter.com/2/dm_conversations/with/:participant_id/dm_events"
                )
                .get_collected_paging_response_body(twitter_dev_user.id)
            )
            == response_body
        )
