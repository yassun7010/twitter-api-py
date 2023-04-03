from typing import Optional, Self, Union, overload

import twitter_api.api.v2.endpoints.tweets.retweeted_by as tweet_retweeted_by
import twitter_api.api.v2.endpoints.tweets.search.all as tweets_search_all
import twitter_api.api.v2.endpoints.tweets.search.recent as tweets_search_recent
import twitter_api.api.v2.endpoints.tweets.search.stream as tweets_search_stream
import twitter_api.api.v2.endpoints.users.tweets as user_tweets
from twitter_api.api.authentication.endpoints.oauth import post_request_token
from twitter_api.api.authentication.endpoints.oauth2 import (
    post_invalidate_token,
    post_token,
)
from twitter_api.api.v2.endpoints import tweets, users
from twitter_api.api.v2.endpoints.tweets.retweeted_by import get_tweet_retweeted_by
from twitter_api.api.v2.endpoints.tweets.search.all import get_tweets_search_all
from twitter_api.api.v2.endpoints.tweets.search.recent import get_tweets_search_recent
from twitter_api.api.v2.endpoints.tweets.search.stream import get_tweets_search_stream
from twitter_api.api.v2.endpoints.users import (
    followers,
    following,
    get_user,
    get_users,
    liked_tweets,
)
from twitter_api.api.v2.endpoints.users.followers import get_user_followers
from twitter_api.api.v2.endpoints.users.following import post_user_following
from twitter_api.api.v2.endpoints.users.liked_tweets import get_user_liked_tweets
from twitter_api.api.v2.endpoints.users.tweets import get_user_tweets
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
            tweets.get_tweets.V2GetTweetsResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: tweets.TweetUrl,
        response_body: Union[
            tweets.get_tweet.V2GetTweetResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: tweet_retweeted_by.TweetRetweetedByUrl,
        response_body: Union[
            get_tweet_retweeted_by.V2GetTweetRetweetedByResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: tweets_search_all.TweetsSearchAllUrl,
        response_body: Union[
            get_tweets_search_all.V2GetTweetsSearchAllResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: tweets_search_recent.TweetsSearchRecentUrl,
        response_body: Union[
            get_tweets_search_recent.V2GetTweetsSearchRecentResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: tweets_search_stream.TweetsSearchStreamUrl,
        response_body: Union[
            get_tweets_search_stream.V2GetTweetsSearchStreamResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: users.UsersUrl,
        response_body: Union[
            get_users.V2GetUsersResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: users.UserUrl,
        response_body: Union[
            get_user.V2GetUserResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: liked_tweets.UserLikedTweetsUrl,
        response_body: Union[
            get_user_liked_tweets.V2GetUserLikedTweetsResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: followers.UserFollowersUrl,
        response_body: Union[
            get_user_followers.V2GetUserFollowersResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: user_tweets.UserTweetsUrl,
        response_body: Union[
            get_user_tweets.V2GetUserTweetsResponseBody,
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
        url: post_request_token.Url,
        response_body: Union[
            post_request_token.OauthPostRequestTokenResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_post_response_body(
        self,
        url: post_invalidate_token.Url,
        response_body: Union[
            post_invalidate_token.Oauth2PostInvalidateTokenResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_post_response_body(
        self,
        url: post_token.Url,
        response_body: Union[
            post_token.Oauth2PostTokenResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_post_response_body(
        self,
        url: tweets.TweetsUrl,
        response_body: Union[
            tweets.post_tweet.V2PostTweetResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_post_response_body(
        self,
        url: following.UserFollowingUrl,
        response_body: Union[
            post_user_following.V2PostUserFollowingResponseBody,
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
            tweets.delete_tweet.V2DeleteTweetResponseBody,
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
