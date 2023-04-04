from typing import Optional, Self, Union, overload

from twitter_api.api.resources.oauth2_invalidate_token import (
    Oauth2InvalidateTokenUrl,
    Oauth2PostInvalidateTokenResponseBody,
)
from twitter_api.api.resources.oauth2_token import Oauth2TokenUrl
from twitter_api.api.resources.oauth2_token.post_oauth2_token import (
    Oauth2PostTokenResponseBody,
)
from twitter_api.api.resources.oauth_request_token import OauthRequestTokenUrl
from twitter_api.api.resources.oauth_request_token.post_oauth_request_token import (
    OauthPostRequestTokenResponseBody,
)
from twitter_api.api.resources.v2_dm_conversation_messages import (
    DmConversationsMessagesUrl,
    V2PostDmConversationMessagesResponseBody,
)
from twitter_api.api.resources.v2_dm_conversations import DmConversationsUrl
from twitter_api.api.resources.v2_dm_conversations.post_dm_conversations import (
    V2PostDmConversationsResponseBody,
)
from twitter_api.api.resources.v2_dm_conversations_with_messages import (
    DmConversationsWithParticipantMessagesUrl,
    V2PostDmConversationsWithParticipantMessagesResponseBody,
)
from twitter_api.api.resources.v2_tweet import TweetUrl
from twitter_api.api.resources.v2_tweet.delete_tweet import V2DeleteTweetResponseBody
from twitter_api.api.resources.v2_tweet.get_tweet import V2GetTweetResponseBody
from twitter_api.api.resources.v2_tweet_retweeted_by import TweetRetweetedByUrl
from twitter_api.api.resources.v2_tweet_retweeted_by.get_tweet_retweeted_by import (
    V2GetTweetRetweetedByResponseBody,
)
from twitter_api.api.resources.v2_tweets import TweetsUrl
from twitter_api.api.resources.v2_tweets.get_tweets import V2GetTweetsResponseBody
from twitter_api.api.resources.v2_tweets.post_tweet import V2PostTweetResponseBody
from twitter_api.api.resources.v2_tweets_search_all import TweetsSearchAllUrl
from twitter_api.api.resources.v2_tweets_search_all.get_tweets_search_all import (
    V2GetTweetsSearchAllResponseBody,
)
from twitter_api.api.resources.v2_tweets_search_recent import TweetsSearchRecentUrl
from twitter_api.api.resources.v2_tweets_search_recent.get_tweets_search_recent import (
    V2GetTweetsSearchRecentResponseBody,
)
from twitter_api.api.resources.v2_tweets_search_stream import TweetsSearchStreamUrl
from twitter_api.api.resources.v2_tweets_search_stream.get_tweets_search_stream import (
    V2GetTweetsSearchStreamResponseBody,
)
from twitter_api.api.resources.v2_user import UserUrl
from twitter_api.api.resources.v2_user.get_user import V2GetUserResponseBody
from twitter_api.api.resources.v2_user_followers import UserFollowersUrl
from twitter_api.api.resources.v2_user_followers.get_user_followers import (
    V2GetUserFollowersResponseBody,
)
from twitter_api.api.resources.v2_user_following import UserFollowingUrl
from twitter_api.api.resources.v2_user_following.post_user_following import (
    V2PostUserFollowingResponseBody,
)
from twitter_api.api.resources.v2_user_liked_tweets import UserLikedTweetsUrl
from twitter_api.api.resources.v2_user_liked_tweets.get_user_liked_tweets import (
    V2GetUserLikedTweetsResponseBody,
)
from twitter_api.api.resources.v2_user_retweets import UserRetweetsUrl
from twitter_api.api.resources.v2_user_retweets.post_user_retweets import (
    V2PostUserRetweetsResponseBody,
)
from twitter_api.api.resources.v2_user_tweets import UserTweetsUrl
from twitter_api.api.resources.v2_user_tweets.get_user_tweets import (
    V2GetUserTweetsResponseBody,
)
from twitter_api.api.resources.v2_users import UsersUrl
from twitter_api.api.resources.v2_users.get_users import V2GetUsersResponseBody
from twitter_api.error import TwitterApiError
from twitter_api.rate_limit.manager.rate_limit_manager import RateLimitManager
from twitter_api.rate_limit.rate_limit_target import RateLimitTarget
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.oauth import (
    AccessSecret,
    AccessToken,
    ApiKey,
    ApiSecret,
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
        url: TweetsUrl,
        response_body: Union[
            V2GetTweetsResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: TweetUrl,
        response_body: Union[
            V2GetTweetResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: TweetRetweetedByUrl,
        response_body: Union[
            V2GetTweetRetweetedByResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: TweetsSearchAllUrl,
        response_body: Union[
            V2GetTweetsSearchAllResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: TweetsSearchRecentUrl,
        response_body: Union[
            V2GetTweetsSearchRecentResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: TweetsSearchStreamUrl,
        response_body: Union[
            V2GetTweetsSearchStreamResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: UsersUrl,
        response_body: Union[
            V2GetUsersResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: UserUrl,
        response_body: Union[
            V2GetUserResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: UserLikedTweetsUrl,
        response_body: Union[
            V2GetUserLikedTweetsResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: UserFollowersUrl,
        response_body: Union[
            V2GetUserFollowersResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: UserTweetsUrl,
        response_body: Union[
            V2GetUserTweetsResponseBody,
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
        response_body: Union[OauthPostRequestTokenResponseBody, TwitterApiError],
    ) -> Self:
        ...

    @overload
    def inject_post_response_body(
        self,
        url: Oauth2InvalidateTokenUrl,
        response_body: Union[
            Oauth2PostInvalidateTokenResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_post_response_body(
        self,
        url: Oauth2TokenUrl,
        response_body: Union[
            Oauth2PostTokenResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_post_response_body(
        self,
        url: TweetsUrl,
        response_body: Union[
            V2PostTweetResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_post_response_body(
        self,
        url: UserFollowingUrl,
        response_body: Union[
            V2PostUserFollowingResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_post_response_body(
        self,
        url: UserRetweetsUrl,
        response_body: Union[
            V2PostUserRetweetsResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_post_response_body(
        self,
        url: DmConversationsWithParticipantMessagesUrl,
        response_body: Union[
            V2PostDmConversationsWithParticipantMessagesResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_post_response_body(
        self,
        url: DmConversationsUrl,
        response_body: Union[
            V2PostDmConversationsResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_post_response_body(
        self,
        url: DmConversationsMessagesUrl,
        response_body: Union[
            V2PostDmConversationMessagesResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    def inject_post_response_body(self, url, response_body) -> Self:
        self._client.inject_response_body(Endpoint("POST", url), response_body)

        return self

    def inject_delete_response_body(
        self,
        url: TweetUrl,
        response_body: Union[
            V2DeleteTweetResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        self._client.inject_response_body(Endpoint("DELETE", url), response_body)

        return self

    @classmethod
    def from_bearer_token(
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
    def from_app_auth_v2(
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
    def from_user_auth_v1(
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
