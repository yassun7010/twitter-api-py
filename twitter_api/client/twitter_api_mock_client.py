from typing import Optional, Self, Union, overload

from twitter_api.api.resources.oauth2_invalidate_token import Oauth2InvalidateTokenUrl
from twitter_api.api.resources.oauth2_invalidate_token.post_oauth2_invalidate_token import (
    PostOauth2InvalidateTokenResponseBody,
)
from twitter_api.api.resources.oauth2_token import Oauth2TokenUrl
from twitter_api.api.resources.oauth2_token.post_oauth2_token import (
    PostOauth2TokenResponseBody,
)
from twitter_api.api.resources.oauth_request_token import OauthRequestTokenUrl
from twitter_api.api.resources.oauth_request_token.post_oauth_request_token import (
    PostOauthRequestTokenResponseBody,
)
from twitter_api.api.resources.v2_dm_conversation_messages import (
    V2DmConversationsMessagesUrl,
)
from twitter_api.api.resources.v2_dm_conversation_messages.post_v2_dm_conversations_messages import (
    PostV2DmConversationMessagesResponseBody,
)
from twitter_api.api.resources.v2_dm_conversations import V2DmConversationsUrl
from twitter_api.api.resources.v2_dm_conversations.post_v2_dm_conversations import (
    PostV2DmConversationsResponseBody,
)
from twitter_api.api.resources.v2_dm_conversations_with_messages import (
    V2DmConversationsWithParticipantMessagesUrl,
)
from twitter_api.api.resources.v2_dm_conversations_with_messages.post_v2_dm_conversations_with_messages import (
    PostV2DmConversationsWithParticipantMessagesResponseBody,
)
from twitter_api.api.resources.v2_tweet import V2TweetUrl
from twitter_api.api.resources.v2_tweet.delete_v2_tweet import DeleteV2TweetResponseBody
from twitter_api.api.resources.v2_tweet.get_v2_tweet import GetV2TweetResponseBody
from twitter_api.api.resources.v2_tweet_retweeted_by import V2TweetRetweetedByUrl
from twitter_api.api.resources.v2_tweet_retweeted_by.get_v2_tweet_retweeted_by import (
    GetV2TweetRetweetedByResponseBody,
)
from twitter_api.api.resources.v2_tweets import V2TweetsUrl
from twitter_api.api.resources.v2_tweets.get_v2_tweets import GetV2TweetsResponseBody
from twitter_api.api.resources.v2_tweets.post_v2_tweets import PostV2TweetsResponseBody
from twitter_api.api.resources.v2_tweets_search_all import V2TweetsSearchAllUrl
from twitter_api.api.resources.v2_tweets_search_all.get_v2_tweets_search_all import (
    GetV2TweetsSearchAllResponseBody,
)
from twitter_api.api.resources.v2_tweets_search_recent import V2TweetsSearchRecentUrl
from twitter_api.api.resources.v2_tweets_search_recent.get_v2_tweets_search_recent import (
    GetV2TweetsSearchRecentResponseBody,
)
from twitter_api.api.resources.v2_tweets_search_stream import V2TweetsSearchStreamUrl
from twitter_api.api.resources.v2_tweets_search_stream.get_v2_tweets_search_stream import (
    GetV2TweetsSearchStreamResponseBody,
)
from twitter_api.api.resources.v2_user import V2UserUrl
from twitter_api.api.resources.v2_user.get_v2_user import GetV2UserResponseBody
from twitter_api.api.resources.v2_user_followers import V2UserFollowersUrl
from twitter_api.api.resources.v2_user_followers.get_v2_user_followers import (
    GetV2UserFollowersResponseBody,
)
from twitter_api.api.resources.v2_user_following import V2UserFollowingUrl
from twitter_api.api.resources.v2_user_following.post_v2_user_following import (
    PostV2UserFollowingResponseBody,
)
from twitter_api.api.resources.v2_user_liked_tweets import V2UserLikedTweetsUrl
from twitter_api.api.resources.v2_user_liked_tweets.get_v2_user_liked_tweets import (
    GetV2UserLikedTweetsResponseBody,
)
from twitter_api.api.resources.v2_user_retweets import V2UserRetweetsUrl
from twitter_api.api.resources.v2_user_retweets.post_v2_user_retweets import (
    PostV2UserRetweetsResponseBody,
)
from twitter_api.api.resources.v2_user_tweets import V2UserTweetsUrl
from twitter_api.api.resources.v2_user_tweets.get_v2_user_tweets import (
    GetV2UserTweetsResponseBody,
)
from twitter_api.api.resources.v2_users import V2UsersUrl
from twitter_api.api.resources.v2_users.get_v2_users import GetV2UsersResponseBody
from twitter_api.api.types.v2_scope import Scope
from twitter_api.error import TwitterApiError
from twitter_api.rate_limit.manager.rate_limit_manager import RateLimitManager
from twitter_api.rate_limit.rate_limit_target import RateLimitTarget
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.oauth import (
    AccessSecret,
    AccessToken,
    ApiKey,
    ApiSecret,
    CallbackUrl,
    ClientId,
    ClientSecret,
    Env,
    OAuthVersion,
)

from .request.mock_request_client import MockRequestClient
from .request.request_client import RequestClient
from .twitter_api_client import TwitterApiClient


class TwitterApiMockClient(TwitterApiClient):
    """Twitter API V2 をモックするためのクライアント"""

    def __init__(
        self,
        *,
        oauth_version: OAuthVersion,
        rate_limit_target: RateLimitTarget,
        rate_limit_manager: Optional[RateLimitManager] = None,
    ) -> None:
        self._client = MockRequestClient(
            oauth_version=oauth_version,
            rate_limit_target=rate_limit_target,
            rate_limit_manager=rate_limit_manager,
        )

    @property
    def _request_client(self) -> RequestClient:
        return self._client

    @overload
    def inject_get_response_body(
        self,
        url: V2TweetsUrl,
        response_body: Union[
            GetV2TweetsResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: V2TweetUrl,
        response_body: Union[
            GetV2TweetResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: V2TweetRetweetedByUrl,
        response_body: Union[
            GetV2TweetRetweetedByResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: V2TweetsSearchAllUrl,
        response_body: Union[
            GetV2TweetsSearchAllResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: V2TweetsSearchRecentUrl,
        response_body: Union[
            GetV2TweetsSearchRecentResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: V2TweetsSearchStreamUrl,
        response_body: Union[
            GetV2TweetsSearchStreamResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: V2UsersUrl,
        response_body: Union[
            GetV2UsersResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: V2UserUrl,
        response_body: Union[
            GetV2UserResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: V2UserLikedTweetsUrl,
        response_body: Union[
            GetV2UserLikedTweetsResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: V2UserFollowersUrl,
        response_body: Union[
            GetV2UserFollowersResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: V2UserTweetsUrl,
        response_body: Union[
            GetV2UserTweetsResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    def inject_get_response_body(self, url, response_body) -> Self:
        self._client.inject_response_body(Endpoint("GET", url), response_body)

        return self

    @overload
    def inject_post_response_body(
        self,
        url: OauthRequestTokenUrl,
        response_body: Union[PostOauthRequestTokenResponseBody, TwitterApiError],
    ) -> Self:
        ...

    @overload
    def inject_post_response_body(
        self,
        url: Oauth2InvalidateTokenUrl,
        response_body: Union[
            PostOauth2InvalidateTokenResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_post_response_body(
        self,
        url: Oauth2TokenUrl,
        response_body: Union[
            PostOauth2TokenResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_post_response_body(
        self,
        url: V2TweetsUrl,
        response_body: Union[
            PostV2TweetsResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_post_response_body(
        self,
        url: V2UserFollowingUrl,
        response_body: Union[
            PostV2UserFollowingResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_post_response_body(
        self,
        url: V2UserRetweetsUrl,
        response_body: Union[
            PostV2UserRetweetsResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_post_response_body(
        self,
        url: V2DmConversationsWithParticipantMessagesUrl,
        response_body: Union[
            PostV2DmConversationsWithParticipantMessagesResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_post_response_body(
        self,
        url: V2DmConversationsUrl,
        response_body: Union[
            PostV2DmConversationsResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_post_response_body(
        self,
        url: V2DmConversationsMessagesUrl,
        response_body: Union[
            PostV2DmConversationMessagesResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    def inject_post_response_body(self, url, response_body) -> Self:
        self._client.inject_response_body(Endpoint("POST", url), response_body)

        return self

    def inject_delete_response_body(
        self,
        url: V2TweetUrl,
        response_body: Union[
            DeleteV2TweetResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        self._client.inject_response_body(Endpoint("DELETE", url), response_body)

        return self

    @classmethod
    def from_oauth2_bearer_token(
        cls,
        bearer_token: str,
        *,
        rate_limit_manager: Optional[RateLimitManager] = None,
    ):
        return TwitterApiMockClient(
            oauth_version="2.0",
            rate_limit_target="app",
            rate_limit_manager=rate_limit_manager,
        )

    @classmethod
    def from_oauth2_app(
        cls,
        *,
        api_key: ApiKey,
        api_secret: ApiSecret,
        rate_limit_manager: Optional[RateLimitManager] = None,
    ) -> Self:
        return TwitterApiMockClient(
            oauth_version="2.0",
            rate_limit_target="app",
            rate_limit_manager=rate_limit_manager,
        )

    @classmethod
    def from_oauth2_user_flow(
        cls,
        *,
        client_id: ClientId,
        client_secret: ClientSecret,
        callback_url: CallbackUrl,
        scope: list[Scope],
        rate_limit_manager: Optional[RateLimitManager] = None,
    ):
        from twitter_api.api.types.v2_authorization import OAuthV2AuthorizeClient
        from twitter_api.client.sessions.twitter_oauth2_mock_session import (
            TwitterOAuth2MockSession,
        )

        session = TwitterOAuth2MockSession(scope=scope)
        return OAuthV2AuthorizeClient(session=session)

    @classmethod
    def from_oauth1_user(
        cls,
        *,
        api_key: ApiKey,
        api_secret: ApiSecret,
        access_token: AccessToken,
        access_secret: AccessSecret,
        rate_limit_manager: Optional[RateLimitManager] = None,
    ):
        return TwitterApiMockClient(
            oauth_version="1.0a",
            rate_limit_target="app",
            rate_limit_manager=rate_limit_manager,
        )

    @classmethod
    def _get_env(cls, key: Env[str]) -> str:
        """
        環境変数を取り出す。

        Mock であるためとりあえず値を返す。
        """

        return ""
