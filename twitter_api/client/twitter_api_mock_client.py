from typing import Optional, Self, Union, overload

import twitter_api.api.v2.endpoints.tweets.retweeted_by as tweet_retweeted_by
import twitter_api.api.v2.endpoints.tweets.search.all as tweets_search_all
import twitter_api.api.v2.endpoints.tweets.search.recent as tweets_search_recent
import twitter_api.api.v2.endpoints.tweets.search.stream as tweets_search_stream
import twitter_api.api.v2.endpoints.users.tweets as user_tweets
from twitter_api.api.authentication.endpoints.oauth import (
    request_token as oauth_request_token,
)
from twitter_api.api.authentication.endpoints.oauth2 import invalidate_token, token
from twitter_api.api.responses import (
    Oauth2PostInvalidateTokenResponseBody,
    Oauth2PostTokenResponseBody,
    OauthPostRequestTokenResponseBody,
    V2DeleteTweetResponseBody,
    V2GetTweetResponseBody,
    V2GetTweetRetweetedByResponseBody,
    V2GetTweetsResponseBody,
    V2GetTweetsSearchAllResponseBody,
    V2GetTweetsSearchRecentResponseBody,
    V2GetTweetsSearchStreamResponseBody,
    V2GetUserFollowersResponseBody,
    V2GetUserLikedTweetsResponseBody,
    V2GetUserResponseBody,
    V2GetUsersResponseBody,
    V2GetUserTweetsResponseBody,
    V2PostTweetResponseBody,
    V2PostUserFollowingResponseBody,
)
from twitter_api.api.v2.endpoints import tweets, users
from twitter_api.api.v2.endpoints.users import followers, following, liked_tweets
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
        url: tweets.TweetsUrl,
        response_body: Union[
            V2GetTweetsResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: tweets.TweetUrl,
        response_body: Union[
            V2GetTweetResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: tweet_retweeted_by.TweetRetweetedByUrl,
        response_body: Union[
            V2GetTweetRetweetedByResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: tweets_search_all.TweetsSearchAllUrl,
        response_body: Union[
            V2GetTweetsSearchAllResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: tweets_search_recent.TweetsSearchRecentUrl,
        response_body: Union[
            V2GetTweetsSearchRecentResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: tweets_search_stream.TweetsSearchStreamUrl,
        response_body: Union[
            V2GetTweetsSearchStreamResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: users.UsersUrl,
        response_body: Union[
            V2GetUsersResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: users.UserUrl,
        response_body: Union[
            V2GetUserResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: liked_tweets.UserLikedTweetsUrl,
        response_body: Union[
            V2GetUserLikedTweetsResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: followers.UserFollowersUrl,
        response_body: Union[
            V2GetUserFollowersResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: user_tweets.UserTweetsUrl,
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
        url: oauth_request_token.OauthRequestTokenUrl,
        response_body: Union[OauthPostRequestTokenResponseBody, TwitterApiError],
    ) -> Self:
        ...

    @overload
    def inject_post_response_body(
        self,
        url: invalidate_token.Oauth2InvalidateTokenUrl,
        response_body: Union[
            Oauth2PostInvalidateTokenResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_post_response_body(
        self,
        url: token.Oauth2TokenUrl,
        response_body: Union[
            Oauth2PostTokenResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_post_response_body(
        self,
        url: tweets.TweetsUrl,
        response_body: Union[
            V2PostTweetResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_post_response_body(
        self,
        url: following.UserFollowingUrl,
        response_body: Union[
            V2PostUserFollowingResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    def inject_post_response_body(self, url, response_body) -> Self:
        self._client.inject_response_body(Endpoint("POST", url), response_body)

        return self

    def inject_delete_response_body(
        self,
        url: tweets.TweetUrl,
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
